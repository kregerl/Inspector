from discord_slash.utils.manage_commands import create_option
from discord_slash import SlashCommand, SlashContext
from dotenv import dotenv_values
from typing import List
from time import sleep
import screenshots
import discord
import base64


# Server ids
guild_ids: List[int] = [706579652734615645, 259431635949322240]

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    print("Ready!")


@slash.slash(
    name="inspect",
    guild_ids=guild_ids,
    description="Generates an image showing the csgo item in-game using the inspect link",
    options=[
        create_option(
            name="url",
            description="The inspect url",
            option_type=3,
            required=True
        )
    ]
)
async def _inspect(ctx: SlashContext, url: str):
    await ctx.defer()
    queue: List[str] = []
    queue += screenshots.queue_inspect(url)
    if 'error' in queue:
        await ctx.send("Invalid URL")
    while not ctx.responded:
        request_id, request = screenshots.request_status(queue)
        status: int = request['response'][request_id]['status']
        if status == 2:
            image_id: int = request['response'][request_id]['images'][0]['id']
            await ctx.send(f'https://cs.deals/csgoScreenshot/{base64.b64encode(str(image_id).encode("ascii")).decode("ascii")}.jpg')
        elif status == 3:
            await ctx.send('Request timed out, please try again.')
        sleep(2)

config = dotenv_values('.env')
client.run(config['CLIENT_TOKEN'])
