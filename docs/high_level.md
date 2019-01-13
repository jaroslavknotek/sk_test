High level description
===

Application is a thin client, processing data from SpaceKnow api. 

## Architecture

App comprises of three main modules
- sk_api 
- carcounter
- main

**sk_api**

Low level communication with api. Provide all necessities to call SpaceKnow api and properly communicate. 
It works with the async api as well.

**carcounter**

Uses sk_api to obtain scenes and maps and performs car counting on them. This is the module in which all business
logic is stored. All low level methods are in *sk_api*.

**main** 
It is responsible for orchestration and output processing.

## Flow
- App finds all available scenes for the given polygon and time span
- Once the scenes are available, they are used to calculate cars and obtain maps
  - for each scene there is map obtained along with it's tiles and counting is performed. all si sychronously in one 
    thread
It might be more efficient to create chain of continuation from scene to map to tiles. 
~~~
                - tile_1
Scene -> Map    - tile_2
                - tile_n
~~~

Once all images are composed the number of cars for each image si summed and printed to user.