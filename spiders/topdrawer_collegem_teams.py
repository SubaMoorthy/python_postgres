import sys
from bs4 import *
import urllib2
import logging
import traceback
import psycopg2
import ConfigParser

def insert_team_data(club,opp,g,ga,sh,sog,sa,fo,co,yc,rc,att):
    global conn,cur
    try:
        connect_DB()
        club = club.replace("'", "  ''  ")
        sq = "insert into team (team_name,goals,shots,r_shots_on_goals,yellow,red,source) values ( '"+club+"',"+g+","+sh+","+sog+","+yc+","+rc+",'topdrawer')"
        cur.execute(sq)
        conn.commit()
    except:
        traceback.print_exc(file=sys.stdout)
        #print("data ingestion failure!")

#update database doesn't need to commit

def connect_DB():
    CONFIG_FILE = 'C:\Users\Suba\workspace\webcrawler_pro\webcrawler\Scheduler\config.cfg'
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
        #traceback.print_exc(file=sys.stdout)
        #print "I am unable to connect to the database"
        return False


def crawl_schedule_score(club,scorelink):
    global headers
    
    
    #print(club+" scores and schedules." )
    
    req = urllib2.Request(url=scorelink,headers=headers)
        
        
    try:
        	handle = urllib2.urlopen(req).read();
    except IOError, e:
        	#print "urlopen failed."
        	return False

    soup = BeautifulSoup(handle, "html5lib")


    firstrow=True
        
        
    if not(len(soup.find_all("table"))>1):
            return
        
#    ssf=open(club.replace("/" , "_")+"_score_schedule.json",'w')
#    ssf.close()
#    ssf=open(club.replace("/" , "_")+"_score_schedule.json",'a')
#    ssf.write("{\""+club+"_score_schedule\":[")

    recordnum=0

    try:
        for mbscore in soup.find_all("table")[1].find("tbody").find_all("tr",recursive=False):
            if firstrow == True:
                firstrow = False
                continue;
            else:
                score=mbscore
                scoreattrs=score.find_all("td", recursive=False)
            
                date_time=scoreattrs[0].string
                #print("datetime: "+str(date_time))
            
            
                opponent=(list(scoreattrs[1].stripped_strings))[0]+" "+scoreattrs[1].find("a").string
                #opponent=str(scoreattrs[1].find("a").last_sibling)+scoreattrs[1].find("a").string#################################str(scoreattrs[1].find("a").last_sibling) is none
                #print("opponent: "+str(opponent))
                
                oppoverall=scoreattrs[2].string######################none, cannot concatnate
                #print("oppoverall: "+str(oppoverall))
            
                score=""
                try:
                    score=scoreattrs[3].find("a").string+scoreattrs[3].find("a").next_sibling
                    #print("score: "+str(score))
                except:
                    return
                    #print("score: "+str(score))
            
                overall=scoreattrs[4].string#
                #print("overall: "+str(overall))
                
                conf=scoreattrs[5].string
                #print("conf: "+str(conf))
            
                info=scoreattrs[6].string.strip(' ').strip('\n').strip(' ').strip('\n').strip(' ')##############################
                #print("info: "+str(info))
                
#                ssf.write(("{\"Date_Time\":\""+str(date_time)+"\",\"Opponent\":\""+str(opponent)+"\",\"Opp.Overall\":\""+str(oppoverall)+"\",\"Score\":\""+str(score)+"\",\"Overall\":\""+str(overall)+"\",\"Conf.\":\""+str(conf)+"\",\"Info\":\""+str(info)+"\"},").encode('utf8'))
#                ssf.close()
#                ssf=open(club.replace("/" , "_")+"_score_schedule.json",'a')

                recordnum=recordnum+1

#        if not(ssf.closed):
#            ssf.close()
#
#        if recordnum<1:
#            os.remove(club.replace("/" , "_")+"_score_schedule.json")
#            return
#        
#        with open(club.replace("/" , "_")+"_score_schedule.json", 'rb+') as ssf:
#            ssf.seek(-1, os.SEEK_END)
#            ssf.truncate()
#            ssf.close()
#
#        ssf=open(club.replace("/" , "_")+"_score_schedule.json",'a')
#        ssf.write("]}")
#        ssf.close()

    except:
        return
        #traceback.print_exc(file=sys.stdout)
        #############there is a problem, what if no record is added at all?????????????
#        if not(ssf.closed):
#            ssf.close()
#        
#        if recordnum<1:
#            os.remove(club.replace("/" , "_")+"_score_schedule.json")
#            return
#        
#        with open(club.replace("/" , "_")+"_score_schedule.json", 'rb+') as ssf:
#            ssf.seek(-1, os.SEEK_END)
#            ssf.truncate()
#            ssf.close()
#        ssf=open(club.replace("/" , "_")+"_score_schedule.json",'a')
#        ssf.write("]}")
#        ssf.close()
        #print("Exception in the middle of crawling, incomplete data in json file "+club.replace("/" , "_")+"_score_schedule.json")



def crawl_stat(club,statlink):

    global headers
    
    #print(club+" stats\n")
    
    req = urllib2.Request(url=statlink,headers=headers)
    
    
    try:
        handle = urllib2.urlopen(req).read();
    except IOError, e:
        #print "urlopen failed."
        return False
    
    soup = BeautifulSoup(handle, "html5lib")


    if not(len(soup.find_all("table"))>1):
            return
