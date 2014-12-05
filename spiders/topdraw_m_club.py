import sys
from bs4 import *
import urllib2
import logging
import traceback
import psycopg2
import ConfigParser

#modify 4 places
def insert_player_data(Position,Player_Name,Gender,College,Division,Conference):
    global conn,cur
    try:
        Player_Name = Player_Name.replace("'", "  ''  ")
        connect_DB()
        sq = "insert into player (position_1,full_name,gender,Division,Conference,source) values ( '"+Position+"','"+Player_Name+"','"+Gender+"','"+Division+"','"+Conference+"','topdrawer club' )"
        cur.execute(sq)
        conn.commit()
    except:
        return
        #traceback.print_exc(file=sys.stdout)
        #print("data ingestion failure!")


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
        cur = conn.cursor()
        return True
    except:
        #traceback.print_exc(file=sys.stdout)
        #print "I am unable to connect to the database"
        return False

def craw_page(page_url):

    global headers
#    global f

    req = urllib2.Request(url=page_url,headers=headers)
    
    try:
        handle = urllib2.urlopen(req).read();
    except IOError, e:
        #print "maybe this page is the end."
        return False
    
    soup = BeautifulSoup(handle, "html5lib")


    try:
        prows=soup.find("table").find("tbody").find_all("tr")
        if (prows is None) or (len(prows)==0):
            #print("number of rows is 0, return False here.")##########################
            return False
    except:
        return False

    for player in soup.find("table").find("tbody").find_all("tr"):
        #print(player)
        attlist=player.find_all("td",recursive=False)
        
        try:
            Position = attlist[2].string
            Position=str(Position)
        except:
            Position = "N/A"
        try:
            Player_Name = attlist[0].a.string
            Player_Name=str(Player_Name)
        except:
            Player_Name = "N/A"
        try:
            Gender=attlist[1].string
            Gender=str(Gender)
        except:
            Gender = "N/A"
        try:
            College = attlist[3].a.string
            College=str(College)
        except:
            College = "N/A"
        try:
            Division = attlist[4].string
            Division=str(Division)
        except:
            Division = "N/A"
        try:
            Conference = attlist[5].string
            Conference=str(Conference)
        except:
            Conference = "N/A"
        


#        f.write(("{\"Position\":\""+Position+"\",\"PlayerName\":\""+Player_Name+"\",\"Gender\":\""+Gender+"\",\"College\":\""+College+"\",\"Division\":\""+Division+"\",\"Conference\":\""+Conference+"\"},").encode('utf8'))
        insert_player_data(Position,Player_Name,Gender,College,Division,Conference)

#        f.close()
#        f=open("club_male.json",'a')
    return True


#scrapping
def main():
    global headers
#    global f

    i=0
    while True:
            purl = "http://www.topdrawersoccer.com/search/?area=clubplayer&genderId=m&pageNo="+str(i)
            if(not(craw_page(purl))):
                break
            i=i+1
            
    #no exception area
#    if not(f.closed):
#                f.close()
#            
#    with open("club_male.json", 'rb+') as f:
#                f.seek(-1, os.SEEK_END)
#                f.truncate()
#                f.close()
#    f=open("club_male.json",'a')
#    f.write("]}")
#    f.close()




if __name__ == '__main__':

    global headers
#    global f

    
#    f=open("club_male.json",'w')
#    f.close()
#    f=open("club_male.json",'a')
#    f.write("{\"players\":[")

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    #enable debugging
    logging.basicConfig(level=logging.DEBUG)

    try:
        main()
    except:
        
        traceback.print_exc(file=sys.stdout)
        
#        if not(f.closed):
#            f.close()
#
#        with open("club_male.json", 'rb+') as f:
#            f.seek(-1, os.SEEK_END)
#            f.truncate()
#            f.close()
#        f=open("club_male.json",'a')
#        f.write("]}")
#        f.close()





