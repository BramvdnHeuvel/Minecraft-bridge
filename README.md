# Minecraft-bridge

This repository hosts a Minecraft server that is also connected to a Matrix client.

This way, communication is enabled between a Minecraft server and a Matrix room.

## Setup

1. Create a Docker image using the following command:

```
docker build -t matrix-mc-server ./
```

2. Download the [latest Minecraft server jar file](https://www.minecraft.net/en-us/download/server).

3. Open `config.yaml` and adjust it to however you like.

**NOTE:** Make sure to set EULA to `true` otherwise the server will refuse to start.

4. Start the Docker container. You will need a few volumes:

- `/usr/src/app/config.yaml` - Location of your custom `config.yaml`
- `/usr/src/app/whitelist.json` - Location of your whitelist, if any.
- `/usr/src/app/world/` - Folder of your custom Minecraft world to load
- `/usr/src/app/server.jar` - (Default) location of the server jar file. Can be changed in `config.yaml`.

For example, your Docker compose file could look like the following:

```docker-compose
version: '3'

services:
    matrix-mc-server:
        image: matrix-mc-server:latest
        volumes:
            - <your config>:/usr/src/app/config.yaml
            - <your whitelist>:/usr/src/app/whitelist.json
            - <your world folder>:/usr/src/app/world
            - <your server jar file>:/usr/src/app/server.jar
```