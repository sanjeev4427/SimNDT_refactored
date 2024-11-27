import numpy as np
import json
import scipy.io
import pyopencl as cl

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
import SimNDT.engine.infoCL as infoCL
from SimNDT.run_setup.snapshots import SnapShots
from SimNDT.run_setup.SimulationVideo import create_vector_field_video
from SimNDT.run_setup.engineController import EngineController
from SimNDT.run_setup import HelperMethods



def read_scenario(sim_params, SimNDT_geom_objects, SimNDT_Bc_objs):
    """
    Reads and sets up the scenario based on the provided simulation parameters, geometric objects, and boundary conditions.
    
    Parameters:
    - sim_params: Dictionary containing simulation parameters.
    - SimNDT_geom_objects: List of geometric objects.
    - SimNDT_Bc_objs: List of boundary condition objects.
    
    Returns:
    - SimNDT_Scenario: The scenario object.
    """
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
    # print(repr(SimNDT_Scenario))
    # print("\n")
    return SimNDT_Scenario

def read_geometry_objects(sim_params):
    """
    Reads and sets up geometric objects like ellipses, circles, rectangles, squares, and inclusions from the simulation parameters.
    
    Parameters:
    - sim_params: Dictionary containing simulation parameters.
    
    Returns:
    - SimNDT_geom_objects: List of geometric objects.
    """
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
            # print("\n")
        print("Finished reading GeometricObjects...\n")
        # print(repr(SimNDT_geom_objects))
        # print("\n")
        return SimNDT_geom_objects

def read_materials(sim_params):
    """
    Reads and sets up materials for the simulation. 
    
    Parameters:
    - sim_params: Dictionary containing simulation parameters.
    
    Returns:
    - SimNDT_Mat_objs: List of material objects.
    """
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
            
            # print("\n")
            
        print("Finished reading Materials...\n")
        # print(repr(materials))
        # print("\n")
        return SimNDT_Mat_objs

def read_boundaries(sim_params):
    """
    Reads and sets up boundary conditions for the simulation.
    
    Parameters:
    - sim_params: Dictionary containing simulation parameters.
    
    Returns:
    - SimNDT_Bc_objs: List of boundary condition objects.
    """
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
            # print("\n")
        print("Finished reading Boundaries...\n")
        # print(repr(bc))
        # print("\n")
        return SimNDT_Bc_objs

def read_transducers(sim_params):
    """
    Reads and sets up transducers for the simulation, including properties like size, location, and field.
    
    Parameters:
    - sim_params: Dictionary containing simulation parameters.
    
    Returns:
    - SimNDT_Transd_objs: List of transducer objects.
    """
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
        # print("\n")
        return SimNDT_Transd_objs

def check_transducer_size(Scenario, Transducer):
    """
    Checks if the transducer size is appropriate for the given scenario and raises errors if there are issues.
    
    Parameters:
    - Scenario: The scenario object.
    - Transducer: List of transducer objects.
    
    Raises:
    - ValueError: If the transducer size is inappropriate.
    """
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
    """
    Reads and sets up the inspection method for the simulation, such as Transmission, PulseEcho, LinearScan, or Tomography.
    
    Parameters:
    - sim_params: Dictionary containing simulation parameters.
    
    Returns:
    - SimNDT_Inspection: The inspection object.
    """
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
        # print(repr(SimNDT_Inspection))
        # print("\n")
        return SimNDT_Inspection
    
def read_source(sim_params):
    """
    Reads and sets up the source for the simulation, including properties like longitudinal and shear wave sources.
    
    Parameters:
    - sim_params: Dictionary containing simulation parameters.
    
    Returns:
    - SimNDT_Source: The source object.
    """
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
        # print(repr(SimNDT_Source))
        # print("\n")
        return SimNDT_Source

def read_signal(sim_params):
    """
    Reads and sets up the signal for the simulation, including properties like amplitude, frequency, and number of cycles.
    
    Parameters:
    - sim_params: Dictionary containing simulation parameters.
    
    Returns:
    - SimNDT_Signal: The signal object.
    """
        # setting up the signal
      
    if "Signal" in sim_params.keys():
        signal_name = sim_params["Signal"]["Name"]
        signal_amplitude = sim_params["Signal"]["Amplitude"]
        signal_frequency = sim_params["Signal"]["Frequency"]
        signal_n_cycles = sim_params["Signal"]["N_Cycles"]
        
        SimNDT_Signal = Signals(Name=signal_name, Amplitud=signal_amplitude, Frequency=signal_frequency, N_Cycles=signal_n_cycles)  
        print("Finished reading Signal...\n")
        # print(repr(SimNDT_Signal))
        # print("\n")
        return SimNDT_Signal
    
