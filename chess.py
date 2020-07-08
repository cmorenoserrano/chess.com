#!/usr/bin/python3
## ----------------------------------------------------------------------------
## Python Dependencies
import os
from copy import deepcopy
import datetime
import urllib
import urllib.request
import requests
import json, argparse
from fpdf import FPDF

## ----------------------------------------------------------------------------
session = requests.Session()

def getUserGames(username):
    #username = "sprocket314"
    baseUrl = "https://api.chess.com/pub/player/" + username + "/games/"
    archivesUrl = baseUrl + "archives"

    #read the archives url and store in a list
    f = urllib.request.urlopen(archivesUrl)
    archives = f.read().decode("utf-8")
    archives = archives.replace("{\"archives\":[\"", "\",\"")
    archivesList = archives.split("\",\"" + baseUrl)
    archivesList[len(archivesList)-1] = archivesList[len(archivesList)-1].rstrip("\"]}")

    #download all the archives
    for i in range(len(archivesList)-1):
        url = baseUrl + archivesList[i+1] + "/pgn"
        filename = archivesList[i+1].replace("/", "-")
        if not os.path.exists("chess_games"):
            os.mkdir("chess_games")
        urllib.request.urlretrieve(url, "chess_games/" + filename + ".pgn") #change
        print(filename + ".pgn has been downloaded.")
    print ("All files have been downloaded.")

def getPlayerMatches(username):
    baseUrl = "https://api.chess.com/pub/player/" + username + "/matches"

    response = session.get(baseUrl)
    matches = response.json()
    #print(matches)
    return matches

def getPlayerStats(username):
    baseUrl = "https://api.chess.com/pub/player/" + username + "/stats"

    response = session.get(baseUrl)
    stats = response.json()
    #print(stats)
    return stats

def getClubMembers(clubname):
    baseUrl = "https://api.chess.com/pub/club/" + clubname + "/members"

    response = session.get(baseUrl)
    members = response.json()
    #print(members)
    return members

def getClubMatches(clubname):
    baseUrl = "https://api.chess.com/pub/club/" + clubname + "/matches"

    response = session.get(baseUrl)
    matches = response.json()
    #print(matches)
    return matches

def getResults(club,members,scope_finished,scope_in_progress):
    #print(scope_finished)
    clubUrl = "https://api.chess.com/pub/club/" + club
    results = {}
    
    for match in scope_finished:
        baseUrl = match["@id"]
        response = session.get(baseUrl)
        team_match = response.json()
        if not os.path.exists("club_matches_finished"):
            os.mkdir("club_matches_finished")
        dumps(team_match,file_name='club_matches_finished/'+match["name"]+'.json')
        for team in team_match["teams"]:
            if team_match["teams"][team]["@id"] == clubUrl:
                for player in team_match["teams"][team]["players"]:
                    if "played_as_black" in player:
                        if player["played_as_black"] == "win" and player["username"] in members:
                            members[player["username"]] += 1
                        if player["played_as_black"] == ("insufficient" or "agreed" or "repetition" or "stalemate" or "50move" or "threecheck" or "timevsinsufficient") and player["username"] in members:
                            members[player["username"]] += 0.5
                    if "played_as_white" in player:
                        if player["played_as_white"] == "win" and player["username"] in members:
                            members[player["username"]] += 1
                        if player["played_as_white"] == ("insufficient" or "agreed" or "repetition" or "stalemate" or "50move" or "threecheck" or "timevsinsufficient") and player["username"] in members:
                            members[player["username"]] += 0.5

    #print(scope_in_progress)
    for match in scope_in_progress:
        baseUrl = match["@id"]
        response = session.get(baseUrl)
        team_match = response.json()
        if not os.path.exists("club_matches_in_progress"):
            os.mkdir("club_matches_in_progress")
        dumps(team_match,file_name='club_matches_in_progress/'+match["name"]+'.json')
        for team in team_match["teams"]:
            if team_match["teams"][team]["@id"] == clubUrl:
                for player in team_match["teams"][team]["players"]:
                    if "played_as_black" in player:
                        if player["played_as_black"] == "win" and player["username"] in members:
                            members[player["username"]] += 1
                        if player["played_as_black"] == ("insufficient" or "agreed" or "repetition" or "stalemate" or "50move" or "threecheck" or "timevsinsufficient") and player["username"] in members:
                            members[player["username"]] += 0.5
                    if "played_as_white" in player:
                        if player["played_as_white"] == "win" and player["username"] in members:
                            members[player["username"]] += 1
                        if player["played_as_white"] == ("insufficient" or "agreed" or "repetition" or "stalemate" or "50move" or "threecheck" or "timevsinsufficient") and player["username"] in members:
                            members[player["username"]] += 0.5

    ranking = []
    for player in members:
        points = [members[player]]
        ranking.append([player] + points)
    ##########################################################################
    ranking.sort(key = lambda ranking : ranking[1], reverse = True)
    ##########################################################################
    #print(ranking)
                            
    results = ranking
    dumps(results,file_name='results.json')
    return results
        
