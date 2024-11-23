import numpy as np
import json

from SimNDT.core.scenario import Scenario
from SimNDT.core.material import Material
from SimNDT.core.boundary import Boundary
from SimNDT.core.geometryObjects import Ellipse, Circle, Inclusions, Rectangle, Square
from SimNDT.core.geometryObjects import Concrete2Phase, Concrete2PhaseImmersion, Concrete3Phase, Concrete3PhaseImmersion
from SimNDT.core.inspectionMethods import Source, LinearScan, Transmission, PulseEcho, Tomography
from SimNDT.core.signal import Signals
from SimNDT.core.receivers import Receivers
from SimNDT.core.transducer import Transducer
from SimNDT.core.simulation import Simulation
import SimNDT.core.checkSimulation as CheckSim
from SimNDT.core.simPack import SimPack
from SimNDT.gui.engineController import EngineController
from SimNDT.gui import HelperMethods
import scipy.io
import SimNDT.engine.infoCL as infoCL
import pyopencl as cl



"""
1. create a josn file with the simulation parameters.
2. read the json file and return the dictionary of simulation parameters
3. pass these simulation parameters to the appropriate classes.

"""



# def read_sim_parameters(json_file_path):
#     with open(json_file_path, 'r') as json_file:
#         sim_parameters = json.load(json_file)
#     return sim_parameters  # dictionary of simulation parameters      

# Load the .mat file

# filename = r"C:\Users\Kumar\Downloads\test.mat"
mat_filename = r"C:\Users\Kumar\Nextcloud\Work\GUW\sim_ndt\batch_processing_simulator\saved simulations\test_opencl_gpu.mat" 
# mat_data = scipy.io.loadmat(mat_filename)

def read_scenario(sim_params, SimNDT_geom_objects, SimNDT_Bc_objs):
    if "Scenario" in sim_params.keys():
        scena_width = sim_params["Scenario"]["Width"]
        scena_height = sim_params["Scenario"]["Height"]
        scena_pixel_mm = sim_params["Scenario"]["Pixel_mm"]
        scena_label = sim_params["Scenario"]["Label"]
        
        SimNDT_Scenario = Scenario(Width=scena_width, Height=scena_height, Pixel_mm=scena_pixel_mm, Label=scena_label)
        # adding the geometric objects to the scenario
        for geom_num in range(len(SimNDT_geom_objects)):
            SimNDT_Scenario.addObject(SimNDT_geom_objects[geom_num])   
             
        SimNDT_Scenario.createBoundaries(SimNDT_Bc_objs)
        
    print("Finished reading Scenario...\n")
    print(repr(SimNDT_Scenario))
    print("\n")
    return SimNDT_Scenario

