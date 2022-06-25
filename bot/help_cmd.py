from __future__ import annotations

import inspect
import random
import hikari
import lightbulb
import miru


def get_help_embed(bot: lightbulb.BotApp) -> hikari.Embed:
    embed = hikari.Embed(color=random.randint(0, 16777215)).set_author(name=bot.get_me().username)
    for _p, plugin in bot.plugins.items():
        embed.add_field(f"{_p} Commands", value=plugin.description or "No description provided")
    embed.set_thumbnail(bot.get_me().display_avatar_url)
    return embed


def get_plugin_embed(plugin: lightbulb.Plugin, context: lightbulb.Context | miru.Context) -> hikari.Embed:
    embed = hikari.Embed(color=random.randint(0, 16777215), description=plugin.description).set_author(
        name=f"{plugin.name.upper()} COMMANDS"
    )
    embed.add_field(
        name="Prefix commands",
        value="\n".join(
            command.name for command in plugin.all_commands if isinstance(command, lightbulb.PrefixCommand)
        ),
        inline=True,
    )
    embed.add_field(
        name="Slash commands",
        value="\n".join(command.name for command in plugin.all_commands if isinstance(command, lightbulb.SlashCommand)),
        inline=True,
    )
    embed.set_footer(f"Requested by {context.user}")
    return embed


class HelpPag(miru.View):
    index: int = 0

    def __init__(self, context: lightbulb.Context) -> None:
        self.lb_context = context
        super().__init__(timeout=60, autodefer=True)

    async def view_check(self, context: miru.Context) -> bool:
        if self.lb_context.author == context.user:
            return True
        return False

    async def change_page(self, context: miru.Context) -> None:
        if self.index == 0:
            return await context.edit_response(
                f"Page `{self.index+1}/{len(self.lb_context.bot.plugins)+1}`", embed=get_help_embed(context.app)
            )
        plugin = [plugin for plugin in self.lb_context.bot.plugins.values()][self.index - 1]
        await context.edit_response(
            f"Page `{self.index+1}/{len(self.lb_context.bot.plugins)+1}`", embed=get_plugin_embed(plugin, context)
        )

    @miru.button(emoji="⬅️", style=hikari.ButtonStyle.PRIMARY)
    async def previous_page(self, _: miru.Button, context: miru.Context) -> None:
        if (self.index) < 1:
            return await context.respond("This is the first page.", flags=hikari.MessageFlag.EPHEMERAL)
        self.index -= 1
        await self.change_page(context)

    @miru.button(emoji="➡️", style=hikari.ButtonStyle.PRIMARY)
    async def next_page(self, _: miru.Button, context: miru.Context) -> None:
        if (self.index + 1) > len(self.lb_context.bot.plugins):
            return await context.respond("This is the last page.", flags=hikari.MessageFlag.EPHEMERAL)
        self.index += 1
        await self.change_page(context)


class Help(lightbulb.BaseHelpCommand):
    def __init__(self, app: lightbulb.BotApp) -> None:
        super().__init__(app)

    async def send_bot_help(self, context: lightbulb.Context) -> None:
        view = HelpPag(context)
        res = await context.respond(
            f"Page `1/{len(context.bot.plugins)+1}`",
            embed=get_help_embed(context.bot),
            components=view.build(),
            reply=True,
        )
        view.start(await res.message())

    async def send_command_help(self, context: lightbulb.Context, command: lightbulb.Command) -> None:
        embed = hikari.Embed(
            color=random.randint(0, 16777215),
            description=f"> {(command.description or inspect.getdoc(command.callback) or 'No description provided')}",
        )
        embed.set_author(name=f"{command.name.upper()} COMMAND")
        embed.add_field("Usage", f"```\n{command.signature}\n```")
        await context.respond(embed=embed)

    async def send_plugin_help(self, context: lightbulb.Context, plugin: lightbulb.Plugin) -> None:
        await context.respond(embed=get_plugin_embed(plugin, context), reply=True)

    async def send_group_help(self, context, group) -> None:
        return await super().send_group_help(context, group)
