"""
    This module prepares the necessary files for running the server in the
    correct configuration.
"""

import src.config as config

def write_eula():
    """
        Write whether the user accepts to Minecraft's EULA.
        The server refuses to run unless explicitly accepted.
    """
    with open("eula.txt", 'w') as fp:
        if config.EULA == True:
            fp.write("eula=true")
        else:
            fp.write("eula=false")

def write_server_properties():
    """
        Write the configuration for the Minecraft world.
    """
    with open("server.properties", 'w') as fp:
        for key, value in config.at(['minecraft']).items():
            fp.write(f"{key}={value}\n")
