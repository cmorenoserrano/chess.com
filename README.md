# chess.com - Script to make use of chess.com API

## Pre-requisites

The script uses a modified fpdf library in order to pass the logo parameter to the add_page method that then passes it to the header method. If you are not going to use the PDF reporting functionality (`-r` switch), then you do not need to care about this. Otherwise, you will have to replace your local `fpdf.py` with the modified one which is available in this Github repo. If you are in MacOS, the location of the file to be replaced is here: `/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/fpdf/fpdf.py`. This location may vary from case to case.

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

## Docker version

In order to make it easier to use the script without the need of installing Python, or its dependencies, or updating the fpdf libraries with the modified ones, a Docker image gets built automatically with every release with all of that done for you. This docker image is hosted in Docker Hub here: https://hub.docker.com/repository/docker/cmorenoserrano/chess/

First, you must install Docker in your computer (https://docs.docker.com/get-docker/).

Then, you pull the image from the Docker repo:

`docker pull cmorenoserrano/chess:latest`

Then you can run the usual script commands from above, but with docker:

`docker run --name chess --rm -it -v /tmp/chess:/usr/src/app cmorenoserrano/chess:latest chess.py -u sprocket314 -c team-united-kingdom-1 -d 01-06-2020:30-06-2020 -r`

This docker command will use the `cmorenoserrano/chess:latest` image that you pulled from the repo with the docker pull command and run a single Python command, which is to run the chess.py Python script for user sprocket314 (to get all of its details) and then get all of the details for club team-united-kingdom-1 and in addition, run a league table report (with player of the month) for the month of June. This will generate a PDF for this club and time period.

All of the data will be generated inside the container and because we mounted the /tmp/chess folder, all of the data will also be replicated in your local machine inside /tmp/chess. Feel free to update the folder location from /tmp/chess to any other location in your machine.

### Windows users

Windows users will have to update the command with Windows-style path instead:

`docker run --name chess --rm -it -v c:\temp\chess:/usr/src/app cmorenoserrano/chess:latest chess.py -u sprocket314 -c team-united-kingdom-1 -d 01-06-2020:30-06-2020 -r`

Then, all of your data will appear inside c:\temp\chess\. Feel free to update the folder location from c:\temp\chess\ to any other location in your machine.
