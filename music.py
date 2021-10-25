import discord
from discord.ext import commands
import youtube_dl
import asyncio
from requests import get

sources = []
urls = 0
playList = []
loopQueue = False
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}


def search(arg):
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            get(arg)
        except:
            video = ydl.extract_info(f"ytsearch:{arg}",
                                     download=False)['entries'][0]
        else:
            video = ydl.extract_info(arg, download=False)

    return video


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
        global sources
        global urls
        global playList
        global loopQueue
        if ctx.voice_client != None:
          ctx.voice_client.stop()
          await asyncio.sleep(1)
          sources = []
          urls = 0
          playList = []
          loopQueue = False
          await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, url):
        global urls
        global loopQueue
        global YDL_OPTIONS
        # id = 'KQEOBZLx-Z8'
        # tempurl = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % id
        # json = simplejson.load(urllib.urlopen(tempurl))
        # title = json['entry']['title']['$t']
        # playList.append(title)
        # print(playList)

        if ctx.voice_client is None:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()

        urls += 1
        FFMPEG_OPTIONS = {
            'before_options':
            '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        vc = ctx.voice_client

        info = search(url)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(
            url2, **FFMPEG_OPTIONS)
        sources.append(source)
        video_title = info.get('title', None)
        playList.append(video_title)
        await ctx.send("song added: "+video_title)
        # if len(urls) == 0 or not ctx.voice_client.is_playing():
        if urls == 1:
            print(url)
            while (len(sources) != 0):

                #ctx.voice_client.stop()
                vc.play(sources[0])

                while (ctx.voice_client.is_playing()):
                    await asyncio.sleep(1)
                if not loopQueue:
                    sources.pop(0)
                    playList.pop(0)
                    urls -= 1
                else:
                    sources.append(sources.pop(0))
                    playList.append(playList.pop(0))
                await asyncio.sleep(1)

    @commands.command()
    async def loopqueue(self, ctx):
        global loopQueue
        loopQueue = not loopQueue
        if loopQueue:
            await ctx.send("loopqueue enabled")
        else:
            await ctx.send("loopqueue disabled")

    @commands.command()
    async def fs(self, ctx):
        print(urls)  #success stop message
        ctx.voice_client.stop()

        #await ctx.invoke(self.client.get_command('play'),url=urls[0])

    @commands.command()
    async def remove(self, ctx, num):
        global urls
        if num.isnumeric():
            num = int(num)
            if 1 <= num <= len(sources):
                urls -= 1
                sources.pop(num)
                removed = playList.pop(num)
                print("remove succeed: " + removed)
                await ctx.send("remove succeed: " + removed)
                print(playList)
            else:
                print("cannot remove")

    @commands.command()
    async def move(self, ctx, num):
        if num.isnumeric():
            num = int(num)
            if 1 <= num <= len(sources):
                sources.insert(1, sources.pop(num))
                playList.insert(1, playList.pop(num))
                print("move succeed")
                await ctx.send("move succeed number" + num)
            else:
                print("out of list")
        else:
            print("wrong command")

    @commands.command(pass_context=True)
    async def list(self, ctx):
        tempstring = ""
        for i, list in enumerate(playList):
            if i == 0:
                tempstring += "Current: " + list + "\n" + "Next:" + "\n"
            else:
                tempstring += str(i) + ". " + list + "\n"
        if urls:
            if loopQueue:
                tempstring += "loopqueue: enable"
            else:
                tempstring += "loopqueue: disable"
        await ctx.send(tempstring)
        # for url in urls:
        #   await ctx.send(url)

    # @commands.commands()
    # async def fs(self,ctx,url):


def setup(client):
    client.add_cog(music(client))
