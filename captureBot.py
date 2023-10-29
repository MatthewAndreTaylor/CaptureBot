from time import time_ns

import cv2
import discord
from discord.ext import tasks

import capture
from discord_secret import token

help_message = """
Capture Bot 📸 use `!capture` to get a camera snapshot.
Detects differences in image state and uploads the differences to discord.
Use `!start` to start the detecting and `!stop` to turn off detection.
"""

class CaptureBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currFrame = None
        self.detecting = False
        self.firstFrame = capture.get_frame()
        self.channelId = 0

    async def on_ready(self):
        for guild in self.guilds:
            for channel in guild.text_channels:
                self.channelId = channel.id
        print(f"We have logged in as {self.user}")


    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith("!help"):
            await message.channel.send(help_message)

        if message.content.startswith("!start"):
            if not self.detecting:
                self.detecting = True
                self.firstFrame = capture.get_frame()
                self.detect.start()
                await message.channel.send("Starting detection")

        if message.content.startswith("!stop"):
            if self.detecting:
                self.detecting = False
                self.detect.stop()
                await message.channel.send("Stopped detection")

        if message.content.startswith("!capture"):
            if self.currFrame is not None:
                cv2.imwrite("./img.jpg", self.currFrame)
                picture = discord.File("./img.jpg")
                await message.channel.send(file=picture)

        if message.content.startswith("!lapse"):
            self.timelapse.start()
            await message.channel.send("Starting lapse")

    @tasks.loop(seconds=1)
    async def detect(self):
        self.currFrame = capture.get_frame()
        if capture.isOccupied(self.firstFrame, self.currFrame):
            general = self.get_channel(self.channelId)
            cv2.imwrite(f"./img.jpg", self.currFrame)
            picture = discord.File("./img.jpg")
            await general.send(content=f"`detected`", file=picture)

        self.firstFrame = self.currFrame

    @detect.before_loop
    async def before_detection(self):
        await self.wait_until_ready()

    @tasks.loop(seconds=2)
    async def timelapse(self):
        frame = capture.get_frame()
        cv2.imwrite(f"./timelapse/img{time_ns()}.jpg", frame)

    @timelapse.before_loop
    async def before_timelapse(self):
        await self.wait_until_ready()


intents = discord.Intents.default()
intents.message_content = True
client = CaptureBot(intents=intents)
try:
    client.run(token)
except discord.HTTPException as e:
    raise e

capture.cam.release()
