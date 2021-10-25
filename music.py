import discord
from discord.ext import commands
import youtube_dl
import asyncio
import urllib
import simplejson

urls = []
playList = []
fsStatus = False


class music(commands.Cog):
    def __int__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Join a voice channel first")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.send("MusicBot is occupied")

    @commands.command()
    async def disconnect(self, ctx):
        if ctx.voice_client != None:
            await ctx.voice_client.diconnect()

    @commands.command()
    async def play(self, ctx, url):
      
      # id = 'KQEOBZLx-Z8'
      # tempurl = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % id
      # json = simplejson.load(urllib.urlopen(tempurl))
      # title = json['entry']['title']['$t']
      # playList.append(title) 
      # print(playList)
      
      if ctx.voice_client is None:
          voice_channel = ctx.author.voice.channel
          await voice_channel.connect()

      global fsStatus
      if not fsStatus:
          urls.append(url)
      else:
          fsStatus = False
      # if len(urls) == 0 or not ctx.voice_client.is_playing():
      if not ctx.voice_client.is_playing():

          print(url)
          while (len(urls) != 0):

              #ctx.voice_client.stop()
              FFMPEG_OPTIONS = {
                  'before_options':
                  '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                  'options': '-vn'
              }
              YDL_OPTIONS = {'format': "bestaudio"}
              vc = ctx.voice_client

              with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                  info = ydl.extract_info(urls.pop(0), download=False)
                  url2 = info['formats'][0]['url']
                  source = await discord.FFmpegOpusAudio.from_probe(
                      url2, **FFMPEG_OPTIONS)
                  vc.play(source)
              while (ctx.voice_client.is_playing()):
                  await asyncio.sleep(1)
              playList.pop(0)


    @commands.command()
    async def fs(self, ctx):
        global fsStatus
        fsStatus = True
        print(urls) #success stop message
        ctx.voice_client.stop()
        #await ctx.invoke(self.client.get_command('play'),url=urls[0])

    @commands.command()
    async def remove(self, ctx, num):
        if num.isnumeric():
            num = int(num)
            if 1 <= num <= len(urls):
                urls.pop(num - 1)
                print("remove succeed")
                print(urls)
            else:
                print("cannot remove")

    @commands.command()
    async def move(self, ctx, num):
        if num.isnumeric():
            num = int(num)
            if 1 <= num <= len(urls):
                urls.insert(0, urls.pop(num - 1))
            else:
                print("out of list")
        else:
            print("wrong command")

    @commands.command(pass_context=True)
    async def list(self, ctx):
        print(urls)
        # for url in urls:
        #   await ctx.send(url)
        await ctx.send(urls)

    # @commands.commands()
    # async def fs(self,ctx,url):


def setup(client):
    client.add_cog(music(client))
