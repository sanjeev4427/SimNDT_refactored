### Batch processing run
1. Update the path to save the simulation data in the JOSN file under the key name ["Snapshot"]["Save_filepath"].
2. Run and save simulation command: python main.py "path_to_json_file"

### Saving simulation video file 
1. update the path to video file in the param JSON file under key name ['SimVideo']["Save_filepath"].
2. Comment out saveVideo(sim_params, simPack) function to not save the videos. 
