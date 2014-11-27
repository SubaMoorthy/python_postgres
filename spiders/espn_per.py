import sys,os
import traceback
from datetime import *
from time import *
from selenium import webdriver
import psycopg2
import ConfigParser



##eliminate duplicates!!!
#insert_team_data(team_name,"{\""+rank+"\",\""+player_name+"\",\""+player_club+"\",\""+yc+"\",\""+rc+"\",\""+points+"\"}")

def insert_team_data(team_name,Largest_Attendance,Lowest_Attendance,Most_Home_Goals,Most_Away_Goals,Largest_Margin_of_Defeat,Largest_Margin_of_Victory,Average_Attendance,Aggregated_Attendance,Longest_Losing_Streak,Longest_Unbeaten_Streak,Longest_Winless_Streak,Longest_Winning_Streak):
    global conn,cur
    try:
        connect_DB()
        sq = "insert into team (team_name,Largest_Attendance,Lowest_Attendance,Most_Home_Goals,Most_Away_Goals,Largest_Margin_of_Victory,Average_Attendance,Aggregated_Attendance,Longest_Losing_Streak,Longest_Unbeaten_Streak,Longest_Winless_Streak,Longest_Winning_Streak,source) values ( '"+team_name+"','"+Largest_Attendance+"','"+Lowest_Attendance+"','"+Most_Home_Goals+"','"+Most_Away_Goals+"','"+Largest_Margin_of_Victory+"','"+Average_Attendance+"','"+Aggregated_Attendance+"','"+Longest_Losing_Streak+"','"+Longest_Unbeaten_Streak+"','"+Longest_Winless_Streak+"','"+Longest_Winning_Streak+"','espnfc');"
        
        cur.execute(sq)
        conn.commit()
    except:
        traceback.print_exc(file=sys.stdout)
        print("data ingestion failure!")
#update database doesn't need to commit

def connect_DB():
    global conn,cur
    CONFIG_FILE = '../Scheduler/config.cfg'
    DB_INFO_SECTION = 'DbInfo'
    config = ConfigParser.ConfigParser()

    config.read(CONFIG_FILE)
    host = config.get(DB_INFO_SECTION, 'host')
    database_name = config.get(DB_INFO_SECTION, 'database_name')
    user = config.get(DB_INFO_SECTION, 'user')
    password = config.get(DB_INFO_SECTION, 'password')
    conn_string = "host=\'"+ host + "\' dbname=\'" + database_name +'\' user=\'' + user + '\' password=\''+ password + '\''
    try:
        conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres' port='5433'")
        cur = conn.cursor()#        s="select * from player"#        cur.execute(s)
        return True
    except:
        traceback.print_exc(file=sys.stdout)
        print "I am unable to connect to the database"
        return False

def IsCrawled(team_name):
    global crawllist
    
    for e in crawllist:
        if(e==team_name):
            return True
    return False


def writefile(team_name, team_info):
    
    f=open(team_name.replace("/","")+".json",'w')
    f.write(team_info.encode('utf8'))
    f.close()