def generateLeagueTable(results, start_date, end_date):
    pdf = PDF()
    pdf.alias_nb_pages()
    #components = final
    header = ['Position','Member','Points']
    data = []
    '''for component in components:
            if component["packageUrl"]["packageUrl"] is not None:
                    current = component["packageUrl"]["packageUrl"]
                    if component["recommendation"] is not None:
                            no_violations = component["recommendation"]["remediation"]["versionChanges"][0]["data"]["component"]["packageUrl"]
                            #non_failing = component["recommendation"]["remediation"]["versionChanges"][1]["data"]["component"]["packageUrl"]
                    else:
                            no_violations = "No recommendation available"
                    aux = [current,no_violations]
                    #aux = [current,no_violations,non_failing]
                    data.append(aux)
                    #print(data)
    '''
    pdf.print_chapter('League Table for Club Daily Matches',"")
    pdf.set_font('Times','',12)
    pdf.set_text_color(0,0,0)
    instructions = "Current standings from "+str(start_date)+" to "+str(end_date)
    pdf.multi_cell(0,7,instructions,0)
    pdf.ln(5)
    pdf.set_font('Times','',12)
    pdf.dynamic_table(header,data)
    pdf.output('./leagueTable.pdf', 'F')
    print("PDF generated -> leagueTable.pdf")




def getArguments():
    global baseUrl
    parser = argparse.ArgumentParser(description='Chess.com API data handling script')
    parser.add_argument('-u','--username', help='Specific username', required=False)
    parser.add_argument('-c','--club', help='Specific club', required=False)
    parser.add_argument('-ug','--userGames', help='Download all archived games for a specified user', action='store_true', required=False)
    parser.add_argument('-m','--clubMembers', help='Download all the members of a club',action='store_true', required=False)
    parser.add_argument('-cm','--clubMatches', help='Download all the club matches', action='store_true', required=False)
    parser.add_argument('-pm','--playerMatches', help='Download all the player matches', action='store_true', required=False)
    parser.add_argument('-d','--dateRange',help='Specify a date range: dd-mm-yyyy:dd-mm-yyyy',required=False)
    parser.add_argument('-r','--report',help='Generate League table report',action='store_true',required=False)
    
    args = vars(parser.parse_args())
    return args
#-----------------------------------------------------------------------------

