#Experiment_for_MOT_lifetime.
from labscript import *
from labscript_devices.PulseBlasterUSB import PulseBlasterUSB
from labscript_devices.NI_DAQmx.models import NI_PXIe_6535
from labscript_devices.NI_DAQmx.models import NI_PXIe_6738
#from user_devices.AndorSolis.labscript_devices import AndorSolis
from user_devices.MakoCamera.labscript_devices import Mako_Camera

PulseBlasterUSB(name='pulseblaster_0')
ClockLine(name='clockline0', pseudoclock=pulseblaster_0.pseudoclock, connection='flag 0')
ClockLine(name='clockline1', pseudoclock=pulseblaster_0.pseudoclock, connection='flag 1')
NI_PXIe_6738(name='NI_AO_card', parent_device=clockline0, clock_terminal='PFI7', MAX_name='PXI1Slot2', max_AO_sample_rate=400e3)
NI_PXIe_6535(name='NI_DIO_card', parent_device=clockline1, clock_terminal='PFI4', MAX_name='PXI1Slot3')

DigitalOut(name='AOM_3D', parent_device=NI_DIO_card, connection='port0/line0') # 3.3V output
DigitalOut(name='Mako_3D', parent_device=NI_DIO_card, connection='port0/line1')
DigitalOut(name='Shutter_IMG', parent_device=NI_DIO_card, connection='port0/line2')
DigitalOut(name='Shutter_Push', parent_device=NI_DIO_card, connection='port0/line3')
DigitalOut(name='Shutter_3D', parent_device=NI_DIO_card, connection='port0/line4')
DigitalOut(name='Dipole_AOM', parent_device=NI_DIO_card, connection='port0/line5')
DigitalOut(name='AOM_2D', parent_device=NI_DIO_card, connection='port0/line6')
DigitalOut(name='K_AOM_Push', parent_device=NI_DIO_card, connection='port0/line7')
DigitalOut(name='K_AOM_3D', parent_device=NI_DIO_card, connection='port1/line0')
DigitalOut(name='K_AOM_2D', parent_device=NI_DIO_card, connection='port1/line1')
DigitalOut(name='Na_EOM_3D', parent_device=NI_DIO_card, connection='port1/line2')
DigitalOut(name='Na_Zyla', parent_device=NI_DIO_card, connection='port1/line3')

AnalogOut(name='FREQ_2D', parent_device=NI_AO_card, connection='ao0')
AnalogOut(name='INT_2D', parent_device=NI_AO_card, connection='ao1')
AnalogOut(name='FREQ_3D', parent_device=NI_AO_card, connection='ao2')
AnalogOut(name='INT_3D', parent_device=NI_AO_card, connection='ao3')
AnalogOut(name='FREQ_Push', parent_device=NI_AO_card, connection='ao4')
AnalogOut(name='INT_Push', parent_device=NI_AO_card, connection='ao5')
AnalogOut(name='INT_Dipole', parent_device=NI_AO_card, connection='ao6')
AnalogOut(name='K_INT_2D', parent_device=NI_AO_card, connection='ao7')
AnalogOut(name='K_INT_Push', parent_device=NI_AO_card, connection='ao8')
AnalogOut(name='K_FREQ_3D', parent_device=NI_AO_card, connection='ao9')
DigitalOut(name='IGBT', parent_device=NI_AO_card, connection='port0/line0') # 5V output
DigitalOut(name='AOM_Push', parent_device=NI_AO_card, connection='port0/line1')

#AndorSolis('Zyla', NI_DIO_card, 'port1/line3', 0)#11684
#MakoCamera('mako', NI_DIO_card, 'port0/line1', '1', camera_attributes={'AcquisitionMode':'Continuous', 'ExposureMode':'Timed', 'TriggerActivation':'RisingEdge', 'TriggerMode':'Off',  'TriggerSelector':'FrameStart', 'TriggerSource':'Freerun'})
Mako_Camera('mako', NI_DIO_card, 'port0/line1', 536905351)

###--------------------------------------------------------------###
from SoPaExpClass import ExperimentClass
Experiment = myClass()
###


