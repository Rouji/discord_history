#!/usr/bin/env python3

import json
import os
import re

import discord


def format_message(message, bridge_bots):
    content = message.clean_content
    for obj in message.embeds + message.attachments:
        if obj["url"] not in content:
            content += "\n%s" % obj["url"]

    user = message.author.name
    content = content.strip()

    if user in bridge_bots:
        match = re.match(bridge_bots[user]["regex"], content)
        if match:
            user = match.group("user") + bridge_bots[user].get("suffix", "")
            content = match.group("content")

    return "[%s] <%s> %s\n" % (message.timestamp.strftime("%Y-%m-%d %H:%M:%S"), user, content)


def get_history():
    with open("config.json") as f:
        config = json.load(f)

    token = config["token"]
    servers = config.get("servers")
    bridge_bots = config.get("bridge_bots", {})

    os.makedirs("logs", exist_ok=True)

    client = discord.Client()

    async def download_channel(channel, cid):
        messages = []
        print("Fetching %s" % cid)
        async for message in client.logs_from(channel, limit=10000000):
            messages.append(message)

        if not messages:
            return

        messages.sort(key=lambda x: x.timestamp)
        with open("logs/%s.txt" % cid, "w") as f:
            for message in messages:
                f.write(format_message(message, bridge_bots))

    @client.event
    async def on_ready():
        for channel in client.private_channels:
            cid = "private.%s" % "_".join([x.name for x in channel.recipients])
            await download_channel(channel, cid)

        for server in client.servers:
            if servers and server.name not in servers:
                continue

            for channel in server.channels:
                cid = "%s.%s" % (server.name, channel.name)
                await download_channel(channel, cid)


        client.loop.call_later(1, client.loop.stop)

    client.run(token, bot=False)


if __name__ == "__main__":
    get_history()
