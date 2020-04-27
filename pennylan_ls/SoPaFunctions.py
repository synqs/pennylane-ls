def prepare_initial(self):
    #### Initial Preparation ####
    FREQ_3D.constant(self.t, value=threeDFreq)
    FREQ_2D.constant(self.t, value=twoDFreq)
    FREQ_Push.constant(self.t, value=pushFreq)

    INT_3D.constant(self.t, value=threeDInt)
    INT_2D.constant(self.t, value=twoDInt)
    INT_Push.constant(self.t, value=pushInt)

    AOM_2D.go_high(self.t)  ##AOM 2DMOT OFF
    AOM_3D.go_high(self.t)  ##AOM 3DMOT OFF
    AOM_Push.go_high(self.t)  ##AOM push/imaging beam OFF
    self.t += 1e-3

def take_reference(self):
    #### Take background image ####
    AOM_3D.go_low(self.t)##AOM 3DMOT ON
    Shutter_3D.go_high(self.t)##Shutter 3DMOT open
    self.t+=100e-3
    mako.expose(self.t,'fake1', trigger_duration=Cam_EXPOT)##take image of MOT beams: background
    self.t+=0.2

def load_MOT(self,MOT_loading_time):
    #### MOT loading ####
    AOM_2D.go_low(self.t)##AOM 2DMOT ON
    AOM_Push.go_low(self.t)##AOM push/imaging beam ON
    Shutter_Push.go_high(self.t) ##Shutter push beam open
    self.t+=100e-3
    if use_MOT:
        IGBT.go_high(self.t)##MOT coils ON
    self.t+=MOT_loading_time
    AOM_Push.go_high(self.t)##AOM push/imaging beam OFF
    Shutter_Push.go_low(self.t)##Shutter push beam close
    AOM_2D.go_high(self.t)##AOM 2DMOT OFF

def idle(self,Hold_Time):
    self.t+=Hold_Time

def meas(self):
    AOM_3D.go_high(self.t)  ##AOM 3DMOT Off
    if use_MOT_fluorescence_imaging:
        FREQ_3D.constant(self.t, value=5.5)
    mako.expose(self.t, 'fake2', trigger_duration=Cam_EXPOT)
    self.t += 10e-6
    AOM_3D.go_low(self.t)
    self.t += Img_Pulse_length
    AOM_3D.go_high(self.t)
    self.t += 0.1

def reset_after(self):
    #### Reset to default ####
    if use_MOT:
        IGBT.go_low(self.t)##MOT coils OFF
    Shutter_Push.go_high(self.t) ##Shutter push beam open
    AOM_2D.go_low(self.t)##AOM 2DMOT ON
    AOM_3D.go_low(self.t)##AOM 3DMOT ON
    FREQ_3D.constant(self.t,value=threeDFreq)
    AOM_Push.go_low(self.t)##AOM push/imaging beam ON
    FREQ_Push.constant(self.t,value=pushFreq)