import carcounter
import os
import json
import argparse

parser = argparse.ArgumentParser(description='count cars')
parser.add_argument("--outputDir", type=str, help="output directory")
parser.add_argument("--config", type=str, help="path to config file")

args = parser.parse_args()
# input data definition

# create output directory
dir_path = args.outputDir
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

with open(args.config, 'r') as f:
    config = json.load(f)

# count cars
cred = config["credentials"]
polygon = config["polygon"]
car_counter_api = carcounter.CarCounter(cred, polygon)

print("getting valid scenes")
start_date = "2018-01-01 00:00:00"
end_date = "2019-02-01 00:00:00"
scenes = car_counter_api.get_scenes(start_date, end_date)

print("getting car data")
cars_maps = car_counter_api.get_cars_maps(dir_path, scenes)

print("counting results")
car_sum = sum([count for _, count in cars_maps])
print("car sum over all available images: ", car_sum)
print("see the pictures in ", dir_path)
