# HAAS VF2 MTConnect Adapter
An MTConnect adapter for the HAAS VF2 CNC machine written in Python.

# Introduction
A python encoded adapter for the HAAS VF2 CNC machine named 'HAAS_adapterv2.py' has been released on the public domain. Unless required by applicable law or agreed to in writing, the software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either expressed or implied.

The adapter makes a HAAS VF2 CNC machine MTConnect protocol compliant and enables the machine to communicate with an MTConnect agent. The software has been tested on a HAAS VF2 machine with the MTConnect cpp agent. The steps to build and create the agent can be found at https://github.com/mtconnect/cppagent. The accompanying HAAS-VF2.xml mtconnect schema is to be appropriately routed to in the `agent.cfg` file once the agent is installed.

# Usage
The implementation assumes that the adapter would be running on an external IOT device, e.g, a beaglebone, raspberry pi (or a PC) that is connected and communicating with the HAAS VF2 via RS232 communication. Hence, the primary mode of fetching process parameters from the HAAS is through serial communication. The adapter code in its current state assumes that the HAAS is connected to the IOT device through the `ttyUSB0` port (would be 'COM' for PC based systems). The HAAS with its serial DB9 port has to be connected to the IOT device via the implementation of appropriate TTL - RS 232 logic converter modules ( such as a serial to USB module). It is therefore to the discretion of the user to change the serial port address to approrpate value when running the adapter.

The default TCP/IP port that the adapter publishes data to is set to:

`PORT = 7000`

It is upto the discretion of the user to update the port address to cater to specific requirements if needed.

# Process Parameters
The current implementation fetches a limited number of process parameters from the HAAS VF2 namely:
1. Power Status
2. Part Number
3. Program Name
4. Spindle Speed
5. Spindle Load
6. Execution Status
7. Absolute X, Y and Z co-ordinates

These parameter values are obtained by writing specific macros to the serial port of the IOT device that is connected to the HAAS. For example, writing `Q600 5023` yields the absolute Z co-ordinate. It is upto the discretion of the user to add code content if there is need of fetching of other types of process parameters. The user is referred to the HAAS mill operator's manual at https://goo.gl/wxH7YE for appropriate macro codes for different process parameters.

# MTConnect
For more information on the MTConnect standard and the dataitems included within the standard please visit http://www.mtconnect.org/