def get_content(xpath):
    global driver,crawllist,faillist
    
    sleep(1)
    element = driver.find_elements_by_xpath(xpath)[0]
    sleep(1)
    element.click()
    
    team_name=element.text
    print(team_name)
    if(IsCrawled(team_name)):
        return
    
    sleep(1)
    ul = driver.find_elements_by_xpath("//*[@id=\"submenu-content-items\"]/ul")[0]
    sleep(1)
    stat = driver.find_element_by_link_text("STATISTICS")
    sleep(1)
    stat.click()
    print(stat.text)
    print(driver.current_url)

    sleep(1)
    peformance_tag=driver.find_elements_by_css_selector("#stats-toggle > ul > li")[0]
    sleep(1)
    peformance_tag.click()

    sleep(1)
    performance_div=driver.find_elements_by_css_selector("#stats-performance > div")

    Largest_Attendance=""
    Lowest_Attendance=""
    Most_Home_Goals=""
    Most_Away_Goals=""
    Largest_Margin_of_Defeat=""
    Largest_Margin_of_Victory=""
    Average_Attendance=""
    Aggregated_Attendance=""
    Longest_Losing_Streak=""
    Longest_Unbeaten_Streak=""
    Longest_Winless_Streak=""
    Longest_Winning_Streak=""
    
    
    for div in performance_div:
        print(div.text)
        print("\n")
        
        if (div.text).find("Largest Attendance")>=0:
            Largest_Attendance = (','.join(((div.text).replace(",","").split("\n"))[1:4]))
            if (div.text).find("Lowest Attendance")>=0:
                Lowest_Attendance = (','.join(((div.text).replace(",","").split("\n"))[5:]))
            else:
                Lowest_Attendance = ""

        elif (div.text).find("Most Home Goals")>=0:
            Most_Home_Goals=(','.join(((div.text).split("\n"))[1:6]))
        
        elif (div.text).find("Most Away Goals")>=0:
            Most_Away_Goals=(','.join(((div.text).split("\n"))[1:6]))
        
        elif (div.text).find("Largest Margin of Victory")>=0:
            Largest_Margin_of_Victory = (','.join(((div.text).split("\n"))[1:6]))
        
        elif (div.text).find("Largest Margin of Defeat")>=0:
            Largest_Margin_of_Defeat = (','.join(((div.text).split("\n"))[1:6]))
        
        elif (div.text).find("Average Attendance")>=0:
            Average_Attendance = ((div.text).split("\n"))[1]
            Average_Attendance = Average_Attendance.replace(",","")
            if (div.text).find("Aggregated Attendance")>=0:
                Aggregated_Attendance = ((div.text).split("\n"))[3]
                Aggregated_Attendance = Aggregated_Attendance.replace(",","")
        elif (div.text).find("Longest Winning Streak")>=0:
            Longest_Winning_Streak = ((div.text).split("\n"))[1]
            if (div.text).find("Longest Unbeaten Streak")>=0:
                Longest_Unbeaten_Streak = ((div.text).split("\n"))[3]
            if (div.text).find("Longest Losing Streak")>=0:
                Longest_Losing_Streak = ((div.text).split("\n"))[5]
            if (div.text).find("Longest Winless Streak")>=0:
                Longest_Winless_Streak = ((div.text).split("\n"))[7]

    jstr= "{ \""+team_name+" performance\": {\"Largest_Attendance\":\""+Largest_Attendance+"\",\"Lowest_Attendance\":\""+Lowest_Attendance+"\",\"Most_Home_Goals\":\""+Most_Home_Goals+"\",\"Most_Away_Goals\":\""+Most_Away_Goals+"\",\"Largest_Margin_of_Defeat\":\""+Largest_Margin_of_Defeat+"\",\"Largest_Margin_of_Victory\":\""+Largest_Margin_of_Victory+"\",\"Average_Attendance\":\""+Average_Attendance+"\",\"Aggregated_Attendance\":\""+Aggregated_Attendance+"\",\"Longest_Losing_Streak\":\""+Longest_Losing_Streak+"\",\"Longest_Unbeaten_Streak\":\""+Longest_Unbeaten_Streak+"\",\"Longest_Winless_Streak\":\""+Longest_Winless_Streak+"\",\"Longest_Winning_Streak\":\""+Longest_Winning_Streak+"\"}}"

    insert_team_data(team_name,Largest_Attendance,Lowest_Attendance,Most_Home_Goals,Most_Away_Goals,Largest_Margin_of_Defeat,Largest_Margin_of_Victory,Average_Attendance,Aggregated_Attendance,Longest_Losing_Streak,Longest_Unbeaten_Streak,Longest_Winless_Streak,Longest_Winning_Streak)

    #writefile(team_name, jstr)
    crawllist.append(team_name)

def crawl(catpath,xpath):
    global driver,crawllist,faillist

    try:
            driver.get('http://www.espnfc.us/')
            sleep(1)
            teams = driver.find_elements_by_xpath("//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]")[0]
            sleep(1)
            teams.click()
            
            sleep(1)
            cat = driver.find_elements_by_xpath(catpath)[0]
            sleep(1)
            cat.click()
            
            get_content(xpath)
    
            for thislink in faillist:
                if thislink == [catpath,xpath]:
                    faillist.remove(thislink)
    
    except:
            traceback.print_exc(file=sys.stdout)
            print("\ncrawl page failure, stop crawling this page...\n")
            
            for thislink in faillist:
                if thislink == [catpath,xpath]:
                    return
            
            faillist.append([catpath,xpath])
#            print(faillist)
            return

def crawl_next(catpath, nextpath, time, xpath):
    global driver,crawllist,faillist
    
    
    try:
            driver.get('http://www.espnfc.us/')
            sleep(1)
            teams = driver.find_elements_by_xpath("//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]")[0]
            sleep(1)
            teams.click()
            
            sleep(1)
            cat = driver.find_elements_by_xpath(catpath)[0]
            sleep(1)
            cat.click()
            
            for i in range(0,time):
                sleep(1)
                next= driver.find_elements_by_xpath(nextpath)[0]
                sleep(1)
                next.click()
        
            get_content(xpath)

            for thislink in faillist:
                if thislink == [catpath,nextpath,time,xpath]:
                    faillist.remove(thislink)
        
    except:
            traceback.print_exc(file=sys.stdout)
            print("\ncrawl page failure, stop crawling this page...\n")
            
            for thislink in faillist:
                if thislink == [catpath,nextpath,time,xpath]:
                    return
    
            faillist.append([catpath,nextpath,time,xpath])
