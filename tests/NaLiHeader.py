from labscript import *
from labscript_devices.CiceroOpalKellyXEM3001 import CiceroOpalKellyXEM3001
from labscript_devices.NI_DAQmx.models import NI_PXI_6254
from labscript_devices.NI_DAQmx.models import NI_PXI_6733
from user_devices.MakoCamera.labscript_devices import MakoCamera
from serial import Serial
from windfreak import SynthHD
from user_devices.SynthHDDevice.labscript_devices import SynthHDDevice
from user_devices.CustomArduinoDevice.labscript_devices import CustomArduinoDevice
#from labscript_devices.MakoCamera.labscript_devices import MakoCamera

CiceroOpalKellyXEM3001(name='clock', serial='1711000H46')

NI_PXI_6733(name='Bilbo_card_4', parent_device=clock.clockline, clock_terminal='PFI1', MAX_name='PXI1Slot4')
NI_PXI_6733(name='Gollum_card_5', parent_device=clock.clockline, clock_terminal='PFI7', MAX_name='PXI1Slot5')
NI_PXI_6733(name='Frodo_card_6', parent_device=clock.clockline, clock_terminal='PFI7', MAX_name='PXI1Slot6')
NI_PXI_6254(name='Gandalf_card_2', parent_device=clock.clockline, clock_terminal='PFI0', MAX_name='PXI1Slot2')
CustomArduinoDevice('arduino', com_port='COM3')
SynthHDDevice('synth',com_port='COM4')

#CARD 6 (Frodo)  : This is a 6733 card. All the channels out of this card are defined below.
#digital channels
DigitalOut(name='D1_1_Na_Big_AOM',parent_device=Frodo_card_6, connection='port0/line0')
DigitalOut(name='D1_2_Na_MOT_AOM',parent_device=Frodo_card_6, connection='port0/line1')
DigitalOut(name='D1_3_Na_imaging_AOM',parent_device=Frodo_card_6, connection='port0/line2')
DigitalOut(name='D1_4_slower_shutter',parent_device=Frodo_card_6, connection='port0/line3')
Shutter(name='D1_5_Na_imaging_shutter',parent_device=Frodo_card_6, connection='port0/line4')
Shutter(name='D1_6_Na_repumper_shutter',parent_device=Frodo_card_6, connection='port0/line5')
Shutter(name='D1_7_Na_umpump_shutter',parent_device=Frodo_card_6, connection='port0/line6')
DigitalOut(name='D1_8_Na_MOT_shutter',parent_device=Frodo_card_6, connection='port0/line7')

#Analog channels
AnalogOut(name='A1_1_Na_img_int', parent_device=Frodo_card_6, connection='ao0')
AnalogOut(name='A1_2_Li_beat_freq', parent_device=Frodo_card_6, connection='ao1')
AnalogOut(name='A1_3_Verdi_AOM', parent_device=Frodo_card_6, connection='ao2')
AnalogOut(name='A1_4_Li_img_int', parent_device=Frodo_card_6, connection='ao3')
AnalogOut(name='A1_5_ODT1_horizontal', parent_device=Frodo_card_6, connection='ao4')
AnalogOut(name='A1_6_ODT1_ver', parent_device=Frodo_card_6, connection='ao5')
AnalogOut(name='A1_7_ODT2_hor', parent_device=Frodo_card_6, connection='ao6')
AnalogOut(name='A1_8_ODT2_ver', parent_device=Frodo_card_6, connection='ao7')

#CARD 4 (Bilbo)  : This is a 6733 card. All the channels out of this card are defined below.
#digital channels

DigitalOut(name='D2_1_Na_repump_AOM',parent_device=Bilbo_card_4,connection='port0/line0')
DigitalOut(name='D2_2_Na_umpump_repump_AOM',parent_device=Bilbo_card_4,connection='port0/line1')
DigitalOut(name='D2_3_Na_slower_AOM',parent_device=Bilbo_card_4,connection='port0/line2')
DigitalOut(name='D2_4_Na_umpump_AOM',parent_device=Bilbo_card_4,connection='port0/line3')
DigitalOut(name='D2_5_Antibias_switch',parent_device=Bilbo_card_4,connection='port0/line4')
DigitalOut(name='D2_6_Li_MOT_int',parent_device=Bilbo_card_4,connection='port0/line5')
DigitalOut(name='D2_7_Schutz_box',parent_device=Bilbo_card_4,connection='port0/line6')
DigitalOut(name='D2_8_Li_repump_int',parent_device=Bilbo_card_4,connection='port0/line7')

