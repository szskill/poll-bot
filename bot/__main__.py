import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from .embeds import create_poll_embed, create_help_embed

# Load .env contents into os.environ so we can load the token
# (really, that's actually all we need)
load_dotenv()

# If you don't know what intents are, it's basically a way of telling Discord
# what features of the gateway you are going to be using, a.k.a. reading message
# content, which is what we'll be doing here
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="p!", intents=intents)


@bot.event
async def on_command_error(ctx: commands.Context, err: commands.CommandError) -> None:
    """Handles when a command error is raised."""

    if isinstance(err, commands.MissingRequiredArgument):
        await ctx.reply(embed=create_help_embed(ctx.command))
    elif isinstance(err, commands.CommandNotFound):
        return


@bot.command(name="start-poll")
async def start_poll(ctx: commands.Context, *, text: str) -> None:
    """Starts a poll! 👀

    _How do I even use this command?_
    It's the simplest command.
    `p!start-poll Should pineapple belong on pizza?`
    """

    embed = create_poll_embed(text, ctx.author)

    poll_msg = await ctx.reply(embed=embed)
    await poll_msg.add_reaction("👍")
    await poll_msg.add_reaction("👎")


if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
