# tileD
The self-hosted dashboard for managing your Tile trackers and Tile enabled devices - tileD(ashboard)

## About
Tile premium is $3/mo. If you're like me, that is WAYY too much money and you'd rather host something yourself on an old poweredge that idles at few hundred watts!

tileD will allow (does allow?) for:
- Unlimited custom alerts
- Unlimited location history
- Custom integrations for notifications
- 10 points of self-hosted coolness!

This is a python program running in Flask. Should run on pretty much anything, as it is only a few hundred lines of code and barely anything but web calls and text manipulation. 

This application heavily relies on (and is inspired by) the [pytile](https://github.com/bachya/pytile) library. Shoutout to that guy for reverse engineering the Tile devices API. 

I would have coded this in a real JS framework but I did not want to reverse engineer the pytile library. IDK anything about flask so bear with me. 

## Installation

Here's your docker compose:

```yaml
services:
    tileD:
        image: gusvendegna/tiled:latest
        ports:
            - 5000:5000
        environment:
            - TILE_EMAIL=bob@gmail.com
            - TILE_PASSWORD=yourpassword
            - DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/123123123123

```

Device location history is very much dependent on how long you have been running the application for. You can technically fetch this from tile to start, but that requires a premium subscription and that's kinda what I'm trying to avoid here. Importing this data in could be a future goal. of this project.

I will never prune any location information, personally, and probably will never add that into the app since it's only a few TEXT properties and you probably have a gig or two to spare. There is some client side caching and I am trying to avoiding storage of duplicate data but only god knows what is actually going on.


[DockerHub  Link](https://hub.docker.com/r/gusvendegna/tiled)
