import sys,os
from bs4 import BeautifulSoup
from bs4 import *
import html5lib,urllib2
import logging
import traceback
import psycopg2
import ConfigParser
#modify 4 places
def insert_player_data(Position,Player_Name,Gender,College,Division,Conference):
    global conn,cur
    try:
        connect_DB()
        Player_Name = Player_Name.replace("'", "  ''  ")
        sq = "insert into player (position_1,full_name,gender,Division,Conference,source) values ( '"+Position+"','"+Player_Name+"','"+Gender+"','"+Division+"','"+Conference+"','topdrawer' )"
        cur.execute(sq)
        conn.commit()
    except:
        traceback.print_exc(file=sys.stdout)
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
        traceback.print_exc(file=sys.stdout)
        #print "I am unable to connect to the database"
        #return False


def craw_page(page_url):

    global headers

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
        
        Position = attlist[2].string
        if Position is None:
            Position = "N/A"
        Player_Name = attlist[0].a.string
        Gender=attlist[1].string
        College = attlist[3].a.string
        Division = attlist[4].string
        Conference = attlist[5].string


#        f.write(("{\"Position\":\""+Position+"\",\"PlayerName\":\""+Player_Name+"\",\"Gender\":\""+Gender+"\",\"College\":\""+College+"\",\"Division\":\""+Division+"\",\"Conference\":\""+Conference+"\"},").encode('utf8'))

        insert_player_data(Position,Player_Name,Gender,College,Division,Conference)
#
#        f.close()
#        f=open("college_female.json",'a')
    return True


#scrapping
def main():
    global headers
#    global f

    
    for j in range(1,6):
        i=0
        while True:
            purl = "http://www.topdrawersoccer.com/search/?area=collegeplayer&genderId=f&divisionId="+str(j)+"&pageNo="+str(i)
            if(not(craw_page(purl))):
                break

            i=i+1
    i=0
    
#    if not(f.closed):
#                f.close()
#            
#    with open("college_female.json", 'rb+') as f:
#                f.seek(-1, os.SEEK_END)
#                f.truncate()
#                f.close()
#    f=open("college_female.json",'a')
#    f.write("]}")
#    f.close()




if __name__ == '__main__':

    global headers
#    global f

#    
#    f=open("college_female.json",'w')
#    f.close()
#    f=open("college_female.json",'a')
#    f.write("{\"players\":[")

    #request headers
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    #enable debugging
    logging.basicConfig(level=logging.DEBUG)

    #print("Scrapping Started......")

    try:
        main()
    except:
        
        traceback.print_exc(file=sys.stdout)
        #print("something is wrong while crawling web page. Incomplete Json file ends")
        
#        if not(f.closed):
#            f.close()
#
#        with open("college_female.json", 'rb+') as f:
#            f.seek(-1, os.SEEK_END)
#            f.truncate()
#            f.close()
#        f=open("college_female.json",'a')
#        f.write("]}")
#        f.close()





