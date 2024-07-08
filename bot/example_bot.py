# This example requires the 'message_content' intent.

import discord
import functools
import logging
import random

from keys import BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

logger = logging.getLogger('discord')


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send(f'Hello! {message.author}')

    if message.content.startswith('$roll'):
        count_str, size_str = str(message.content).split()[1].split('d')
        dice_values = []
        for _ in range(int(count_str)):
            dice_values.append(random.randint(1, int(size_str)))

        total = functools.reduce(lambda sum, x: sum+x, dice_values)

        response = f'Rolling {count_str}d{size_str}: {
            ' + '.join(str(value) for value in dice_values)} = {total}'
        await message.channel.send(response)

        logger.info(f'{message.author} sent \'{message.content}\'')
        logger.info(f'responded with \'{response}\'')


client.run(BOT_TOKEN)
