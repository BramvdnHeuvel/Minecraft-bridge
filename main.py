import asyncio
import time
import re

from nio import AsyncClient, MatrixRoom, RoomMessageText
import mc_wrapper
 
import config
import build_server

STARTUP_TIME = time.time()

client = AsyncClient(config.MATRIX_HOMESERVER, config.MATRIX_USERNAME)

async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    if room.machine_name != config.MATRIX_ROOM:
        return
    if event.sender == client.user_id:
        return
    if int(event.server_timestamp) < STARTUP_TIME:
        return

    # Determine platform
    platform = 'Matrix'
    if re.fullmatch(r"@_discord_\d+:t2bot\.io", event.sender):
        platform = 'Discord'

    # Determine how to display username
    name = room.users[event.sender].display_name
    for user in room.users:
        if user == event.sender:
            continue

        if room.users[user].display_name == name:
            name = room.users[event.sender].disambiguated_name
            break

    mc_wrapper.reply_to_mc(
        event.body, name,
        admin=(event.sender in config.MC_ADMINS),
        platform=platform
    )
client.add_event_callback(message_callback, RoomMessageText)


async def activate_client() -> None:
    print(await client.login(config.MATRIX_PASSWORD))

    await client.room_send(
        room_id=config.MC_CHANNEL,
        message_type="m.room.message",
        content = {
            "msgtype": "m.text",
            "body": "Starting Minecraft-Matrix bridge...",
            "format": "org.matrix.custom.html",
            "formatted_body": "<strong>Starting Minecraft-Matrix bridge...</strong>"
        }
    )
    await client.sync_forever(timeout=30000) # milliseconds

async def start():
    await asyncio.gather(
        activate_client(),
        mc_wrapper.start(client, config.MC_CHANNEL)
    )

asyncio.run(start())