def read_simulation(sim_params):
    """
    Reads and sets up the simulation parameters, including time scale, 
            maximum frequency, and simulation time.
    
    Parameters:
    - sim_params: Dictionary containing simulation parameters.
    
    Returns:
    - SimNDT_Simulation: The simulation object.
    """
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
        # print(repr(SimNDT_Simulation))
        # print("\n")
        return SimNDT_Simulation

def read_receivers(sim_params):
    """
    Reads and sets up the receivers for the simulation.
    
    Parameters:
    - sim_params: Dictionary containing simulation parameters.
    
    Returns:
    - SimNDT_Receivers: The receivers object.
    """
    
    # setting up the receivers
    
    if "Receivers" in sim_params.keys():
        receiver_method = sim_params["Receivers"]["Method"]
        SimNDT_Receivers = Receivers(method=receiver_method)
        print("Finished reading Receivers...\n")
        # print(repr(SimNDT_Receivers))
        # print("\n")
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
    
    Parameters:
    - Scenario: The scenario object.
    - SimNDT_Mat_objs: List of material objects.
    - SimNDT_Transd_objs: List of transducer objects.
    - Simulation: The simulation object.
    """
    
    if np.size(Scenario.Iabs) == 1:
            ValueError("Please define the Boundaries Conditions!!!!")
    # setting up the platform and device
    if infoCL.importCL():
        Platforms = infoCL.getPlatforms()
        print('Platforms:', Platforms)
    else:
        Platforms = None
        
    if Platforms is not None:
        PlatformAndDevices = infoCL.getPlatformsAndDevices()    
        print('PlatformAndDevices:', PlatformAndDevices)
        
        preferred_platform = None
        preferred_device = None
        
        # First pass: Look for non-Intel GPU
        for PlatformAndDevice in PlatformAndDevices:
            platform_name = PlatformAndDevice[0].name
            device_name = PlatformAndDevice[1].name
            if 'Intel' not in platform_name and 'GPU' in device_name:
                preferred_platform = platform_name
                preferred_device = cl.device_type.to_string(PlatformAndDevice[1].type)
                break
        
        # Second pass: If no non-Intel GPU found, use any available platform
        if preferred_platform is None:
            for PlatformAndDevice in PlatformAndDevices:
                preferred_platform = PlatformAndDevice[0].name
                preferred_device = cl.device_type.to_string(PlatformAndDevice[1].type)
                break
        
        Simulation.Platform = preferred_platform
        Simulation.Device = preferred_device
    else:
        Simulation.Platform = "Serial"
        Simulation.Device = "CPU"
        
    print("Assigned Platform: ", Simulation.Platform)
    print("Assig. Device: ", Simulation.Device)
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

def enableSnapshot(sim_params):
    """
    Enables and sets up snapshots for the simulation, including properties like step size, file path, and fields to save.
    
    Parameters:
    - sim_params: Dictionary containing simulation parameters.
    
    Returns:
    - SimNDT_SnapShots: The snapshots object.
    """
    if "Snapshot" in sim_params.keys():
        step = sim_params["Snapshot"]["Step"]
        save_filepath = sim_params["Snapshot"]["Save_filepath"]
        filename = sim_params["Snapshot"]["Filename"]
        enableFields = sim_params["Snapshot"]["enableFields"]
        enableNumPy = sim_params["Snapshot"]["enableNumPy"]
        extension = sim_params["Snapshot"]["Extension"]
        db = sim_params["Snapshot"]["dB"]
        color = sim_params["Snapshot"]["Color"]
        field = sim_params["Snapshot"]["Field"]
        enableSignals = sim_params["Snapshot"]["enableSignals"]
        enableImages = sim_params["Snapshot"]["enableImages"]
        enableVolume = sim_params["Snapshot"]["enableVolume"]
        enableView = sim_params["Snapshot"]["enableView"]
        sensorShape = sim_params["Snapshot"]["sensorShape"]
        sensorPlacement = sim_params["Snapshot"]["sensorPlacement"]
        sensorSize = sim_params["Snapshot"]["sensorSize"]

        print("Steps for Snapshots: ", type(step))
        # RunSimulation(self.filename, self.SimNDT_Simulation)
        SimNDT_SnapShots = SnapShots(
            Enable=True,
            Step=step,
            Filename=filename,
            File_path=save_filepath,
            enableFields=enableFields,
            enableNumPy=enableNumPy,
            Extension=extension,
            dB=db,
            Color=color,
            Field=field,
            enableSignals=enableSignals,
            enableImages=enableImages,
            enableVolume=enableVolume,
            enableView=enableView,
            sensorShape=sensorShape,
            sensorPlacement=sensorPlacement,
            sensorSize=sensorSize
            )
        return SimNDT_SnapShots
    

def openSim(sim_params):
    """
    Reads all simulation parameters and sets up the entire simulation environment, 
    including scenario, materials, boundaries, transducers, inspection, source, 
    signal, simulation, receivers, and snapshots.
    
    Parameters:
    - sim_params: Dictionary containing simulation parameters.
    
    Returns:
    - SimNDT_Scenario: The scenario object.
    - SimNDT_Mat_objs: List of material objects.
    - SimNDT_Bc_objs: List of boundary condition objects.
    - SimNDT_Transd_objs: List of transducer objects.
    - SimNDT_geom_objects: List of geometric objects.
    - SimNDT_Inspection: The inspection object.
    - SimNDT_Source: The source object.
    - SimNDT_Signal: The signal object.
    - SimNDT_Simulation: The simulation object.
    - SimNDT_Receivers: The receivers object.
    - SimNDT_SnapShots: The snapshots object.
    """
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
    
    SimNDT_SnapShots = enableSnapshot(sim_params)
    
    print("steps: ", SimNDT_SnapShots.Step)
    print("Finished reading all parameters...\n")

    simPack = SimPack(SimNDT_Scenario, SimNDT_Mat_objs, \
                        SimNDT_Bc_objs, SimNDT_Inspection, SimNDT_Source, \
                        SimNDT_Transd_objs, SimNDT_Signal, SimNDT_Simulation, \
                            SimNDT_geom_objects, SimNDT_Receivers, SimNDT_SnapShots)
    
    return simPack




def runEngine(simPack):
    """
    Runs the simulation engine with the provided simulation components and 
    saves the simulation video.
    
    Parameters:
    - SimNDT_Scenario: The scenario object.
    - SimNDT_Materials: List of material objects.
    - SimNDT_Boundaries: List of boundary condition objects.
    - SimNDT_Inspection: The inspection object.
    - SimNDT_Source: The source object.
    - SimNDT_Transducers: List of transducer objects.
    - SimNDT_Signal: The signal object.
    - SimNDT_Simulation: The simulation object.
    - SimNDT_Receivers: The receivers object.
    - SimNDT_SnapShots: The snapshots object.
    """
    

    
    engine = EngineController(simPack, simPack.SnapShots)

    
    
    state = engine.run()

    if state == "Stop":
        print("Stop by User!!!!!")
    else:
        print("Simulation Done.")
    
    
        
    # SimNDT_Receivers = Receivers(self.SimNDT_Inspection.Name)
    # SimNDT_Receivers.setReceivers(engine)


def openSim_mat_file(mat_filename):
    """
    Loads simulation data from a MATLAB file and sets up the simulation environment based on the loaded data.
    
    Parameters:
    - mat_filename: The path to the MATLAB file.
    
    Returns:
    - SimNDT_Scenario: The scenario object.
    - SimNDT_Materials: List of material objects.
    - SimNDT_Boundaries: List of boundary condition objects.
    - SimNDT_Transducers: List of transducer objects.
    - SimNDT_ObjectList: List of geometric objects.
    - SimNDT_Inspection: The inspection object.
    - SimNDT_Source: The source object.
    - SimNDT_Signal: The signal object.
    - SimNDT_Simulation: The simulation object.
    - SimNDT_Receivers: The receivers object.
    """
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