def read_geometry_objects(sim_params):
    # geometric objects
    # geometric objects
    if "GeometricObjects" in sim_params.keys():
        print("Showing {} GeometricObjects.\n".format(len(sim_params["GeometricObjects"])))
        SimNDT_geom_objects = []
        for geom_num in range(len(sim_params["GeometricObjects"])):
            geom_name = sim_params["GeometricObjects"][geom_num]["Name"]
            
            if geom_name == "ellipse":
                geom_x0 = sim_params["GeometricObjects"][geom_num]["x0"]
                geom_y0 = sim_params["GeometricObjects"][geom_num]["y0"]
                geom_a = sim_params["GeometricObjects"][geom_num]["a"]
                geom_b = sim_params["GeometricObjects"][geom_num]["b"]
                geom_theta = sim_params["GeometricObjects"][geom_num]["theta"]
                geom_label = sim_params["GeometricObjects"][geom_num]["Label"]
                
                geom_obj = Ellipse(x0=geom_x0, y0=geom_y0, a=geom_a, b=geom_b, theta=geom_theta, Label=geom_label)
                SimNDT_geom_objects.append(geom_obj)
            elif geom_name == "circle":
                geom_x0 = sim_params["GeometricObjects"][geom_num]["x0"]
                geom_y0 = sim_params["GeometricObjects"][geom_num]["y0"]
                geom_r = sim_params["GeometricObjects"][geom_num]["r"]
                geom_label = sim_params["GeometricObjects"][geom_num]["Label"]
                
                geom_obj = Circle(x0=geom_x0, y0=geom_y0, r=geom_r, Label=geom_label)
                SimNDT_geom_objects.append(geom_obj)
            elif geom_name == "rectangle":
                geom_x0 = sim_params["GeometricObjects"][geom_num]["x0"]
                geom_y0 = sim_params["GeometricObjects"][geom_num]["y0"]
                geom_w = sim_params["GeometricObjects"][geom_num]["W"]
                geom_h = sim_params["GeometricObjects"][geom_num]["H"]
                geom_theta = sim_params["GeometricObjects"][geom_num]["theta"]
                geom_label = sim_params["GeometricObjects"][geom_num]["Label"]
                
                geom_obj = Rectangle(x0=geom_x0, y0=geom_y0, W=geom_w, H=geom_h, theta=geom_theta, Label=geom_label)
                SimNDT_geom_objects.append(geom_obj)
            elif geom_name == "square":
                geom_x0 = sim_params["GeometricObjects"][geom_num]["x0"]
                geom_y0 = sim_params["GeometricObjects"][geom_num]["y0"]
                geom_l = sim_params["GeometricObjects"][geom_num]["L"]
                geom_theta = sim_params["GeometricObjects"][geom_num]["theta"]
                geom_label = sim_params["GeometricObjects"][geom_num]["Label"]
                
                geom_obj = Square(x0=geom_x0, y0=geom_y0, L=geom_l, theta=geom_theta, Label=geom_label)
                SimNDT_geom_objects.append(geom_obj)
            elif geom_name == "inclusion":
                geom_diameter = sim_params["GeometricObjects"][geom_num]["Diameter"]
                geom_fraction = sim_params["GeometricObjects"][geom_num]["Fraction"]
                geom_label = sim_params["GeometricObjects"][geom_num]["Label"]
                
                geom_obj = Inclusions(Diameter=geom_diameter, Fraction=geom_fraction, Label=geom_label)
                SimNDT_geom_objects.append(geom_obj)
            # print(geom_obj)
            print("\n")
        print("Finished reading GeometricObjects...\n")
        # print(repr(SimNDT_geom_objects))
        print("\n")
        return SimNDT_geom_objects

def read_materials(sim_params):
        # reading materials ######### 
    if "Materials" in sim_params.keys():
        print("Showing {} Materials.\n".format(len(sim_params["Materials"])))
        SimNDT_Mat_objs = []
        for mat_num in range(len(sim_params["Materials"])):
            mat_name = sim_params["Materials"][mat_num]["Name"]
            mat_rho = sim_params["Materials"][mat_num]["Rho"]
            mat_c11 = sim_params["Materials"][mat_num]["C11"]
            mat_c12 = sim_params["Materials"][mat_num]["C12"]
            mat_c22 = sim_params["Materials"][mat_num]["C22"]
            mat_c44 = sim_params["Materials"][mat_num]["C44"]
            mat_vl = np.sqrt(mat_c11 / mat_rho)
            mat_vt = np.sqrt(mat_c44 / mat_rho)
            mat_label = sim_params["Materials"][mat_num]["Label"]
            mat_eta_v = sim_params["Materials"][mat_num]["Eta_v"]
            mat_eta_s = sim_params["Materials"][mat_num]["Eta_s"]
            mat_damping = sim_params["Materials"][mat_num]["Damping"]
            
            mat_obj = Material(mat_name, mat_rho, mat_c11, mat_c12, mat_c22, mat_c44, mat_label, mat_damping, mat_eta_v, mat_eta_s)
            
            # print(materials["material_label_{}".format(mat_label)])
            SimNDT_Mat_objs.append(mat_obj)
            # print(mat_obj)
            
            print("\n")
            
        print("Finished reading Materials...\n")
        # print(repr(materials))
        print("\n")
        return SimNDT_Mat_objs

