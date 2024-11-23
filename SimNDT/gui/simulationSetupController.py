__author__ = 'Miguel Molero'

import sys
import numpy as np
from PySide.QtGui import *


from SimNDT.gui.advancedSimulationSetupController import AdvancedSimulationSetup


import SimNDT.engine.infoCL as infoCL



if infoCL.importCL():
    import pyopencl as cl



def calculate_simulation_parameters(Scenario, Materials, Transducers, Simulation):


        timeScale = Simulation.TimeScale
        pointCycle = Simulation.PointCycle
        MaxFreq = Simulation.MaxFreq
        SimTime = Simulation.SimulationTime
        dx_user = None
        dt_user = None

        if np.size(Scenario.Iabs) == 1:
            print("Please define the Boundaries Conditions!!!!")
           
        if infoCL.importCL():
            Platforms = infoCL.getPlatforms()
        else:
            Platforms = None
            print("Platform = CPU [Serial Processing]..")
            

        if Platforms is not None:
           PlatformAndDevices = infoCL.getPlatformsAndDevices()
           print("Here is platform and devices...", PlatformAndDevices)

        info = [cl.device_type.to_string(device.type) + ": " + device.name + " OpenCL Platform: " + platform.name
                    for platform, device in PlatformAndDevices]
        print(info)



        # dlg = AdvancedSimulationSetup(SimTime, MaxFreq,
        #                               Scenario, Materials, Transducers, Simulation)
    

        

        Simulation.job_parameters(Materials, Transducers[0])


        Simulation.create_numericalModel(Scenario)

        if dx_user is not None or dt_user is not None:
            Simulation.jobByUser(dx_user, dt_user)
            Simulation.create_numericalModel(Scenario)

        if Platforms is not None:
            Simulation.setPlatform(PlatformAndDevices[0].name)
            Simulation.setDevice(cl.device_type.to_string(PlatformAndDevices[1].type))
            print(PlatformAndDevices[0].name, cl.device_type.to_string(PlatformAndDevices[1].type))
        else:
            Simulation.setPlatform("Serial")
            Simulation.setDevice("CPU")

