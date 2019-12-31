# Floorball game monitor
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c82f8b283d9045a681cd4b03c03788ec)](https://www.codacy.com/manual/rikard.fahlstrom/floorball-game-monitor?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=RikardFahlstrom/floorball-game-monitor&amp;utm_campaign=Badge_Grade)

## Overview
Since the official iPhone app for the Swedish Floorball association  
do not support push notifications for match events, I created  
my own scraping script that checks for changes in specific match result  
and sends a push notification to a given Slack channel.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

What things you need to install the software and how to install them

*   Python 3.6 or above
*   A Slack app which can post messages to a specific channel based on an incoming webhook

### Installing

Run below to get the necessary libraries, preferably in a virtualenv.

```bash
$ virtualenv -p python3 virtualenv_name
```
```bash
$ source virtualenv_name/bin/activate
```

Then
```bash
$ pip install -r requirements.txt
```

Create the `config.py` in the same directory as `program.py`  
It should contain this information:

```python
slack_token = "xxxxxxxxxx"
```

## Usage
To monitor a the result from a specific game from the command line:
```bash
$ python program.py <game_id> <game_start_time> 
```

To schedule upcoming games via crontab
```bash
* * * * * python3 <absolute_path_to_program.py> <game_id> <game_start_time> 
```
Where
*   `<game_id>` is found in the URL from a specific game detail view
*   `<game_start_time>` is start time of the specific game in format `%Y-%m-%d %H:%M`

Specific example with [this game](https://innebandy.se/statistik/sasong/37/serie/11566/match/503033)
*   crontab schedule `02 19 03 01 *`
*   `<game_id>` is 503033
*   `<game_start_time>` is "2020-01-03 19:00"

Ends up with
```bash
02 19 03 01 * python3 <absolute_path_to_program.py> "503033" "2020-01-03 19:00" 
```

## Contributing

Please open an issue or send a pull request.

## Acknowledgments

*   [README-template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2.js)  - The template I used as a starting point