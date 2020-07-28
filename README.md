# chess.com - Script to make use of chess.com API

## Usage

This script uses Python 3.7 so the sample commands follow the `python3` pattern instead of the usual `python` because I also program in Python 2. If you only use Python 3, please replace `python3` with `python`.

You can get started with the following help command to display all available options:

`python3 chess.py -h`

This provides the following options:

```
python3 chess.py -h
usage: chess.py [-h] [-u USERNAME] [-c CLUB] [-ug] [-m] [-cm] [-pm] Complete
                [-d DATERANGE] [-r]

Chess.com API data handling script

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME,  --username  USERNAME  Specific username
  -ug,          --userGames           Download all archived games for a specified user
  -c CLUB,      --club      CLUB      Specific club
  -d DATERANGE, --dateRange DATERANGE Specify a date range: dd-mm-yyyy:dd-mm-yyyy
  -r,           --report              Generate League table report
```

Let's say that you want to get all of your PGN games, you just have to run:

`python3 chess.py -u username -ug`

This will download one PGN file per calendar month, containing all of the archived games from the user `username` into a `chess_games` folder inside a `username` folder at the directory from where you are running the script. Each user will have their own folder. 

`python3 chess.py -u username`

Just calling the script with the `-u` switch will create a folder for that user and json files containing the user's details, matches and stats.

`python3 chess.py -c clubname`

Calling the script just with the `-c` switch will create a folder for that club, json files containing the club's details, members, matches and the club's logo.

`python3 chess.py -c clubname -d 01-01-2020:31-01-2020 -r`

If we add the `-r` switch, the script will generate a PDF report for that club for the specified date range in `-d dd-mm-yyyy:dd-mm-yyyy`. In the example, the report will be produced for the month of January 2020 and it will include a Player of the Month feature for that month.