#anlog channels
AnalogOut(name='A2_1_curvature_power_supply', parent_device=Bilbo_card_4, connection='ao0')
AnalogOut(name='A2_2_Gradient_power_supply', parent_device=Bilbo_card_4, connection='ao1')
AnalogOut(name='A2_3_bias_power_supply', parent_device=Bilbo_card_4, connection='ao2')
AnalogOut(name='A2_4_finetune_power_supply', parent_device=Bilbo_card_4, connection='ao3')
AnalogOut(name='A2_5_Na_MOT_power', parent_device=Bilbo_card_4, connection='ao4')
AnalogOut(name='A2_6_Offset_Y_fast', parent_device=Bilbo_card_4, connection='ao5')
AnalogOut(name='A2_7_Na_img_freq', parent_device=Bilbo_card_4, connection='ao6')
AnalogOut(name='A2_8_Sirah_AOM', parent_device=Bilbo_card_4, connection='ao7')

#CARD 5 (Gollum)  : This is a 6733 card. All the channels out of this card are defined below.
#digital channels

DigitalOut(name='D4_1_Makotrigger',parent_device=Gollum_card_5,connection='port0/line0')
DigitalOut(name='D4_2_Retiga_trigger',parent_device=Gollum_card_5,connection='port0/line1')
DigitalOut(name='D4_3_Nuvu_trigger',parent_device=Gollum_card_5,connection='port0/line2')
DigitalOut(name='D4_5_free',parent_device=Gollum_card_5,connection='port0/line4')
DigitalOut(name='D4_6_Synth_switch',parent_device=Gollum_card_5,connection='port0/line5')
DigitalOut(name='D4_8_small_slower_switch',parent_device=Gollum_card_5,connection='port0/line7')
DigitalOut(name='D4_7_external_trig',parent_device=Gollum_card_5,connection='port0/line6')
DigitalOut(name='D4_4_free',parent_device=Gollum_card_5,connection='port0/line3')

#analog channels
AnalogOut(name='A3_1_broken',parent_device=Gollum_card_5,connection='ao0')
AnalogOut(name='A3_2_Offset_Y',parent_device=Gollum_card_5,connection='ao1')
AnalogOut(name='A3_3_Offset_Z',parent_device=Gollum_card_5,connection='ao2')
AnalogOut(name='A3_4_comp_coil_cur',parent_device=Gollum_card_5,connection='ao3')
AnalogOut(name='A3_5_small_slower_cur',parent_device=Gollum_card_5,connection='ao4')
AnalogOut(name='A3_6_Big_slower_cur',parent_device=Gollum_card_5,connection='ao5')
AnalogOut(name='A3_7_ODT1_Setpoint',parent_device=Gollum_card_5,connection='ao6')
AnalogOut(name='A3_8_ODT2_Setpoint',parent_device=Gollum_card_5,connection='ao7')


#CARD 2 (Gandalf)  : This is a 6254 card. All the channels out of this card are defined below.
#digital channels