def read_boundaries(sim_params):
        # boundary conditions
    if "Boundaries" in sim_params.keys():    
        print("Reading {} Boundaries.\n".format(len(sim_params["Boundaries"])))
        SimNDT_Bc_objs = []
        for bc_num in range(len(sim_params["Boundaries"])):
            bc_name = sim_params["Boundaries"][bc_num]["Name"]
            bc_size = sim_params["Boundaries"][bc_num]["Size"]
            bc_type = sim_params["Boundaries"][bc_num]["Type"]
            
            bc_obj = Boundary(bc_name, bc_type, bc_size)
            SimNDT_Bc_objs.append(bc_obj)
            # print(bc_obj)
            print("\n")
        print("Finished reading Boundaries...\n")
        # print(repr(bc))
        print("\n")
        return SimNDT_Bc_objs

def read_transducers(sim_params):
        # transducers 
    if "Transducers" in sim_params.keys():
        SimNDT_Transd_objs = []
        trans_name = sim_params["Transducers"]["Name"]
        trans_size = sim_params["Transducers"]["Size"]
        trans_center_offset = sim_params["Transducers"]["CenterOffset"]
        trans_border_offset = sim_params["Transducers"]["BorderOffset"]
        trans_size_pixel = sim_params["Transducers"]["SizePixel"]
        trans_location = sim_params["Transducers"]["Location"]
        trans_point_source = sim_params["Transducers"]["PointSource"]
        trans_window = sim_params["Transducers"]["Window"]
        trans_field = sim_params["Transducers"]["Field"]
        trans_pzt = sim_params["Transducers"]["PZT"]

        
        SimNDT_Transducers = Transducer(
                                        name=trans_name,
                                        Size=trans_size,
                                        CenterOffset=trans_center_offset,
                                        BorderOffset=trans_border_offset,
                                        Location=trans_location,
                                        PointSource=trans_point_source,
                                        EnableWindow=trans_window,
                                        Field=trans_field,
                                        PZT=trans_pzt
                                        )
        SimNDT_Transd_objs.append(SimNDT_Transducers)
        print("Finished reading Transducers...\n")
        print(repr(SimNDT_Transd_objs))
        print("\n")
        return SimNDT_Transd_objs

def check_transducer_size(Scenario, Transducer):
    
    for trans_num in range(len(Transducer)):
        trans = Transducer[trans_num]
        
        if trans.Size >= Scenario.Width:
            raise ValueError("Transducer is larger than Scenario Width!!!!")
                
        elif trans.Size <= 0 and not trans.PointSource:
            raise ValueError("Incorrect Transducer Size!!!!")
            
        if (np.abs(trans.CenterOffset) + trans.Size / 2.0 >= Scenario.Width / 2.0):
            raise ValueError("Transducer is out of Scenario!!!!")
        
        if trans.BorderOffset < 0 or trans.BorderOffset >= Scenario.Height:
            raise ValueError("Transducer is out of Scenario!!!!")
    
def read_inspection(sim_params):
        # setting up the inspection method
    
    if "Inspection" in sim_params.keys():
        
        insp_name = sim_params["Inspection"]["Name"]
        if insp_name == "Transmission":
            insp_location = sim_params["Inspection"]["Location"]
            
            SimNDT_Inspection = Transmission(Location=insp_location)
        
        elif insp_name == "PulseEcho":
            insp_location = sim_params["Inspection"]["Location"]
            
            SimNDT_Inspection = PulseEcho(Location=insp_location)
        
        elif insp_name == "LinearScan":
            insp_ini = sim_params["Inspection"]["ini"]
            insp_end = sim_params["Inspection"]["end"]
            insp_step = sim_params["Inspection"]["step"]
            insp_location = sim_params["Inspection"]["Location"]
            insp_method = sim_params["Inspection"]["Method"]
            insp_theta = sim_params["Inspection"]["Theta"]
            
            SimNDT_Inspection = LinearScan(ini=insp_ini, end=insp_end, step=insp_step, Location=insp_location, Method=insp_method, Theta=insp_theta)
        
        elif insp_name == "Tomography":
            insp_projection_step = sim_params["Inspection"]["ProjectionStep"]
            insp_diameter_ring = sim_params["Inspection"]["DiameterRing"]
            insp_one_projection = sim_params["Inspection"]["OneProjection"]
            
            SimNDT_Inspection = Tomography(ProjectionStep=insp_projection_step, DiameterRing=insp_diameter_ring, OneProjection=insp_one_projection)
        print("Finished reading Inspection...\n")
        print(repr(SimNDT_Inspection))
        print("\n")
        return SimNDT_Inspection
    
