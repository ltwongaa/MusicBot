import discord
from discord.ext import commands
import music

cogs=[music]

client = commands.Bot(command_prefix = '!' , intents = discord.Intents.all())

for i in range(len(cogs)):
  cogs[i].setup(client)



client.run("OTAxNzAzMjk2MzU4Njg2NzUw.YXTuog.cTfPTSk_lGm1U9U51jzUlx6D5FU")
#client.run("OTAxODgyMjYyNjQ2Mjk2NjU5.YXWVTw.yO6EVmTpZ7Lf7g1pWHjgdxO_v-o")
