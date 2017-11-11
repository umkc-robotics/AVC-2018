import sys
import time 
from Phidget22.Devices.Magnetometer import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from AsyncDriver import ThreadDriver, ProcessDriver
from collections import namedtuple
from math import atan2, degrees
# set up CompassData class -> named tuple (x,y,z)
CompassData = namedtuple("CompassData", ["x","y","z"])



class CompassException(Exception):
    pass



class Compass(ProcessDriver):

    def __init__(self, conf):
        self.conf = conf
        self.compass_connected = False
        self.heading = None
        ProcessDriver.__init__(self, compass_process, (conf,))

    def is_connected(self):
        """
        Returns boolean explaining whether or not compass has connected
        """
        return self.compass_connected

    def get_heading(self):
        """
        Returns current heading
        """
        return self.heading

    def set_direction(self, data):
        """
        Using a CompassData object, calculate current heading
        Returns: None
        """
        # using only x and y coordinate of data, figure out heading
        radHeading = atan2(data.y,data.x) # NOTE: declination rad taken care of in device
        self.heading = degrees(radHeading)

    def handle_input(self, input_obj):
        if isinstance(input_obj, CompassData):
            self.set_direction(input_obj)
        elif isinstance(input_obj, bool):
            print "RECEIVING A BOOLEAN"
            self.compass_connected = input_obj



def compass_process(conf, comm_pipe):
    try:
        keep_running = True
        # start magnetometer
        ch = Magnetometer()
        # give it a comm_pipe parameter to send data through handlers
        ch.comm_pipe = comm_pipe
        # attach handlers
        ch.setOnAttachHandler(MagnetometerAttached)
        ch.setOnDetachHandler(MagnetometerDetached)
        ch.setOnErrorHandler(ErrorEvent)
        ch.setOnMagneticFieldChangeHandler(MagneticFieldChangeHandler)
        # now wait for attachment
        print("Waiting for the Phidget Magnetometer Object to be attached...")
        ch.openWaitForAttachment(5000)
        # send confirmation the magnetometer was found
        comm_pipe.send(True)
        while keep_running:
            # check pipe for messages
            if comm_pipe.poll():
                received = comm_pipe.recv()
                if received == "EXIT":
                    keep_running = False
                    break

    except Exception as e:
    	try:
        	print "SENDING ERROR..."
        	comm_pipe.send(e)
        except IOError as e:
        	pass
    finally:
        try:
            ch.close()
        except PhidgetException as e:
            pass


# HANDLER FUNCTIONS

def MagnetometerAttached(e):
    try:
        attached = e
        #print("\nAttach Event Detected (Information Below)")
        #print("===========================================")
        #print("Library Version: %s" % attached.getLibraryVersion())
        #print("Serial Number: %d" % attached.getDeviceSerialNumber())
        #print("Channel: %d" % attached.getChannel())
        #print("Channel Class: %s" % attached.getChannelClass())
        #print("Channel Name: %s" % attached.getChannelName())
        #print("Device ID: %d" % attached.getDeviceID())
        #print("Device Version: %d" % attached.getDeviceVersion())
        #print("Device Name: %s" % attached.getDeviceName())
        #print("Device Class: %d" % attached.getDeviceClass())
        #print("\n")

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        raise e  
    
def MagnetometerDetached(e):
    detached = e
    try:
        print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        raise e

def ErrorEvent(e, eCode, description):
    print("Error %i : %s" % (eCode, description))
    raise e

def MagneticFieldChangeHandler(e, fieldStrength, timestamp):
    #print("Magnetic Field: %f  %f  %f" % (fieldStrength[0], fieldStrength[1], fieldStrength[2]))
    #print("Timestamp: %f\n" % timestamp)
    e.comm_pipe.send(CompassData(fieldStrength[0], fieldStrength[1], fieldStrength[2]))
