import asyncio
import os

import lightbulb
import uvicorn
import dotenv

from .web import web_app
from .embeds import create_help_embed, create_poll_embed

# Load .env contents into os.environ, so we can grab the token
dotenv.load_dotenv()

bot = lightbulb.BotApp(os.getenv("TOKEN"), "p!")


@bot.command
@lightbulb.option("text", "The poll text? Very obvious.", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.set_help(docstring=True)
@lightbulb.command("start-poll", "Starts a poll.")
@lightbulb.implements(lightbulb.PrefixCommand)
async def start_poll(ctx: lightbulb.Context) -> None:
    """Starts a poll!

    _How do I even use this command?_
    It's the simplest command.
    `p!start-poll Should pineapple belong on pizza?`
    """

    poll_msg = await (await ctx.respond(embed=create_poll_embed(ctx.options.text, ctx.member))).message()
    await poll_msg.add_reaction("👍")
    await poll_msg.add_reaction("👎")


@bot.listen(lightbulb.CommandErrorEvent)
async def on_command_error(event: lightbulb.CommandErrorEvent) -> None:
    cause = event.exception.__cause__ or event.exception

    if isinstance(cause, lightbulb.NotEnoughArguments):
        await event.context.respond(embed=create_help_embed(event.context.command))
    else:
        raise cause


async def main() -> None:
    await asyncio.gather(
        bot.start(),
        uvicorn.Server(uvicorn.Config(web_app, port=3000)).serve(),
    )


asyncio.run(main())
