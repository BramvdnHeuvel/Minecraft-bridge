from subprocess import Popen, PIPE
from typing import Union
import asyncio
import json
import re
from nbsr import NonBlockingStreamReader as NBSR
import config
import build_server as build

# Write the appropriate files
build.write_eula()
build.write_server_properties()

# run the shell as a subprocess:
p = Popen(config.RUN_COMMAND,
        stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)
# wrap p.stdout with a NonBlockingStreamReader object:
nbsr = NBSR(p.stdout)

async def start(client, mc_channel):
    """
        Start reading from the Minecraft subprocess.
    """
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
    """
        Process a message that is sent to stdout in the Minecraft terminal.

        If this function deems it relevant, it returns a string that can be
        sent to Matrix.
    """
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
            "<strong>" + username + " left the Minecraft server</strong>"
        )
    
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

def reply_to_mc(message : str, display_name : str, sender : str):
    """
        Send something back to the Minecraft terminal.
    """
    if sender in config.MATRIX_ADMINS and message.startswith('!'):
        p.stdin.write((message[1:] + "\r\n").encode())
    else:
        p.stdin.write(
            ("execute as @a run tellraw @s " + format(sender, display_name, message) + "\r\n").encode()
        )
    p.stdin.flush()

def format(sender : str, display_name : str, message : str) -> str:
    """
        Create a string used to format the user's message.
    """
    start = [ "", dict(text="M", color="red" ) ]
    end   = [ dict(text=f" <{display_name}> {message}") ]

    options = config.at(['matrix', 'alternative_platforms']) or {}

    for platform, details in options.items():
        try:
            regex = details['match']
            text  = details['text']
            color = details['color']
        except KeyError:
            print("WARNING: Platform `" + platform + "` is missing some configurations.")
        else:
            if re.fullmatch(regex, sender):
                start.append(dict(text=text, color=color))
    
    return json.dumps(start + end)

if __name__ == '__main__':
    asyncio.run(start())