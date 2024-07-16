# tileD
The self-hosted dashboard for managing your Tile trackers and Tile enabled devices

## About
Tile premium is $3/mo. If you're like me, that is WAYY too much money and you'd rather host something yourself on an old poweredge that idles at few hundred watts!

tileD will allow for:
- Unlimited custom alerts
- Unlimited location history
- Custom integrations for notifications
- 10 points of self-hosted coolness!

This is a python program running in Flask. Should run on pretty much anything, as it is only a few hundred lines of code and barely anything but web calls and text manipulation. 

This application heavily relies on (and is inspired by) the [pytile](https://github.com/bachya/pytile) library. Shoutout to that guy for reverse engineering the Tile devices API. 

I would have coded this in a real JS framework but I did not want to reverse engineer the pytile library. IDK anything about flask so bear with me. 

## Installation

It will eventually be a docker container, but I'm not far enough into development to actually use this application day-to-day, so it lives as raw python files in my documents folder on my desktop. 

However, if someone wants to make me a DockerFile, please feel free. This is probably what a ```docker-compose.yml``` will look like:

```yaml
services:
    tileD:
        image: gusvendegna/tileD:latest
        ports:
            - 8080:8080
        environment:
            - TILE_EMAIL=bob@gmail.com
            - TILE_PASSWORD=yourpassword

# eventually, you'll also put your notification integration (probably discord to start) keys here too
```

Device location history is very much dependent on how long you have been running the application for. You can technically fetch this from tile to start, but that requires a premium subscription and that's kinda what I'm trying to avoid here. Importing this data in could be a future goal. of this project.

I will never prune any location information, personally, and probably will never add that into the app since it's only a few TEXT properties and you probably have a gig or two to spare. There is some client side caching and I am trying to avoiding storage of duplicate data but only god knows what is actually going on.