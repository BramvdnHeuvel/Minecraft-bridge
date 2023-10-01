import src.mc_wrapper as mc_wrapper
import src.mxclient as matrix_client

import asyncio

# Start the Minecraft process
asyncio.run(matrix_client.start())
