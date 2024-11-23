import sys
import numpy as np
# from SimNDT.gui import app
from SimNDT.gui.MainWindow import openSim, openSim_mat_file, runEngine
# from SimNDT.gui.managerDialogsController import runEngine
from define_params_create_json_file import data as sim_params
import pprint

from SimNDT.gui.simulationSetupController import calculate_simulation_parameters
# from SimNDT.gui.managerDialogsController import runEngine
# sys.exit(app.run())


# test delete
# from define_params_create_json_file import data as sim_params
# pprint.pprint(data["Scenario"]["Dimensions"])    
# pprint.pprint(sim_params["Scenario"]["Width"])
# pprint.pprint(sim_params["Materials"][3])
# pprint.pprint(sim_params["Boundaries"][3])
# pprint.pprint(sim_params["GeometricObjects"][3])
# print(data.keys())
# from SimNDT.core.material import Material
# material1 = Material()
# print(material1)
# print(repr(material1))

SimNDT_Scenario, SimNDT_Mat_objs, SimNDT_Bc_objs, SimNDT_Transd_objs, SimNDT_geom_objects, \
SimNDT_Inspection, SimNDT_Source, SimNDT_Signal, SimNDT_Simulation, SimNDT_Receivers = \
    openSim(sim_params)
    
# SimNDT_Scenario_mat, SimNDT_Mat_objs_mat, SimNDT_Bc_objs_mat, SimNDT_Transd_objs_mat, SimNDT_geom_objects_mat, \
# SimNDT_Inspection_mat, SimNDT_Source_mat, SimNDT_Signal_mat, SimNDT_Simulation_mat, SimNDT_Receivers_mat = \
#     openSim_mat_file()

runEngine(SimNDT_Scenario, SimNDT_Mat_objs, SimNDT_Bc_objs,\
                    SimNDT_Inspection, SimNDT_Source, SimNDT_Transd_objs, \
                    SimNDT_Signal, SimNDT_Simulation)

# runEngine(SimNDT_Scenario_mat, SimNDT_Mat_objs_mat, SimNDT_Bc_objs_mat, \
#           SimNDT_Inspection_mat, SimNDT_Source_mat, SimNDT_Transd_objs_mat, \
#           SimNDT_Signal_mat, SimNDT_Simulation_mat)

# print(SimNDT_geom_objects)
# print(SimNDT_Transd_objs)

# SimNDT_Inspection.setInspection(SimNDT_Scenario, SimNDT_Transd_objs[0], SimNDT_Simulation)
# Access the XL attribute
# print(SimNDT_Inspection.YL)
# print(SimNDT_Inspection.Location)
# attributes = dir(SimNDT_Inspection)
# print(SimNDT_Mat_objs[0])

# print(SimNDT_Inspection.XL)
# print(np.unique(SimNDT_Scenario.I))
# print(np.unique(SimNDT_Scenario.Iabs))
# print(np.unique(SimNDT_Scenario.Io))
# print(SimNDT_Scenario)

# calculate_simulation_parameters(SimNDT_Scenario, SimNDT_Mat_objs, SimNDT_Transd_objs, SimNDT_Simulation)

# print(SimNDT_Scenario)