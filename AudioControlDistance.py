maxdistance = 46
import serial.tools.list_ports
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portsList = []

for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

val = input("Select Port: COM")

for x in range(0,len(portsList)):
    if portsList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portVar)

serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()
distance = 0
pastDistance = 0
pastpastDistance = 0
distances = []
sumdistances = 0
while True:
    if serialInst.in_waiting:
        packet = serialInst.readline()
        distance = float(packet.decode('utf').rstrip('\n'))
        distances.append(distance)
        if len(distances) > 20:
            for x in distances:
                sumdistances += x
            sumdistances /= len(distances)
            if sumdistances < pastDistance+5 or sumdistances < pastDistance-5:
                pastDistance = sumdistances
            sumdistances = 0
            distances.pop(0)
        else:
            pastDistance = distance
        if pastpastDistance != round(round((pastDistance),2)*100/maxdistance):
            pastpastDistance = round(round((pastDistance),2)*100/maxdistance)
            print(pastpastDistance)
            if pastpastDistance <= 100 and pastpastDistance > 0:
                volume.SetMasterVolumeLevel(35*math.log((pastpastDistance/100), 10), None)
            

