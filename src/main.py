import carcounter
import os

import argparse

parser = argparse.ArgumentParser(description='count cars')
parser.add_argument("--outputDir", type=str, help="output directory")
parser.add_argument("--startDate", type=str, help="start_date")
parser.add_argument("--endDate", type=str, help="end_date")


args = parser.parse_args()
## input data definition

# todo to file and argument
cred = {
    # id taken from the documentation
    "id": "hmWJcfhRouDOaJK2L8asREMlMrv3jFE1",
    "user": "knotekjaroslav@email.cz",
    "pass": "Spaceknow1"}

# polygon position
polygon = [[153.1050866, -27.3900761], [153.1042391, -27.3913812], [153.1035105, -27.3926031],
           [153.1045404, -27.393127], [153.1054202, -27.3935366], [153.1061819, -27.3921268],
           [153.1067389, -27.3908954], [153.1061381, -27.3905143], [153.1050866, -27.3900761]]


# create output directory
dir_path = args.outputDir
if not os.path.exists(dir_path):
    os.makedirs(dir_path)


## count cars

car_counter_api = carcounter.CarCounter(cred, polygon)
print("getting valid scenes")
scenes = car_counter_api.get_scenes(args.startDate,args.endDate)

print("getting car data")
cars_maps=car_counter_api.get_cars_maps( dir_path ,scenes)
print("counting results")
car_sum=sum([ count for _,count in cars_maps])
print("car sum over all available images: ", car_sum )
print("see the pictures in ", dir_path)