def read_source(sim_params):
        # setting up the source
    
    if "Source" in sim_params.keys():
        source_longitudinal = sim_params["Source"]["Longitudinal"]
        source_shear = sim_params["Source"]["Shear"]
        source_pressure = sim_params["Source"]["Pressure"]
        source_displacement = sim_params["Source"]["Displacement"]
        source_hide_receiver = 0
        
        # check if Source attributes should be changed by passins as arguments
        SimNDT_Source = Source()
        print("Finished reading Source...\n")
        print(repr(SimNDT_Source))
        print("\n")
        return SimNDT_Source

def read_signal(sim_params):
        # setting up the signal
      
    if "Signal" in sim_params.keys():
        signal_name = sim_params["Signal"]["Name"]
        signal_amplitude = sim_params["Signal"]["Amplitude"]
        signal_frequency = sim_params["Signal"]["Frequency"]
        signal_n_cycles = sim_params["Signal"]["N_Cycles"]
        
        SimNDT_Signal = Signals(Name=signal_name, Amplitud=signal_amplitude, Frequency=signal_frequency, N_Cycles=signal_n_cycles)  
        print("Finished reading Signal...\n")
        print(repr(SimNDT_Signal))
        print("\n")
        return SimNDT_Signal
    
def read_simulation(sim_params):
        # setting up the simulation
    
    if "Simulation" in sim_params.keys():
        sim_time_scale = sim_params["Simulation"]["TimeScale"]
        sim_max_freq = sim_params["Simulation"]["MaxFreq"]
        sim_point_cycle = sim_params["Simulation"]["PointCycle"]
        sim_simulation_time = sim_params["Simulation"]["SimulationTime"]
        sim_order = sim_params["Simulation"]["Order"]
        # sim_device = sim_params["Simulation"]["Device"]
        
        SimNDT_Simulation = Simulation(TimeScale=sim_time_scale, MaxFreq=sim_max_freq, PointCycle=sim_point_cycle, SimTime=sim_simulation_time, Order=sim_order)
        
        
        print("Finished reading Simulation...\n")
        print(repr(SimNDT_Simulation))
        print("\n")
        return SimNDT_Simulation

def read_receivers(sim_params):
    
    # setting up the receivers
    
    if "Receivers" in sim_params.keys():
        receiver_method = sim_params["Receivers"]["Method"]
        SimNDT_Receivers = Receivers(method=receiver_method)
        print("Finished reading Receivers...\n")
        print(repr(SimNDT_Receivers))
        print("\n")
        return SimNDT_Receivers
    
def SingleLaunchSetup(SimNDT_Scenario, SimNDT_Source, SimNDT_Inspection, SimNDT_Transd_objs, SimNDT_Signal):
    """
    Sets up the single launch inspection for the simulation by performing the following steps:
    1. Calculates XL and YL for the inspection based on the scenario and transducer.
    2. Sets up and checks the signal values, ensuring they are within valid ranges.
    
    Parameters:
    - SimNDT_Scenario: The simulation scenario object containing scenario details.
    - SimNDT_Source: The source object for the simulation.
    - SimNDT_Inspection: The inspection object for the simulation.
    - SimNDT_Transd_objs: The list of transducer objects for the simulation.
    - SimNDT_Signal: The signal object for the simulation.
    
    Raises:
    - ValueError: If the signal frequency is not within valid ranges or if the signal type is not implemented.
    """
    
    # calculating XL, YL for inspection
    SimNDT_Inspection.XL, SimNDT_Inspection.YL = SimNDT_Inspection.view(SimNDT_Scenario.M, SimNDT_Scenario.N, SimNDT_Scenario.Pixel_mm, SimNDT_Inspection.Theta, SimNDT_Transd_objs[0])
    
    # setting up signal
    # checking signal values
    if SimNDT_Signal.Name == "RaisedCosine":
        if SimNDT_Signal.Frequency > 1e9:
            raise ValueError("Give correctly the Frequency (MHz)")
        cycles = 1
    else:
        ValueError("Implement signal check for gaussian sine.")
        

