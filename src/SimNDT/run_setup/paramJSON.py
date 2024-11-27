import json
import os
from datetime import datetime
from collections import OrderedDict

data = OrderedDict({
  
  "Scenario": {
      "Width": 100,
      "Height": 100,
      "Pixel_mm": 10.0,
      "Label": 0
    },
  
  "Materials": [
    {
        "C22": 1.0864e+11,
        "C44": 3.87e+10,
        "Name": "aluminium",
        "VL": 6319.90320105,
        "Label": 0,
        "VT": 3771.99432349,
        "Damping": 0,
        "Rho": 2720.0,
        "C12": 3.124e+10,
        "C11": 1.0864e+11,
        "Eta_s": 1e-30,
        "Eta_v": 1e-30
    },
    {
        "C22": 1.0864e+11,
        "C44": 3.87e+10,
        "Name": "aluminium",
        "VL": 6319.90320105,
        "Label": 40,
        "VT": 3771.99432349,
        "Damping": 0,
        "Rho": 2720.0,
        "C12": 3.124e+10,
        "C11": 1.0864e+11,
        "Eta_s": 1e-30,
        "Eta_v": 1e-30
    },
    {
        "C22": 7.76e+10,
        "C44": 6.59e+09,
        "Name": "glass",
        "VL": 5560.24591735,
        "Label": 80,
        "VT": 1620.33885591,
        "Damping": 0,
        "Rho": 2510.0,
        "C12": 6.442e+10,
        "C11": 7.76e+10,
        "Eta_s": 1e-30,
        "Eta_v": 1e-30
    },
    {
        "C22": 1.0864e+11,
        "C44": 3.87e+10,
        "Name": "aluminium",
        "VL": 6319.90320105,
        "Label": 120,
        "VT": 3771.99432349,
        "Damping": 0,
        "Rho": 2720.0,
        "C12": 3.124e+10,
        "C11": 1.0864e+11,
        "Eta_s": 1e-30,
        "Eta_v": 1e-30
    }
],
  
  "Boundaries": [
      { 
        "Name": "Top",
        "Size": 5.0,
        "Type": "Absorbing"
      },
      { 
       "Name": "Bottom",
        "Size": 5.0,
        "Type": "Absorbing"
      },
      { 
       "Name": "Left",
        "Size": 5.0,
        "Type": "Absorbing"
      },
      {
        "Name": "Right",
        "Size": 5.0,
        "Type": "Absorbing"
      }
    ],
  
  "Transducers": {
    "SizePixel": 62.0,
    "Name": "emisor",
    "PZT": 0,
    "PointSource": 0,
    "CenterOffset": 0.0,
    "BorderOffset": 0.0,
    "Field": 0,
    "Window": 0,
    "Location": "Top",
    "Size": 20.0
    },

    
  "GeometricObjects": [
    {   "x0": 50.0,
        "a": 5.0,
        "b": 2.0,
        "Name": "ellipse",
        "Label": 40,
        "y0": 50.0,
        "theta": 40.0,
        
    },
    {
        "y0": 75.0,
        "x0": 25.0,
        "r": 5.0,
        "Name": "circle",
        "Label": 80
    },
    {
        "a": 5.0,
        "b": 2.0,
        "Name": "ellipse",
        "Label": 120,
        "y0": 50.0,
        "theta": 40.0,
        "x0": 50.0
    }
    ],
  
  "Inspection": {
    "Location": "Top",
    "Method": "Transmission",
    "Name": "Transmission"
    },
  
  "Source": {
    "Pressure": 1,
    "Longitudinal": 1,
    "Displacement": 0,
    "Shear": 0
  },
  
  "Signal": {
      "Frequency": 500000.0,
      "N_Cycles": 1,
      "Name": "RaisedCosine",
      "Amplitude": 1.0,
    },
  
  "Simulation": {
    "PointCycle": 10,
    "SimulationTime": 5e-05,
    "TimeScale": 1.0,
    "MaxFreq": 1000000.0,
    "Order": 2
    },
  
  "Receivers": {
    "Method": "Trasmission",
  },
  
  "Snapshot" : {
    "Step": 100,
    "Save_filepath": r"C:\Users\Kumar\Nextcloud\Work\GUW\sim_ndt\simndt2-main\simndt2\saved_simulations\numpy_Vx_Vy_2",
    "Filename": "numpy",
    "enableFields": True,
    "enableNumPy": True,
    
    "Extension": ".png",
    "dB": 60,
    "Color": 0,
    "Field": 0,
    "enableSignals": False,
    "enableImages": False,
    "enableVolume": False,
    "enableView": False,
    "sensorShape": [],
    "sensorPlacement": [],
    "sensorSize": 0
},
    
    "SimVideo": {
      "Save_filepath": r"C:\Users\Kumar\Nextcloud\Work\GUW\sim_ndt\simndt2-main\simndt2\saved_simulations\sim_video",
    }
      
})

# use python>= 3.7 to keep the ordered dictionary
folder_path = r"C:\Users\Kumar\Nextcloud\Work\GUW\sim_ndt\batch_processing_simulator\ParamJSON"
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
save_path = os.path.join(folder_path, "simndt_params_{current_time}.json".format(current_time=current_time))
with open(save_path, "w") as f:
    json.dump(data, f, indent=2, sort_keys=False)