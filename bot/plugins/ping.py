import lightbulb

plugin = lightbulb.Plugin("Ping", "This plugin has the ping command.")


@plugin.command
@lightbulb.command("ping", "pong")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def _ping(context: lightbulb.Context):
    await context.respond(f"Pong `{(context.bot.heartbeat_latency*1000):.2f}ms`")


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)