#---------------------------------

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('team_uk_logo.jpeg', 10, 8, 33)
        # Times bold 15
        self.set_font('Times', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(100, 10, 'League Table', 1, 0, 'C')
        # Line break
        self.ln(20)

        # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Times', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

        #Chapter title
    def chapter_title(self, title):
        # Arial 12
        self.set_font('Times', 'B', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, '%s' % (title), 0, 1, 'L', 1)
        # Line break
        self.ln(0)

        #Chapter body
    def chapter_body(self, content_dict):
        # Times 12
        self.set_font('Times', '', 12)
        # Output justified text
        #self.multi_cell(0, 5, content)
        for field in content_dict:
            self.cell(0, 5, field+": "+content_dict[field], 1, 1)
        # Line break
        self.ln()

        #Print chapter
    def print_chapter(self, title, content):
        self.add_page('L')
        self.chapter_title(title)
        self.chapter_body(content)

    def print_list(self,data):
        self.cell()

    def fancy_table(this,header,data):
        #Colors, line width and bold font
        this.set_fill_color(255,0,0)
        this.set_text_color(255)
        this.set_draw_color(128,0,0)
        this.set_line_width(.3)
        this.set_font('Times','B')
        #Header
        w=[]
        column_no = len(header)
        page_width = 277 #magic number for A4 in mm
        column_width = page_width/column_no
        for i in range(0,column_no):
            w.append(column_width)
        for i in range(0,column_no):
            this.cell(w[i],7,header[i],1,0,'C',1)
        this.ln()
        #Color and font restoration
        this.set_fill_color(224,235,255)
        this.set_text_color(0)
        this.set_font('Times')
        #Data
        fill=0
        #print("This data: ")
        #print(len(data))
        #print(len(w))
        #print(column_no)
        for row in data:
            for i in range(0,column_no):
                this.cell(w[i],6,row[i],'LR',0,'C',fill)
                #print(row[i])
            this.ln()
            fill=not fill
        this.cell(sum(w),0,'','T')

    def dynamic_table(this,header,data):
        #Colors, line width and bold font
        this.set_fill_color(255,0,0)
        this.set_text_color(255)
        this.set_draw_color(128,0,0)
        this.set_line_width(.3)
        this.set_font('Times','B')
        #Header
        w=[]
        column_no = len(header)
        page_width = 277 #magic number for A4 in mm
        column_width = page_width/column_no
        for i in range(0,column_no):
            w.append(column_width)
        for i in range(0,column_no):
            this.cell(w[i],7,header[i],1,0,'C',1)
        this.ln()
        #Color and font restoration
        this.set_fill_color(224,235,255)
        this.set_text_color(0)
        this.set_font('Times')
        #Data
        fill=0
        #print("This data: ")
        #print(len(data))
        #print(len(w))
        #print(column_no)
        for row in data:
            for i in range(0,column_no):
                this.multi_cell(w[i],6,row[i],1,'L',fill)
                fill=not fill
                this.multi_cell(w[i],6,row[i+1],1,'L',fill)
                fill=not fill
                #this.multi_cell(w[i],6,row[i],0,'C',fill)
                #this.cell(w[i],6,row[i],'LR',0,'C',fill)
                #print(row[i])
                this.ln()
        this.cell(sum(w),0,'','T')
        return

#---------------------------------

def output_pdf(pages, filename):
    pdf = FPDF()
    pdf.set_font('Times','B',12)
    for image in pages:
        pdf.add_page('L')
        pdf.set_xy(0,0)
        pdf.image(image, x = None, y = None, w = 0, h = 0, type = '', link = '')
    pdf.output(filename, 'F')
    return


#---------------------------------


#-----------------------------------------------------------------------------
def main():
    username = ""
    club = ""
    scope_finished = {}
    scope_in_progress = {}
    args = getArguments()
    if args["dateRange"]:
        dateRange = args["dateRange"].split(":",1)
        first = dateRange[0].split("-",2)
        #print(first)
        last = dateRange[1].split("-",2)
        start_date = dateRange[0]
        start_epoch = round(datetime.datetime(int(first[2]),int(first[1]),int(first[0])).timestamp())
        #print(start_epoch)
        end_date = dateRange[1]
        end_epoch = round(datetime.datetime(int(last[2]),int(last[1]),int(last[0])).timestamp())
        #print(end_epoch)


    
    if args["username"]:
        username = args["username"]
    if args["club"]:
        club = args["club"]
    if args["userGames"]:
        getUserGames(username)
    if args["clubMembers"]:
        if args["club"]:
            members = getClubMembers(club)
    if args["clubMatches"]:
        if args["club"]:
            matches = getClubMatches(club)
            #print(matches["finished"])
            if args["dateRange"]:
                #print(len(matches["finished"]))
                scope_finished = list(filter(lambda match: (match["start_time"] >= start_epoch) and (match["start_time"] <= end_epoch), matches["finished"]))
                #print(len(scope_finished))
                #print(len(matches["in_progress"]))
                #scope_in_progress = list(filter(lambda match: (match["start_time"] >= start_epoch) and (match["start_time"] <= end_epoch), matches["in_progress"]))
                #print(len(scope_in_progress))
                scope_in_progress = matches["in_progress"]
    if args["playerMatches"]:
        if args["username"]:
            playerMatches = getPlayerMatches(username)
            print(playerMatches)

    if args["report"]:
        if args["club"]:
            if args["dateRange"]:
                members = {}
                clubMembers = getClubMembers(club)
                for member in clubMembers["weekly"]:
                    #print(member)
                    members.update({member["username"] : 0})
                for member in clubMembers["monthly"]:
                    #print(member)
                    members.update({member["username"] : 0})
                for member in clubMembers["all_time"]:
                    #print(member)
                    members.update({member["username"] : 0})
                #print(members)
                matches = getClubMatches(club)
                scope_finished = list(filter(lambda match: (match["start_time"] >= start_epoch) and (match["start_time"] <= end_epoch), matches["finished"]))
                scope_in_progress = matches["in_progress"]
                results = getResults(club,members,scope_finished,scope_in_progress)
                generateLeagueTable(results,start_date,end_date)


  

    #####Present League Table by tiers ranked based on points
    #####Additional features like player of the week, most improved player, top ranking by time control, etc.
    


	
#-----------------------------------------------------------------------------
def pp(c):
    print( json.dumps(c, indent=4) )

def dumps(page, pretty = True, file_name = "results.json"):
    try:
        if pretty: page = json.dumps(page, indent=4)
        with open(file_name,"w+") as file:
            file.write(page)
    finally:
        return page

def handle_resp(resp, root=""):
    if resp.status_code != 200: 
        print(resp.text)
        return None
    node = resp.json()
    if root in node: node = node[root]
    if node == None or len(node) == 0: return None
    return node

def get_url(url, root=""):
    resp = iq_session.get(url)
    return handle_resp(resp, root)

def post_url(url, params, root=""):
    resp = iq_session.post(url, json=params)
    return handle_resp(resp, root)

def get_epoch(epoch_ms):
    dt_ = datetime.datetime.fromtimestamp(epoch_ms/1000)
    return dt_.strftime("%Y-%m-%d %H:%M:%S")

def get_applicationId(publicId):
    url = f'{iq_url}/api/v2/applications?publicId={publicId}'
    apps = get_url(url, "applications")
    if apps == None: return None
    return apps[0]['id']

def get_reportId(applicationId, stageId):
    url = f"{iq_url}/api/v2/reports/applications/{applicationId}"
    reports = get_url(url)
    for report in reports:
        if report["stage"] in stageId:
            return report["reportHtmlUrl"].split("/")[-1]

def get_policy_violations(publicId, reportId):
    url = f'{iq_url}/api/v2/applications/{publicId}/reports/{reportId}/policy'
    return get_url(url)

def get_recommendation(component, applicationId, stageId):
    url = f'{iq_url}/api/v2/components/remediation/application/{applicationId}?stageId={stageId}'
    return post_url(url, component)

def get_last_version(component):
    url = f"{iq_url}/api/v2/components/versions"
    return post_url(url, component)
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

if __name__ == "__main__":
    main()