Shutter(name='D3_1_Sirah_shutter',parent_device=Gandalf_card_2,connection='port0/line0')
DigitalOut(name='D3_2_Home_AOM_switch',parent_device=Gandalf_card_2,connection='port0/line1')
DigitalOut(name='D3_3_RSD_Y_fast',parent_device=Gandalf_card_2,connection='port0/line2')
DigitalOut(name='D3_4_SSODT2_AOM',parent_device=Gandalf_card_2,connection='port0/line3')
DigitalOut(name='D3_5_sirah_lattice_AOM_switch',parent_device=Gandalf_card_2,connection='port0/line4')
Shutter(name='D3_6_sirah_lattice_shutter',parent_device=Gandalf_card_2,connection='port0/line5')
DigitalOut(name='D3_7_chiller_trigger',parent_device=Gandalf_card_2,connection='port0/line6')
DigitalOut(name='D3_8_passbank_trigger',parent_device=Gandalf_card_2,connection='port0/line7')
DigitalOut(name='D3_9_Li_slower_AOM_switch',parent_device=Gandalf_card_2,connection='port0/line8')
DigitalOut(name='D3_10_Li_repumper_AOM_switch',parent_device=Gandalf_card_2,connection='port0/line9')
DigitalOut(name='D3_11_Li_umpump_repumper_AOM_switch',parent_device=Gandalf_card_2,connection='port0/line10')
DigitalOut(name='D3_12_Li_MOT_AOM_switch',parent_device=Gandalf_card_2,connection='port0/line11')
DigitalOut(name='D3_13_Li_imaging_AOM_switch',parent_device=Gandalf_card_2,connection='port0/line12')
Shutter(name='D3_14_Li_imaging_shutter',parent_device=Gandalf_card_2,connection='port0/line13')
Shutter(name='D3_15_Li_MOT_shutter',parent_device=Gandalf_card_2,connection='port0/line14')
DigitalOut(name='D3_16_Li_umpump_AOM_switch',parent_device=Gandalf_card_2,connection='port0/line15')
DigitalOut(name='D3_17_dimple_AOM_switch',parent_device=Gandalf_card_2,connection='port0/line16')
DigitalOut(name='D3_18_waveguide_AOM_switch',parent_device=Gandalf_card_2,connection='port0/line17')
DigitalOut(name='D3_19_Bfield_sample',parent_device=Gandalf_card_2,connection='port0/line18')
Shutter(name='D3_20_atomic_beam_shutter',parent_device=Gandalf_card_2,connection='port0/line19')
DigitalOut(name='D3_21_broken',parent_device=Gandalf_card_2,connection='port0/line20')
DigitalOut(name='D3_22_not_in_use',parent_device=Gandalf_card_2,connection='port0/line21')
DigitalOut(name='D3_23_arduino_reset',parent_device=Gandalf_card_2,connection='port0/line22')
DigitalOut(name='D3_24_not_in_use',parent_device=Gandalf_card_2,connection='port0/line23')
DigitalOut(name='D3_25_MOT_IGBT',parent_device=Gandalf_card_2,connection='port0/line24')
DigitalOut(name='D3_26_DDS_trigger',parent_device=Gandalf_card_2,connection='port0/line25')
DigitalOut(name='D3_29_FT_HH_IGBT',parent_device=Gandalf_card_2,connection='port0/line28')
DigitalOut(name='D3_30_bias_IGBT',parent_device=Gandalf_card_2,connection='port0/line29')
DigitalOut(name='D3_31_curvture_IGBT',parent_device=Gandalf_card_2,connection='port0/line30')
DigitalOut(name='D3_32_MW_trigger',parent_device=Gandalf_card_2,connection='port0/line31')

#make the connection to the MOT mako
MakoCamera('mako',Gollum_card_5,'port0/line0',18517)
#the connection table ends here

#here we write the ramps onto the arduino

DDS_string = 'Rt'+ str(int(dt_MWclean)) + 'f' + str(int(MWclean_start)) + 'F' + str(int(MWclean_stop))+\
'Rt'+ str(int(dt_RFcool1)) + 'f' + str(int(RFcool1_start)) + 'F' + str(int(RFcool1_stop))+\
'Rt'+ str(int(dt_RFcool2)) + 'f' + str(int(RFcool2_start)) + 'F' + str(int(RFcool2_stop))+\
'Rt' + str(int(dt_MW_transfer*1e6))+'f'+ str(int(MW_F2F1_center-MW_F2F1_halfrange)) + 'F' + str(int(MW_F2F1_center+MW_F2F1_halfrange))

ramp = str.encode(DDS_string)
arduino.add_start_command(b'r' +ramp + b'z' )
arduino.add_stop_command(b'The shot is over\r\n')
#------------------------------------------------------------------
#this is to communicate with SynthHD, for Rabi pulses

Rabi_pulse = str.encode(str(float(Rabi_F2F1_freq)))
Pulse_amp = str.encode(str(Rabi_amp))
synth.add_start_command(b'C0') #selects the channel to output RF
synth.add_start_command(b'c0') #don't sweep continuous
synth.add_start_command(b'W'+Pulse_amp)
synth.add_start_command(b'f'+Rabi_pulse)

#lets import all the functions we need------------------------------------------------------------------------------------------
from NaLiExpClass import ExperimentClass
Experiment = ExperimentClass()
#here ends the importing--------------------------------------------------------------------------------------------------------