def SimulationSetup(Scenario, SimNDT_Mat_objs, SimNDT_Transd_objs, Simulation):
    """
    This function sets up the simulation environment by performing the following steps:
    1. Checks if the boundary conditions are defined in the scenario.
    2. Sets up the platform and device for the simulation, using OpenCL if available.
    3. Calculates the time step (dt) and spatial step (dx) for the simulation based on the materials and transducers.
    4. Creates the numerical model for the simulation, including Tapgrid, Rgrid, MRI, NRI, Im, and Mp.
    """
    
    if np.size(Scenario.Iabs) == 1:
            ValueError("Please define the Boundaries Conditions!!!!")
    # setting up the platform and device
    if infoCL.importCL():
        Platforms = infoCL.getPlatforms()
    else:
        Platforms = None
        
    if Platforms is not None:
        PlatformAndDevices = infoCL.getPlatformsAndDevices()    
        for PlatformAndDevice in PlatformAndDevices:
            Simulation.Platform = PlatformAndDevice[0].name
            Simulation.Device = cl.device_type.to_string(PlatformAndDevice[1].type)
    else:
        Simulation.Platform = "Serial"
        Simulation.Device = "CPU"
        
    # calculating dt, dx in simaulation
    Simulation.job_parameters(SimNDT_Mat_objs, SimNDT_Transd_objs[0])

    # calculating the numerical model (Tapgrid, Rgrid, MRI, NRI, Im, Mp )
    Simulation.create_numericalModel(Scenario)

def checkSimulation(Scenario, Materials, Boundaries, Transducers, Inspection, Signal, Simulation):
    """
    This function performs a series of checks to ensure that the simulation setup is correct and ready to run. 
    It checks the following:
    
    1. Material Labels: Ensures that the number of labels in the scenario matches the number of defined materials, 
       and that there are no repeated labels in the materials.
    2. Boundaries: Ensures that the boundaries are correctly defined and reloads them if necessary.
    3. Transducers: Sets the inspection on the numerical model.
    4. Signal: Generates the signal and ensures it fits within the simulation time.
    
    Parameters:
    - Scenario: The simulation scenario object containing scenario details.
    - Materials: The list of material objects for the simulation.
    - Boundaries: The list of boundary objects for the simulation.
    - Transducers: The list of transducer objects for the simulation.
    - Inspection: The inspection object for the simulation.
    - Signal: The signal object for the simulation.
    - Simulation: The simulation object containing simulation parameters.
    
    Raises:
    - ValueError: If any of the checks fail, a ValueError is raised with an appropriate error message.
    """
    # material label check
    case = CheckSim.labels(Scenario, Materials)

    if case == 1:
        ValueError("Number of labels in scenario is higher than the number of the defined materials. ")
    elif case == 2:
        ValueError("Number of labels in scenario is lower than the number of the defined materials. ")
    
    case = CheckSim.materials(Materials)
    if case == 1:
        raise ValueError("Repeated labels in Materials!!!.")
    print("Materials checked.")

    case = CheckSim.isLabelsEquals(Scenario, Materials)
    if case == 1:
        raise ValueError("Scenario Labels do not coincide with Material Labels!!!.")
    print("Labels checked.")

    # checking boundaries
    Scenario, Boundaries, isChange = CheckSim.boundariesReLoad(Scenario, Materials, Boundaries, Transducers[0], Inspection, Simulation)

    if isChange:
        Boundaries = Boundaries
        Scenario = Scenario
    print("Found error, but fixed: All boundaries with Air Layers")
    print("Boundaries checked.")

    # checking transducers
    # Resetting XL, YL, IR using x2, y2 (not sure why this is done! what are x2, y2?)
    Inspection.setInspection(Scenario, Transducers[0], Simulation)
    print("Inspection set.")

    # checking signal
    t = Simulation.t
    try:
        source = Signal.generate(t)
    except Exception as e:
        raise ValueError("Signal does not fit in the Simulation Time, Increase the Simulation Time to solve this issue")
    print("Signal generated.")

    # If no valueerror is raised, then the simulation is ready to run
    print("Simulation is ready to run!!!") 