#
#    sf=open(club.replace("/" , "_")+"_stat.json",'w')
#    sf.close()
#    sf=open(club.replace("/" , "_")+"_stat.json",'a')
#    sf.write("{\""+club+"_stat\":[")

    try:
        recordnum=0
        for stat in soup.find_all("table")[1].find("tbody").find_all("tr",recursive=False):
    
            statattrs=stat.find_all("td", recursive=False)
            
            '''
            opp="Totals"
            if(len(list(statattrs[0].stripped_strings))>1):
                opp=(list(statattrs[0].stripped_strings))[0]+" "+statattrs[0].find("a").string
                #opp=str(statattrs[0].find("a").last_sibling)+statattrs[0].find("a").string#############################
                #print("opp: "+opp)
            '''
            
            if(len(statattrs)<1):
                break
            
            opp=(list(statattrs[0].stripped_strings))[0]+" "+statattrs[0].find("a").string
            #print("opp: "+str(opp))
            
            g=statattrs[1].string
            #print("g: "+str(g))
            
            ga=statattrs[2].string
            #print("ga: "+str(ga))
            
            sh=statattrs[3].string
            #print("sh: "+str(sh))
            
            sog=statattrs[4].string
            #print("sog: "+str(sog))
            
            sa=statattrs[5].string
            #print("sa: "+str(sa))
            
            fo=statattrs[6].string
            #print("fo: "+str(fo))
            
            co=statattrs[7].string
            #print("co: "+str(co))
            
            yc=statattrs[8].string
            #print("yc: "+str(yc))
            
            rc=statattrs[9].string
            #print("rc: "+str(rc))
            
            att=statattrs[10].string
            #print("att: "+str(att))

#            sf.write(("{\"Opp.\":\""+str(opp)+"\",\"G\":\""+str(g)+"\",\"GA\":\""+str(ga)+"\",\"SH\":\""+str(sh)+"\",\"SOG\":\""+str(sog)+"\",\"SA\":\""+str(sa)+"\",\"FO\":\""+str(fo)+"\",\"CO\":\""+str(co)+"\",\"YC\":\""+str(yc)+"\", \"RC\":\""+str(rc)+"\",\"Att\":\""+str(att)+"\"},").encode('utf8'))
            insert_team_data(club,str(opp),str(g),str(ga),str(sh),str(sog),str(sa),str(fo),str(co),str(yc),str(rc),str(att))
            
#            sf.close()
            recordnum=recordnum+1
#            sf=open(club.replace("/" , "_")+"_stat.json",'a')
#
#        if not(sf.closed):
#            sf.close()
#        
#        if recordnum<1:
#            os.remove(club.replace("/" , "_")+"_stat.json")
#            return
#
#        with open(club.replace("/" , "_")+"_stat.json", 'rb+') as sf:
#            sf.seek(-1, os.SEEK_END)
#            sf.truncate()
#            sf.close()
#        sf=  open(club.replace("/" , "_")+"_stat.json",'a')
#        sf.write("]}")
#        sf.close()
    except:
        return
        #traceback.print_exc(file=sys.stdout)
#        if not(sf.closed):
#            sf.close()
#        
#        if recordnum<1:
#            os.remove(club.replace("/" , "_")+"_stat.json")
#            return
#
#        with open(club.replace("/" , "_")+"_stat.json", 'rb+') as sf:
#            sf.seek(-1, os.SEEK_END)
#            sf.truncate()
#            sf.close()
#        sf = open(club.replace("/" , "_")+"_stat.json",'a')
#        sf.write("]}")
#        sf.close()
        #print("Exception in the middle of crawling, incomplete data in json file "+club.replace("/" , "_")+"_stat.json");

def main():
    
    global headers
    
    #page number
    i=5

    while i>=1:
        
	# request the pagearg1
    
        collegeman="http://www.topdrawersoccer.com/college-soccer/teams/men/divisionid-"+str(i);
        
    	req = urllib2.Request(url=collegeman,headers=headers)
    
        
    	try:
        	handle = urllib2.urlopen(req).read();
    	except IOError, e:
        	#print "urlopen failed."
        	return False
        
        soup = BeautifulSoup(handle, "html5lib")

    
        for loctable in soup.find_all("table"):
            for mbteam in loctable.find("tbody").find_all("tr",recursive=False):
                if mbteam.has_attr('class'):
                    team=mbteam
                    
                    #print(player)
                    attlist=team.find_all("td",recursive=False)
                    club=attlist[0].a.string
                    clublink="http://www.topdrawersoccer.com"+attlist[0].a["href"]
        
                    teamdata=attlist[1].find_all("a", recursive=False)
                    scorelink="http://www.topdrawersoccer.com"+teamdata[0]["href"]
                    statlink="http://www.topdrawersoccer.com"+teamdata[1]["href"]
                    schedulelink="http://www.topdrawersoccer.com"+teamdata[2]["href"]   ###usuall same as scorelink
        
                    crawl_schedule_score(club,scorelink)
                    crawl_stat(club,statlink)

            
        #print("college man, div = "+str(i))
        i=i-1


if __name__ == '__main__':

    global headers

    #request headers
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    #enable debugging
    logging.basicConfig(level=logging.DEBUG)
    
    #print("Scrapping Started......\n")

    try:
        main()

    except:
        traceback.print_exc(file=sys.stdout)
        #print("error in main().")



