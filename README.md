# Minecraft-bridge

This repository hosts a Minecraft server that is also connected to a Matrix client.

This way, communication is enabled between a Minecraft server and a Matrix room.

## Setup

To create a Docker image, go to this folder and run the following command:

```
docker build -t matrix-mc-server ./
```

Then, once a Docker image has been created, you can run the following command to run a Minecraft server. In `config.py`, you can find additional environment variables you can insert to alter settings on the Minecraft server.

```
docker run --name mc-server \
-p 25565:25565 \
-v "<folder in which your store your Minecraft world>":/usr/src/app/world \
-e EULA=true \
-e MATRIX_HOMESERVER='<your matrix homeserver>' \
-e MATRIX_USERNAME='<matrix bridge client username>' \
-e MATRIX_PASSWORD='<matrix bridge client password>' \
-e MC_CHANNEL='<channel in which you communicate>' \
-e SERVER_ADDRESS='<ip address where players can connect to the server>' \
mc-bridge
```

This should successfully launch your bridged Minecraft server.
