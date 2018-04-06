import threading, time, socket, sys, datetime, serial, re

client_counter = 0
client_list = []
first_run_flag = 1
lock = threading.Lock()
event = threading.Event()
event.set()

# Initialising 7 global attributes for HAAS serial comm macros
mac_status = part_num = prog_name = sspeed = coolant = sload = cut_status = combined_output = 'Nil'

"""Creating Socket Objects"""
HOST = ''
PORT = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

"""Binding to the local port/host"""
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

"""Start Listening to Socket for Clients"""
s.listen(5)

"""Function to Clear Out Threads List Once All Threads are Empty"""


def thread_list_empty():
    global client_list, client_counter

    while True:
        try:
            if client_counter == 0 and first_run_flag == 0 and client_list != []:
                print("%d Clients Active" % client_counter)
                print("Clearing All threads....")
                for index, thread in enumerate(client_list):
                    thread.join()
                client_list = []
        except:
            print("Invalid Client List Deletion")


"""Function that parses attributes from the HAAS"""


def fetch_from_HAAS():
    global mac_status, part_num, prog_name, sspeed, coolant, sload, cut_status, combined_output


    ser = serial.Serial()
    ser.baudrate = 9600
    # Assuming HAAS is connected to ttyUSB0 port of Linux System
    ser.port = '/dev/ttyUSB0'
    ser.timeout = 1

    try:
        ser.open()
    except serial.SerialException:
        if ser.is_open:
            try:
                print("Port was open. Attempting to close.")
                ser.close()
                time.sleep(2)
                ser.open()
            except:
                print("Port is already open. Failed to close. Try again.")
                event.clear()
        else:
            print("Failed to connect to serial port. Make sure it is free or it exists. Try again.")
            event.clear()

    while True:
        out = ''
        try:
            # Reading Status
            ser.write(b"Q500\r")
            status = ser.readline()
            status = status[2:-3]
            print(status)

            if status != '':
                mac_status = 'ON'
            else:
                mac_status = 'OFF'

            out += '|power|' + str(mac_status)

            if 'PART' in status:
                part_num = (re.findall(r"[-+]?\d*\.\d+|\d+", status.split(',')[-1])[0])
                prog_name = status.split(',')[1]
            else:
                part_num = 'Nil'
                prog_name = 'Nil'
            out += '|PartCountAct|' + str(part_num) + '|program|' + str(prog_name)

            # Reading Spindle Speed

            try:
                ser.write(b"Q600 3027\r")
                sspeed = ser.readline()
                sspeed = str(float(sspeed[15:26]))
            except:
                sspeed = 'Nil'
            out += '|Srpm|' + sspeed

            # Reading Coolant Level
            try:
                ser.write(b"Q600 1094\r")
                coolant = ser.readline()
                coolant = str(float(coolant[15:26]))
            except:
                pass

            # Quering Spindle Load
            try:
                ser.write(b"Q600 1098\r")
                sload = ser.readline()
                sload = str(float(sload[15:26]))
            except:
                sload = 'Nil'
            out += '|Sload|' + sload

            # Quering Cutting Status
            try:
                cut_status = status.split(',')[status.split(',').index('PARTS') - 1]
                if 'FEED' in cut_status:
                    cut_status = 'FEED_HOLD'
                elif 'IDLE' in cut_status:
                    cut_status = 'IDLE'
            except:
                cut_status = 'Nil'
            out += '|execution|' + cut_status

            # Present Machine Coordinates
            try:
                ser.write(b"Q600 5021\r")
                coord_x = ser.readline()
                coord_x = coord_x[15:27]
            except:
                coord_x = 'Nil'
            # Including this since machine OFF doesnt raise x/y/z parsing exception
            if coord_x == '':
                coord_x = 'Nil'
            out += '|Xabs|' + str(coord_x).replace(" ", "")

            try:
                ser.write(b"Q600 5022\r")
                coord_y = ser.readline()
                coord_y = coord_y[15:27]
            except:
                coord_y = 'Nil'
            if coord_y == '':
                coord_y = 'Nil'
            out += '|Yabs|' + str(coord_y).replace(" ", "")

            try:
                ser.write(b"Q600 5023\r")
                coord_z = ser.readline()
                coord_z = coord_z[15:27]
            except:
                coord_z = 'Nil'
            if coord_z == '':
                coord_z = 'Nil'
            out += '|Zabs|' + str(coord_z).replace(" ", "")

            try:
                ser.write(b"Q600 5024\r")
                coord_a = ser.readline()
                coord_a = coord_a[15:27]
            except:
                coord_a = 'Nil'
            if coord_a == '':
                coord_a = 'Nil'
            out += '|Aabs|' + str(coord_a).replace(" ", "")

            # Final data purge
            combined_output = '\r\n' + datetime.datetime.now().isoformat() + 'Z' + out

        except:
            print("Failed fetching values from machine")
            time.sleep(2)

        # time.sleep(0.1)

    ser.close()


"""Main Thread Class For Clients"""


class NewClientThread(threading.Thread):
    # init method called on thread object creation,
    def __init__(self, conn, string_address):
        threading.Thread.__init__(self)
        self.connection_object = conn
        self.client_ip = string_address

    # run method called on .start() execution
    def run(self):
        global client_counter, combined_output
        global lock
        while True:
            try:
                print("Sending data to Client {} in {}".format(self.client_ip, self.getName()))
                out = combined_output
                self.connection_object.sendall(out)
                time.sleep(0.5)

            except:
                lock.acquire()
                try:
                    client_counter = client_counter - 1
                    print("Connection disconnected for ip {} ".format(self.client_ip))
                    break
                finally:
                    lock.release()


"""Starts From Here"""
t1 = threading.Thread(target=thread_list_empty)
t2 = threading.Thread(target=fetch_from_HAAS)
t1.setDaemon(True)
t2.setDaemon(True)
t1.start()
t2.start()
time.sleep(2)

while event.is_set():

    if first_run_flag == 1:
        print("Listening to Port: %d...." % PORT)


    try:
        conn, addr = s.accept()
        lock.acquire()
        client_counter = client_counter + 1
        first_run_flag = 0
        print("Accepting Comm From:" + " " + str(addr))
        new_Client_Thread = NewClientThread(conn, str(addr))
        new_Client_Thread.setDaemon(True)
        client_list.append(new_Client_Thread)
        print(client_list)
        new_Client_Thread.start()
        lock.release()
    except KeyboardInterrupt:
        print("\nExiting Program")
        sys.exit()

if not event.is_set():
    print("\nExiting Program")
    sys.exit()
