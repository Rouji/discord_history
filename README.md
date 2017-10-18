# Discord History Downloader

This script downloads Discord chat history and saves it in a nice text format.

## Installation

There's no installation procedure per se, but this script requires discord.py library. To install it, run

```
$ pip3 install -r requirements.txt
```

## Config file

Config file is a JSON file with the following format:

```
{
    "token": "YOUR_TOKEN",
    "servers": [],
    "bridge_bots": {
        "bot_name": {
            "regex": "^\\*\\*<(?P<user>.*)>\\*\\* (?P<content>.*)$",
            "suffix": ""
        }
    }
}
```

1. `token` (required) is your personal Discord token. Easiest way to get it is to go to Developer Tools in your browser or desktop application. In Developer Tools go to the Application section, and then Storage > LocalStorage > https://discordapp.com. Find the `token` row, and your token will be the value in quotes. **It is very important to NOT SHARE this token with anyone**, as it provides complete access to your Discord account. Your token might change in the future, if this happens, you'll need to update the config file.

2. `servers` (optional) is a list of servers from which to download chat history. E.g. `"servers": ["my_server"]` will only download history from that particular server. If `servers` is empty or omitted, it will download history from all servers. Be careful with this option because some servers can have gigabytes of chat history.

3. `bridge_bots` (optional) is needed to prettify messages from bridge bots. E.g. you have Discord bot that proxies messages to and from some IRC server, and all messages from it look like `irc_bot: <jane> hi john`. You can transform those messages to `jane_irc: hi john`. To do that, add the following bot to the `bridge_bots`:
```
"irc_bot": {
	"regex": "^<(?P<user>.*)> (?P<content>.*)$",
	"suffix": "_irc"
}
```

`regex` is the regular expression to extract remote username and useful message content from bot message, `suffix` is the suffix to append to remote username. Suffix `"_irc"` will transform remote username "jane" to "jane_irc", empty suffix will leave remote username as is.

## Usage

```
$ ./main.py
```

It should create `logs` directory and populate it with logs.

## Known problems

1. The script downloads all history from all servers in memory and only then dumps it on disk. That can be quite memory intensive.
2. There's currently no way to precisely scope what channels to download chat history from, you can only list servers and it will download history from all channels on those servers.
3. Multi-line messages don't look very nice in the result log file.
4. There's a hard limit of 10 million messages per channel, would be nice to move it to config file.
5. Bridged bots configuration is global, so if there are two different bots with same name, one of them won't work.
6. When the script finishes, it produces `RuntimeError: Event loop stopped before Future completed`.

PRs welcome.
