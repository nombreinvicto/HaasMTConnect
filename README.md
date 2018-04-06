# HAAS VF2 MTConnect Adapter
An MTConnect adapter for the HAAS VF2 CNC machine written in Python.

# Introduction
A python encoded adapter for the HAAS VF2 CNC machine named 'HAAS_adapterv2.py' has been released on the public domain. Unless required by applicable law or agreed to in writing, the software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

The adapter makes a HAAS VF2 CNC machine MTConnect protocol compliant and enables the machine to communicate with an MTConnect agent. The software has been tested on a HAAS VF2 machine with the MTConnect cpp agent. The steps to build and create the agent can be found at https://github.com/mtconnect/cppagent.

#Usage
The implementation assumes that the adapter would be running on an external IOT device, e.g, a beaglebone, raspberry pi ( or a PC ) that is connected and communicating with the HAAS VF2 via RS232 communication. Hence, the primary mode of fetching process parameters from the HAAS is through serial communication. The adapter code in its current state assumes that the HAAS is connected to the IOT device through the 'ttyUSB0' port ( would be 'COM' for PC based systems). The HAAS with its serial DB9 port has to be connected to the IOT device via the implementation of appropriate TTL - RS 232 logic converter modules ( such as a serial to USB module). 