#            print(faillist)
            return


global driver
global crawllist,faillist

crawllist=[]
faillist=[]

driver = webdriver.Chrome('C:/Users/Suba/Downloads/chromedriver_win32')

mls="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/ul/li[4]"

for i in range(1,4):
    for j in range(1,6):
        team="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[4]/div[1]/div/div["+str(i)+"]/div/ul/li["+str(j)+"]";
        crawl(mls, team)

for i in range(1,5):
    team="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[4]/div[1]/div/div[4]/div/ul/li["+str(i)+"]";
    crawl(mls, team)


concacaf="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/ul/li[9]"

for i in range(1,3):
    for j in range(1,6):
        team = "//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[9]/div[1]/div/div["+str(i)+"]/div/ul/li["+str(j)+"]";
        crawl(concacaf, team)

for i in range(1,4):
    team = "//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[9]/div[1]/div/div[3]/div/ul/li["+str(j)+"]";
    crawl(concacaf, team)

top_clubs="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/ul/li[1]"
top_clubs_next = "//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[1]/div[2]/a[2]"

for i in range(1,6):
    team = "//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[1]/div[1]/div/div[5]/div/ul/li["+str(i)+"]"
    crawl_next(top_clubs,top_clubs_next, 1, team)


for i in range(1,5):
    for j in range(1,3):
        team = "//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[1]/div[1]/div/div["+str(i)+"]/div["+str(j)+"]"
        crawl(top_clubs, team)


prem = "//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/ul/li[2]"

for i in range(1,5):
    for j in range(1,6):
        team="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[2]/div[1]/div/div["+str(i)+"]/div/ul/li["+str(j)+"]";
        crawl(prem, team)

la_liga = "//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/ul/li[3]"

for i in range(1,5):
    for j in range(1,6):
        team="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[3]/div[1]/div/div["+str(i)+"]/div/ul/li["+str(j)+"]";
        crawl(la_liga, team)

liga_MX="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/ul/li[5]"

for i in range(1,4):
    for j in range(1,6):
        team="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[5]/div[1]/div/div["+str(i)+"]/div/ul/li["+str(j)+"]";
        crawl(liga_MX, team)

for i in range(1,4):
    team="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[5]/div[1]/div/div[4]/div/ul/li["+str(j)+"]";
    crawl(liga_MX, team)

top_nations="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/ul/li[6]"

for i in range(1,3):
    for j in range(1,3):
        team="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[6]/div[1]/div/div["+str(i)+"]/div["+str(j)+"]"
        crawl(top_nations, team)

for i in range(3,6):
    for j in range(1,6):
        team="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[6]/div[1]/div/div["+str(i)+"]/div/ul/li["+str(j)+"]";
        crawl(top_nations, team)

uefa="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/ul/li[7]"
right="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[7]/div[2]/a[2]"

for i in range(1,6):
    for j in range(1,6):
        team = "//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[7]/div[1]/div/div["+str(i)+"]/div/ul/li["+str(j)+"]";
        crawl(uefa, team)

for i in range(6,11):
    for j in range(1,6):
        team = "//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[7]/div[1]/div/div["+str(i)+"]/div/ul/li["+str(j)+"]";
        crawl_next(uefa,right, 1, team)

for i in range(11,16):
    for j in range(1,6):
        team = "//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[7]/div[1]/div/div["+str(i)+"]/div/ul/li["+str(j)+"]";
        crawl_next(uefa,right, 2, team)

conmebol="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/ul/li[8]"

for i in range(1,3):
    for j in range(1,6):
        team = "//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[8]/div[1]/div/div["+str(i)+"]/div/ul/li["+str(j)+"]"
        crawl(conmebol, team)

caf="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/ul/li[10]"

for i in range(1,4):
    for j in range(1,6):
        team = "//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[10]/div[1]/div/div["+str(i)+"]/div/ul/li["+str(j)+"]";
        crawl(caf,team)

ofc="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/ul/li[11]"
team="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[11]/div[1]/div/div/div/ul/li"
crawl(ofc, team)

afc="//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/ul/li[12]"

for i in range(1,5):
    for j in range(1,6):
        team = "//*[@id=\"desktop-nav-fc\"]/div[2]/div[5]/div/div/div/div/div[12]/div[1]/div/div["+str(i)+"]/div/ul/li["+str(j)+"]";
        crawl(afc, team)

while len(faillist)>0:
    for thisteam in faillist:
        if len(thisteam)==2:
            crawl(thisteam[0],thisteam[1])
        elif len(thisteam)==4:
            crawl_next(thisteam[0],thisteam[1],thisteam[2],thisteam[3])
    print("faillist:")
    print(faillist)
    print("\ncrawllist:")
    print(crawllist)





