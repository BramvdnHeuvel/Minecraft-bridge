from subprocess import Popen, PIPE
from typing import Union
import asyncio
import json
import sys
import re
from nbsr import NonBlockingStreamReader as NBSR
import config

# run the shell as a subprocess:
p = Popen(sys.argv[1:],
        stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)
# wrap p.stdout with a NonBlockingStreamReader object:
nbsr = NBSR(p.stdout)

async def start(client, mc_channel):
    await asyncio.sleep(3)
    
    while True:
        output = nbsr.readline(0.1)
        # 0.1 secs to let the shell output the result
        if not output:
            await asyncio.sleep(1)
        else:
            try:
                sentence = output.decode("utf-8").strip()
            except UnicodeDecodeError:
                print("Could not decode sentence:")
                print(output)
            else:
                print(sentence)
                plain_text, sentence = process_message(sentence)

                if sentence is not None:
                    print("[Matrix] " + plain_text)

                    # Send terminal message to Matrix
                    await client.room_send(
                        room_id=mc_channel,
                        message_type="m.room.message",
                        content = {
                            "msgtype": "m.text",
                            "body": plain_text,
                            "format": "org.matrix.custom.html",
                            "formatted_body": sentence
                        }
                    )

server_live = False

def process_message(sentence : str) -> Union[str, None]:
    global server_live

    if (match := re.fullmatch(
        r"\[[\d:]+\] \[Server thread\/INFO\]: Preparing level \"(.+)\""
        , sentence)):
        level, = match.groups()
        return f"Preparing level {level}...", "<strong>Preparing level \"" + level + "\"...</strong>"
    
    if re.fullmatch(
        r"\[[\d:]+\] \[Server thread\/INFO\]: Done \(\d+.?\d*s\)! For help, type \"help\"",
        sentence):
        server_live = True
        return f"The Minecraft server is live. The server is reacable at <code>{config.SERVER_IP}</code>.", f"The minecraft server is live. The server is reacable at <code>{config.SERVER_IP}</code>."
    
    if re.fullmatch(
        r"\[[\d:]+\] \[Server thread\/INFO\]: Stopping server",
        sentence):
        return "The server has stopped.", "<strong>The server has stopped.</strong>"
    
    if not server_live:
        return None, None

    if (match := re.fullmatch(
        r"\[[\d:]+\] \[Server thread\/INFO\]: ([A-Za-z0-9_]{3,16}) joined the game", 
        sentence)):
        username, = match.groups()
        return username + " joined the Minecraft server", (
            "<strong>" + username + " joined the Minecraft server</strong>")
    
    if (match := re.fullmatch(
        r"\[[\d:]+\] \[Server thread\/INFO\]: ([A-Za-z0-9_]{3,16}) left the game", 
        sentence)):
        username, = match.groups()
        return username + " left the Minecraft server", (
            "<strong>" + username + " left the Minecraft server</strong>")
    
    if (match := re.fullmatch(
        r"\[[\d:]+\] \[Server thread\/INFO\]: <([A-Za-z0-9_]{3,16})> (.+)", 
        sentence)):
        username, message = match.groups()
        return username + ": " + message, (
            "<strong>" + username + "</strong>: " + message
        )

    if (match := re.fullmatch(
        r"\[[\d:]+\] \[Server thread\/INFO\]: ([A-Za-z0-9_]{3,16}) ([\w\[\]\-\. !?,]+)", 
        sentence)):
        message = " ".join(match.groups())
        return message, "<strong>" + message + "</strong>"

    return None, None    

def reply_to_mc(message : str, author : str, 
                admin : bool = False, platform : str = 'Matrix'):
    """
        Send something back to the Minecraft terminal.
    """
    if admin and message.startswith('!'):
        p.stdin.write((message[1:] + "\r\n").encode())
    else:
        msg = [
            "",
            dict(text="M", color="red"),
            dict(text="D", color="aqua") if platform == 'Discord' else None,
            dict(text=f" <{author}> {message}")
        ]
        p.stdin.write(
            ("execute as @a run tellraw @s " + json.dumps([m for m in msg if m is not None]) + "\r\n").encode()
        )
    p.stdin.flush()

if __name__ == '__main__':
    asyncio.run(start())