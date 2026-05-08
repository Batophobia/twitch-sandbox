from twitchAPI import chat
import websockets
import json
from code.common import getCommandData

#https://pytwitchapi.dev/en/stable/modules/twitchAPI.chat.html#twitchAPI.chat.ChatMessage

clients = set()
async def handler(websocket):
  print("New connection")
  clients.add(websocket)
  try:
    async for message in websocket:
      pass
  finally:
    clients.remove(websocket)

async def init():
  return await websockets.serve(handler, "localhost", 6677)

async def broadcast(data):
  if clients:
    for client in clients:
      await client.send(json.dumps(data))

async def add(cmd: chat.ChatCommand):
  # Get command config
  # cmdData = getCommandData(cmd)
  
  await broadcast({
    "type": "spawn",
    "user": cmd.user.name
  })

  await cmd.reply("Welcome in little gremlin")
