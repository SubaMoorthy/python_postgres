import sys,os
from bs4 import BeautifulSoup
from bs4 import *
import html5lib,urllib2
import logging
import traceback
import psycopg2
import ConfigParser
def insert_player_data(Position,Player_Name,Club,Age,Heightin,Heightstr,Weight,Country,Status):
    global conn,cur
    try:
        connect_DB()
        Player_Name = Player_Name.replace("'", "  ''  ")
        Club = Club.replace("'", "  ''  ")
        if Weight == '':
           sq = "insert into player (position_1,full_name,age,heightin,height,country,status,source) values ( '"+Position+"','"+Player_Name+"',"+Age+",'"+Heightin.replace("'",",")+"',"+Heightstr+",'"+Country+"','"+Status+"','mls' )"
        else:   
            sq = "insert into player (position_1,full_name,age,heightin,height,weight,country,status,source) values ( '"+Position+"','"+Player_Name+"',"+Age+",'"+Heightin.replace("'",",")+"',"+Heightstr+","+Weight+",'"+Country+"','"+Status+"','mls' )"
        cur.execute(sq)
        conn.commit()
    except:
        return
        #traceback.print_exc(file=sys.stdout)
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

def writefile(jfilename,jstr):
    f=open(jfilename,'w')
    f.write(jstr.encode("utf-8"))
    f.close()

#scrapping
def main():
    global headers
    
    #page number
    i=0

    while True:
        jstr="{\"players\":["
        
    	req = urllib2.Request(url="http://www.mlssoccer.com/players?page="+str(i),headers=headers)
        
    	try:
        	handle = urllib2.urlopen(req).read();
    	except IOError, e:
        	#print "url open mistake."
        	return True
        
        soup = BeautifulSoup(handle, "html5lib")
        if (not(soup.find("a",   attrs={"title": "Go to next page"}))):
            return
    
        for player in soup.find("table").find("tbody").find_all("tr"):
            #print(player)
            attlist=player.find_all("td",recursive=False)
    
            Position = attlist[1].string.strip(' ').strip('\n').strip(' ')   #maybe you can do better here
            Player_Name = attlist[2].a.string.strip(' ')
            Club = attlist[3].string.strip(' ').strip('\n').strip(' ')
            Age = attlist[4].string.strip(' ').strip('\n').strip(' ')
            Heightin = attlist[5].string.strip(' ').strip('\n').strip(' ').strip("\"")
            
            hf=0
            hi=0
            height=0
            try:
                hf = float(Heightin.split(' ')[0].strip('\''))
                hi = float(Heightin.split(' ')[1].strip('\"'))
                Height = (hf*12+hi)* 2.54 #height is a value not a character
            except:
                try:
                    hf = float(Heightin.strip('\''))
                    Height = (hf*12)* 2.54 #height is a value not a character
                except:
                    Height="N/A"
            
            if Height<10.0 and Height != "N/A":
                Height="N/A"
            Weight = attlist[6].string.strip(' ').strip('\n').strip(' ')
            Country = attlist[7].string.strip(' ').strip('\n').strip(' ')
            Status = attlist[8].string.strip(' ').strip('\n').strip(' ')
            
            insert_player_data(Position,Player_Name,Club,Age,Heightin,str(Height),Weight,Country,Status)
            jstr=jstr+"{\"Position\":\""+Position+"\",\"PlayerName\":\""+Player_Name+"\",\"Club\":\""+Club+"\",\"Age\":\""+Age+"\",\"Heightin\":\""+Heightin+"\",\"Height\":\""+str(Height)+"\",\"Weight\":\""+Weight+"\",\"Country\":\""+Country+"\",\"Status\":\""+Status+"\"},"
                
        jstr=jstr.strip(",")+"]}"
        i=i+1


if __name__ == '__main__':

    global headers
    
    #request headers
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    #enable debugging
    logging.basicConfig(level=logging.DEBUG)

    main()

