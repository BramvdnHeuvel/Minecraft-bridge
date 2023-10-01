"""
    This module loads and parses the config.yaml file.
"""

from typing import Any, List, Optional
import yaml

with open('config.yaml', 'r') as open_file:
    SETTINGS = yaml.load(open_file, Loader=yaml.Loader)

def at(keys : List[str]) -> Optional[Any]:
    """
        Potentially get a value. If it doesn't exist, return None.
    """
    return at_value(keys, SETTINGS)

def at_value(keys : List[str], value : Any) -> Optional[Any]:
    try:
        head, tail = keys[0], keys[1:]
    except IndexError:
        return value
    else:
        try:
            new_value = value[head]
        except TypeError:
            return None
        except KeyError:
            return None
        else:
            return at_value(tail, new_value)

# EULA
EULA = at(['config', 'eula']) or False

# Minecraft bridge credentials
MATRIX_HOMESERVER = at(['matrix', 'homeserver']) or "https://matrix.example.org/"
MATRIX_USERNAME   = at(['matrix', 'username'])   or "@alice:example.org"
MATRIX_PASSWORD   = at(['matrix', 'password'])   or "bridge_password"

# Matrix bridge room
MATRIX_ROOM = at(['matrix', 'room_id']) or "!channel_id:example.org"

SERVER_IP = at(['matrix', 'server_address']) or 'unknown ip'

MATRIX_ADMINS = at(['matrix', 'mc-admins']) or []

try:
    RAM_SIZE = int(at(['config', 'ram']))
except TypeError:
    RAM_SIZE = 1024
except ValueError:
    RAM_SIZE = 1024

SERVER_JAR_LOCATION = at(['config', 'server_jar']) or 'server.jar'

RUN_COMMAND = [
    'java', 
    f'-Xmx{RAM_SIZE}M', 
    f'-Xms{RAM_SIZE}M', 
    '-jar', SERVER_JAR_LOCATION, 
    'nogui'
]
