# This example requires the 'message_content' intent.

import discord
from discord import app_commands, ui
import functools
import logging
import random

from keys import BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

logger = logging.getLogger('discord')


class PartyInvite(ui.View):
    def __init__(self):
        super().__init__()
        self.character_race = None
        self.character_class = None

    @ui.button(label="Accept your quest?", style=discord.ButtonStyle.success)
    async def accept_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.message.delete()
        await interaction.response.send_message("Create your character", view=CharacterCreationView(), ephemeral=True)


class CharacterCreationView(ui.View):
    def __init__(self):
        super().__init__()
        self.race_option = None
        self.class_option = None

    race_options = [
        discord.SelectOption(label="Dwarf", value="Dwarf"),
        discord.SelectOption(label="Human", value="Human"),
    ]
    class_options = [
        discord.SelectOption(label="Barbarian", value="Barbarian"),
        discord.SelectOption(label="Druid", value="Druid"),

    ]

    @ui.select(cls=ui.Select, options=race_options)
    async def select_race(self, interaction: discord.Interaction, _: ui.Select):
        self.race_option = interaction.data["values"][0]
        await interaction.response.defer()

    @ui.select(cls=ui.Select, options=class_options)
    async def select_class(self, interaction: discord.Interaction, _: ui.Select):
        self.class_option = interaction.data["values"][0]
        await interaction.response.defer()

    @ui.button(label="Confirm Choices")
    async def confirm(self, interaction: discord.Interaction, _: ui.Button):
        await interaction.message.delete()
        await interaction.response.send_message(f"Adventure awaits your {self.race_option} {self.class_option}")


# TODO: Work on fixing this portion
# @tree.command(name="roll", description="roll a number of dice\nUsage: /roll 4d10")
# async def roll(interaction: discord.Interaction):
#     count_str, size_str = str(interaction.message.clean_content).split()[
#         1].split('d')
#     dice_values: list[int] = []
#     for _ in range(int(count_str)):
#         dice_values.append(random.randint(1, int(size_str)))

#     total = functools.reduce(lambda sum, x: sum+x, dice_values)

#     response = f'Rolling {count_str}d{size_str}: {
#         ' + '.join(str(value) for value in dice_values)} = {total}'
#     await interaction.response.send_message(response)

#     logger.info(f'{interaction.message.author} sent \'{
#                 interaction.message.content}\'')
#     logger.info(f'responded with \'{response}\'')


@client.event
async def on_ready():
    await tree.sync()
    print(f'We have logged in as {client.user}')


@tree.context_menu(name="Invite To Party")
async def invite_to_party(interaction: discord.Interaction, member: discord.Member):
    await member.send("You've been invited to join the DnD party.", view=PartyInvite())
    await interaction.response.send_message(f"invited {member.name} to group", ephemeral=True, delete_after=5.)


client.run(BOT_TOKEN)
