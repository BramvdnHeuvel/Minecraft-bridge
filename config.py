import os

# Minecraft bridge credentials
MATRIX_HOMESERVER = os.getenv('MATRIX_HOMESERVER')  or "https://homeserv.er"
MATRIX_USERNAME   = os.getenv('MATRIX_USERNAME')    or "@bridge_username:homeserv.er"
MATRIX_PASSWORD   = os.getenv('MATRIX_PASSWORD')    or "bridge_password"

SERVER_IP = os.getenv('SERVER_ADDRESS') or 'unknown ip'

# Matrix users who are allowed to run OP commands in Minecraft through Matrix
MC_ADMINS = [
    "@bramvdnheuvel:nltrix.net",                # Bram on Matrix  (example, feel free to remove)
    "@_discord_625632515314548736:t2bot.io"     # Bram on Discord (example, feel free to remove)
    # Your username on Matrix
]
if os.getenv('MATRIX_ADMINS') is not None:
    MC_ADMINS = os.getenv('MATRIX_ADMINS').split(',')

# Matrix channel that the bot should talk to
MC_CHANNEL = os.getenv('MC_CHANNEL') or "!channel_id:homeserv.er"

make_bool = lambda os_value, default_value : default_value if not os_value else (
    False if os_value.lower() == 'false' else True
)

SERVER_SETTINGS = {
    'level-name': os.getenv('WORLD') or 'world',
    
    # Server settings
    'port'          : 25565 if os.getenv('PORT') == None else int(os.getenv('PORT')),
    'query.port'    : 25565 if os.getenv('PORT') == None else int(os.getenv('PORT')),
    'max-players'   : 7 if os.getenv('MAX_PLAYERS') == None else int(os.getenv('MAX_PLAYERS')),
    
    # Server temperature  >:3
    'view-distance'         : 10 if os.getenv('RENDER_DISTANCE') == None else int(os.getenv('RENDER_DISTANCE')),
    'enable-command-block'  : make_bool(os.getenv('COMMAND_BLOCKS'), True),
    
    # Environment
    'allow-nether'      : make_bool(os.getenv('NETHER'),    True),
    'spawn-npcs'        : make_bool(os.getenv('NPCS'),      True),
    'spawn-animals'     : make_bool(os.getenv('ANIMALS'),   True),
    'spawn-monsters'    : make_bool(os.getenv('MONSTERS'),  True),
    
    # Gamemode
    'pvp'       : make_bool(os.getenv('PVP'),       True),
    'gamemode'  : os.getenv('GAMEMODE') or 'survival',
    'difficulty': os.getenv('DIFFICULTY') or 'medium',
    'hardcore'  : make_bool(os.getenv('HARDCORE'),  False),
    
    # Grief protection
    'online-mode'       : make_bool(os.getenv('VERIFY_ACCOUNTS'),   True),
    'white-list'        : make_bool(os.getenv('WHITELIST'),         True),
    'enforce-whitelist' : make_bool(os.getenv('WHITELIST'),         True),
    'spawn-protection'  : 16 if os.getenv('SPAWN_PROTECTION') == None else os.getenv('SPAWN_PROTECTION'),
}
