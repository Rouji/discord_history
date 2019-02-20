# Discord History Downloader
This script downloads Discord chat history and outputs it as JSON. The primary use case is to save history from selected important channels to be able to access and search it locally. **Requires Python 3.6+**.

## Installation
```
$ pip3 install -r requirements.txt
```

## Usage
```
$ ./main.py -h
usage: main.py [-h] [-s SERVER] [-c CHANNEL] [-m MAX_MESSAGES_PER_CHANNEL]
               [--debug]
               token

Download discord chat history as (streamed) json

positional arguments:
  token                 Your discord token

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Python regex(es) matching server names to be included.
                        If none specified, all servers will be downloaded. PMs
                        are assigned the server name "__private".
  -c CHANNEL, --channel CHANNEL
                        Python regex(es) matching channel names to be
                        included. If none specified, all channels will be
                        downloaded.
  -m MAX_MESSAGES_PER_CHANNEL, --max-messages-per-channel MAX_MESSAGES_PER_CHANNEL
                        Maximum number of messages to get per channel.
  --debug               set logging level to DEBUG
```
For further filtering, sorting, formatting, etc. use `jq` and friends.  
**Note**: Messages are not guaranteed to be in chronological (or really any) order.
