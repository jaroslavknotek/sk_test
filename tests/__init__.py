import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath( os.path.join(inspect.getfile(inspect.currentframe()), os.pardir)))
currentdir = currentdir  +"\\src\\"
sys.path.insert(0,currentdir )