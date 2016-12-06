#### 
<img src="https://dl2.pushbulletusercontent.com/KbQ1LfBQ4PvfBj4LmbcYmXDPBHlTsnHR/Passageway.png" width="500px">

### Project Description
Passageway is an attempt to provide a cost-effective, scalable, and automated method of aggregating foot traffic data within a facility. Such data aggregation offers meaningful statistics about the foot traffic of individuals within a defined space. With Passageway, users are able to see heat maps and view graphs that represent the foot traffic in a building, and analyze it on a website with various building floor-plans layered onto a Google Map. Users may also specify a certain time frame to see specific temporal data. All of the data is collected within the facilities through a system including CHIP computers connected to a pair of Infrared break beams. Ultimately, the data may be used to determine the frequency of activity for specific rooms, hallways, or entryways. Foot traffic data may be useful for understanding activity within a facility, seeing popularity of certain areas during specific times, or identifying times where room capacity is exceeded and thus presents a fire code violation.

### Architecture Overview
<center><img src="http://i.imgur.com/LuledZu.png" width="700px"></center>

### Repositories

 - [Android](https://github.com/Passageway/PassagewayAndroid) 
 - [Field Unit](https://github.com/Passageway/PassagewayFieldUnit) *You are here*
 - [Web](https://github.com/Passageway/PassagewayWeb)

### Repo Overview
This is the Field Unit part of the Passageway project. This is the main part of the project. In this repository is the python program that handles all of the logic for recording data and pushing it to Firebase, the cloud database solution that we used. There are also a few useful bash scripts included as well.

### What it Looks Like
Here are some pictures to give a better understanding of what this field unit looks like when set up. Links to all the required hardware (or at least what we used) are available in the wiki section of this repository.
<center><img src="http://i.imgur.com/1rv1cyM.png" width="400px"></center>

Seen in the picture above is a diagram of how a single field unit would be laid out when fully set up. The two receiving infrared sensors are housed in a larger 3D-printed housing unit and a single sender IR beam is housed. 
<center><img src="http://i.imgur.com/AioHmkr.png" width="500px"></center>

Above is a look at what the field unit looks like from a top-down perspective. This layout ensures that CHIP microcomputer is protected as well as possible and there are minimal exposed wires.

### Detailed Set-up Instructions
The wiki section will have more details on how to exactly set the system up in your own environment for testing. it is worth noting that this system is very much still in early stages and is not perfect by any means.