# def runSimulation(self):
    
#     RunSimulation(self.filename, self.SimNDT_Simulation)
#     if dlg.basename is not None:
#         self.SimNDT_SnapShots = SnapShots(True, Step=step, Filename = dlg.basename, dB = DB, 
#                                             Color = color,
#                                             Field = field, 
#                                             enableFields=isEnableFields,
#                                             enableSignals=isEnableSignals,
#                                             enableImages=isEnableImages,
#                                             enableNumPy=isEnableNumPy,
#                                             enableVolume=isEnableVolume,
#                                             enableView=isView,
#                                             sensorShape = sensorShape,
#                                             sensorPlacement = sensorPlacement,
#                                             sensorSize = sensorSize )
#     else:
#         self.SimNDT_SnapShots = SnapShots(dB = DB,
#                                             enableFields=isEnableFields,
#                                             enableSignals=isEnableSignals,
#                                             enableImages=isEnableImages,
#                                             enableNumPy=isEnableNumPy,
#                                             enableVolume=isEnableVolume,
#                                             enableView=isView)


def openSim(sim_params):
    
    SimNDT_Scenario = None
    SimNDT_Mat_objs = None
    SimNDT_Bc_objs = None
    SimNDT_Transd_objs = None
    SimNDT_geom_objects = None
    SimNDT_Inspection = None
    SimNDT_Source = None
    SimNDT_Signal = None
    SimNDT_Simulation = None
    SimNDT_Receivers = None
    
    # reading geometric objects
    SimNDT_geom_objects = read_geometry_objects(sim_params)
    SimNDT_Mat_objs = read_materials(sim_params)
    SimNDT_Bc_objs = read_boundaries(sim_params)
    SimNDT_Scenario = read_scenario(sim_params, SimNDT_geom_objects, SimNDT_Bc_objs)

    SimNDT_Source = read_source(sim_params)
    SimNDT_Signal = read_signal(sim_params)
    SimNDT_Transd_objs = read_transducers(sim_params)
    check_transducer_size(SimNDT_Scenario, SimNDT_Transd_objs)
    
    SimNDT_Signal = read_signal(sim_params)
    
    SimNDT_Inspection = read_inspection(sim_params)
    if SimNDT_Inspection.Name == "Transmission":
        SingleLaunchSetup(SimNDT_Scenario, SimNDT_Source, SimNDT_Inspection, SimNDT_Transd_objs, SimNDT_Signal)
    
    SimNDT_Simulation = read_simulation(sim_params)
    # sets up simulation env
    SimulationSetup(SimNDT_Scenario, SimNDT_Mat_objs, SimNDT_Transd_objs, SimNDT_Simulation)  
    # checking labels, setting inspection and fixing boundary if necessary 
    checkSimulation(SimNDT_Scenario, SimNDT_Mat_objs, SimNDT_Bc_objs, SimNDT_Transd_objs, SimNDT_Inspection, SimNDT_Signal, SimNDT_Simulation)
    
    
    SimNDT_Receivers = read_receivers(sim_params)
        
    print("Finished reading all parameters...\n")

    return SimNDT_Scenario, SimNDT_Mat_objs, SimNDT_Bc_objs, SimNDT_Transd_objs, SimNDT_geom_objects, SimNDT_Inspection, SimNDT_Source, SimNDT_Signal, SimNDT_Simulation, SimNDT_Receivers


