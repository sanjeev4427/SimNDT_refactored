import json

data = {
  
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
  }
      
      
}


with open("simndt_params.json", "w") as f:
    json.dump(data, f, indent=2)