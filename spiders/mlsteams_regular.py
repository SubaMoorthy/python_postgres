import sys
from bs4 import *
import urllib2
import logging
import traceback
import psycopg2
import ConfigParser

def insert_team_data(year,team_name,gp,g,a,sht,sog,fc,fs,off,ck,pkg,pka):
    global conn,cur
    try:
        connect_DB()
        sq = "insert into team (year,team_name,games_played,goals,r_assists,r_shots,r_shots_on_goals,r_fouls_committed,r_fouls_suffered,r_offsides,r_corner_kick,r_penality_kick_goals,r_penality_kick_attempts,source) values ( "+year+",'"+team_name+"',"+gp+","+g+","+a+","+sht+","+sog+","+fc+","+fs+","+off+","+ck+","+pkg+","+pka+",'mls')"
        cur.execute(sq)
        conn.commit()
    except:
        traceback.print_exc(file=sys.stdout)
        #print("data ingestion failure!")

#update database doesn't need to commit

def connect_DB():
    CONFIG_FILE = '../Scheduler/config.cfg'
    DB_INFO_SECTION = 'DbInfo'
    config = ConfigParser.ConfigParser()

    config.read(CONFIG_FILE)
    host = config.get(DB_INFO_SECTION, 'host')
    database_name = config.get(DB_INFO_SECTION, 'database_name')
    user = config.get(DB_INFO_SECTION, 'user')
    password = config.get(DB_INFO_SECTION, 'password')
    conn_string = "host=\'"+ host + "\' dbname=\'" + database_name +'\' user=\'' + user + '\' password=\''+ password + '\''
    
    global conn,cur
    try:
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()#        s="select * from player"#        cur.execute(s)
        return True
    except:
        traceback.print_exc(file=sys.stdout)
        #print "I am unable to connect to the database"
        return False

#scrapping
def main():
    
    global headers
    global jstr
    
    #page number
    i=2014

    while i>=1996:
    
        reg="http://www.mlssoccer.com/stats/team?season_year="+ str(i)+"&season_type=REG&op=Search&form_id=mls_stats_team_form"
        #ps="http://www.mlssoccer.com/stats/team?season_year="+ str(i)+"&season_type=PS&op=Search&form_id=mls_stats_team_form"
        ######please crawl this link in another file
        
    	req = urllib2.Request(url=reg,headers=headers)
    
        
    	try:
        	handle = urllib2.urlopen(req).read();
    	except IOError, e:
        	#print "urlopen failed."
        	return False
        
        soup = BeautifulSoup(handle, "html5lib")

    
        for team in soup.find("table").find("tbody").find_all("tr"):
            
            attlist=team.find_all("td",recursive=False)
            
            club=attlist[0].string
            gp=attlist[1].string
            g=attlist[2].string
            a=attlist[3].string
            sht=attlist[4].string
            sog=attlist[5].string
            fc=attlist[6].string
            fs=attlist[7].string
            off=attlist[8].string
            ck=attlist[9].string
            pkg=attlist[10].string
            pka=attlist[11].string
            

            jstr=jstr+"{\"Year\":\""+str(i)+"\",\"Club\":\""+club+"\",\"GP\":\""+gp+"\",\"G\":\""+g+"\",\"A\":\""+a+"\",\"SHT\":\""+sht+"\",\"SOG\":\""+sog+"\",\"FC\":\""+fc+"\",\"FS\":\""+fs+"\",\"OFF\":\""+off+"\", \"CK\":\""+ck+"\",\"PKG\":\""+pkg+"\",\"PKA\": \""+pka+"\"},"
        
            insert_team_data(str(i),club,gp,g,a,sht,sog,fc,fs,off,ck,pkg,pka)
            
        i=i-1


if __name__ == '__main__':

    global headers,jstr
    
    jstr="{\"teams_regular_season\":["
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    logging.basicConfig(level=logging.DEBUG)
    
    try:
        main()
        jstr=jstr.strip(",")+"]}"
    except:
        print("Exception in the middle of crawling.")
        jstr=jstr.strip(",")+"]}"