def openSim_mat_file():
    
        data2load = {}
        data2load = scipy.io.loadmat(mat_filename, squeeze_me=True, struct_as_record=False)


        if "Scenario" in data2load:
            Width = getattr(data2load["Scenario"], 'Width')
            Height = getattr(data2load["Scenario"], 'Height')
            Pixel_mm = getattr(data2load["Scenario"], 'Pixel_mm')
            Label = getattr(data2load["Scenario"], 'Label')
            SimNDT_Scenario = Scenario(Width=Width, Height=Height, Pixel_mm=Pixel_mm, Label=Label)
            SimNDT_Scenario = HelperMethods.mat2Obj(data2load["Scenario"], SimNDT_Scenario)

        SimNDT_Materials = HelperMethods.loadDataFromList(data2load, 'Materials', Material())
        SimNDT_Boundaries = HelperMethods.loadDataFromList(data2load, "Boundaries", Boundary())
        SimNDT_Transducers = HelperMethods.loadDataFromList(data2load, "Transducers", Transducer())

        geoLabels = ["ellipse", "circle", "square", "rectangle"]
        geoObjects = [Ellipse(), Circle(), Square(), Rectangle()]
        SimNDT_ObjectList = HelperMethods.loadDataFromListWithLabels(data2load, 'GeometricObjects', geoLabels,
                                                                          geoObjects)

        ConcreteLabels = ["Concrete2Phase", "Concrete2PhaseImmersion", "Concrete3Phase", "Concrete3PhaseImmersion"]
        ConcreteObjects = [Concrete2Phase(), Concrete2PhaseImmersion(), Concrete3Phase(), Concrete3PhaseImmersion()]

        if "ConcreteMicrostructure" in data2load:
            SimNDT_ConcreteMicrostructure = HelperMethods.loadDataWithLabels(data2load, 'ConcreteMicrostructure',
                                                                                  ConcreteLabels, ConcreteObjects)
        if "Simulation" in data2load:
            SimNDT_Simulation = HelperMethods.mat2Obj(data2load["Simulation"], Simulation())
            
        if "Inspection" in data2load:
            inspLabels = ['Transmission', 'PulseEcho', 'LinearScan', 'Tomography']
            inspObjects = [Transmission(), PulseEcho(), LinearScan(), Tomography()]
            SimNDT_Inspection = HelperMethods.loadDataWithLabels(data2load, "Inspection", inspLabels, inspObjects)
            SimNDT_Inspection.setInspection(SimNDT_Scenario, SimNDT_Transducers[0], SimNDT_Simulation)
            
        if "Source" in data2load:
            SimNDT_Source = HelperMethods.mat2Obj(data2load["Source"], Source())

        if "Signal" in data2load:
            SimNDT_Signal = HelperMethods.mat2Obj(data2load["Signal"], Signals())

        

        if "Receivers" in data2load:
            SimNDT_Receivers = HelperMethods.mat2Obj(data2load["Receivers"], Receivers())
    
        return SimNDT_Scenario, SimNDT_Materials, SimNDT_Boundaries, SimNDT_Transducers, SimNDT_ObjectList, SimNDT_Inspection, SimNDT_Source, SimNDT_Signal, SimNDT_Simulation, SimNDT_Receivers

def runEngine(SimNDT_Scenario, SimNDT_Materials, SimNDT_Boundaries,\
                    SimNDT_Inspection, SimNDT_Source, SimNDT_Transducers, \
                    SimNDT_Signal, SimNDT_Simulation):
    
    simPack = SimPack(SimNDT_Scenario, SimNDT_Materials, \
                        SimNDT_Boundaries, SimNDT_Inspection, SimNDT_Source, \
                        SimNDT_Transducers, SimNDT_Signal, SimNDT_Simulation)

    engine = EngineController(simPack)


    state = engine.run()

    if state == "Stop":
        print("Stop by User!!!!!")
    else:
        print("Simulation Done.")

    # SimNDT_Receivers = Receivers(self.SimNDT_Inspection.Name)
    # SimNDT_Receivers.setReceivers(engine)
