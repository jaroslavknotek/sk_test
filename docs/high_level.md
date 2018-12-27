High level description
===

Application is a thin client processing data from SpaceKnow api. 




## Architecture

App comprises of three main modules
- sk_api 
- carcounter
- main

**sk_api**
Low level comunication with api. Provide all necessities to call spaceknow api and properly comunicate. It 
can work wiht the async api.

**carcounter**
Uses sk_api to obtain scenes and maps and performes car counting on them. This is the module in which all business
llogic is stored. All low level methods are in sk_api.

**main** 
It puts it all together. It hold some data such as credentails and polygon(for simplicity let there, stored in a file 
otherwise) processes input params. It is responsible for program steering and output processing.

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

## Notes
I decided to represent sk_api and carcounter with classes since they are not only bunch of methods, but need to hold 
some states. sk_api rememebers header for post request to avoid bother with every call. The carcounter has api as a 
state. I am not sure, wheter this is needed, but I don't know about proper solution... 
maybe decorator with reference to config file 

app support async api. there is a nice generic method in sk_api that follows the cycle

- init
- wait until get-status != processing
- retrieve
- if there is a cursor, repeat step 1

app does not utilize paralellism. I decided to avoid it since I don't know about it that much. I also wanted to avoid too much complexity/

App does not offer proper handling of all invalid states. Can be done upon request. Current state assumes that the space know api works fine.

App does not try to use any features considering billing, users, permissions and such. It focueses mainly on the task.

There is only a single commit. To test my version systems skill I can take another test. 

upon closer look, many literals can be found. I wanted to avoid using some module handling literals. It's seems to be unecessary. Can be done upon request.

there might be some problems with installing pillow. pipenv install pillow had some issues

I tested only few methods. Testing is very time consumin so I decided to just show that how would I do it if I had more time. Testing can be extended upon request.

