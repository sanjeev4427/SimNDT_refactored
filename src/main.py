import json
import os
import sys
import numpy as np
from SimNDT.run_setup.SimulationVideo import create_vector_field_video
from SimNDT.run_setup.runSimulator import openSim, runEngine, saveVideo

def main(json_filepath):
    # Read the JSON file from the provided file path
    with open(json_filepath, "r") as f:
        sim_params = json.load(f)

    # Setup simulation environment with the provided parameters
    simPack = openSim(sim_params)

    # Run the simulation engine and save the results
    runEngine(simPack)

    # save the simulation video
    saveVideo(sim_params, simPack)
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_json_file>")
        sys.exit(1)

    json_filepath = sys.argv[1]
    main(json_filepath)