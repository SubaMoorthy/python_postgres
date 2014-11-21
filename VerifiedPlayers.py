import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import sys
import psycopg2
import time
from psycopg2.extras import RealDictRow
from time import sleep

TWITTER_APP_KEY = 'jdlA1VpJnFDdxvfbBYW0yCHaQ' 
TWITTER_APP_KEY_SECRET = 'NDfP4m6eig8Xr2L7TuS3FbQ5uTIj2BwGIqddORfjMxrJf1hOyg' 
TWITTER_ACCESS_TOKEN = '113962350-sQyC6zAwQbMZ61TDfB3ZxOfB1MGsEgXq348M5fwC'
TWITTER_ACCESS_TOKEN_SECRET = '7TJj7YYTWIoW7sx0WWi6FKEQbiIlhXi1dCKijprcQr5Bt'


class TweetListener(StreamListener):
   

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(TWITTER_APP_KEY,TWITTER_APP_KEY_SECRET)
api = tweepy.API(auth)

auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitterStream = Stream(auth,TweetListener())

#l=0
myusers = []
otherusers=[]
actors = None
con = None
global insert_cur
try:
    HOSTNAME = 'localhost'
    DBNAME = 'webscraping'
    USER = 'postgres'
    PASSWORD = 'postgres'
    conn_string = "host=\'"+ HOSTNAME + "\' dbname=\'" + DBNAME +'\' user=\'' + USER + '\' password=\''+ PASSWORD + '\''
    con = psycopg2.connect(conn_string)
    con.cursor_factory = RealDictRow
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    insert_cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM player")
    actors = cur.fetchall()
except Exception, e:
    print "Error %s" % e
    sys.exit(1)

#print actors
print "  "
#print len(actors)
#print l

flag=0
count=0

for player in actors:
     #try:
         actor = player['full_name']
         print actor
         time.sleep(5)
         users = api.search_users(actor)
         print "users search done"
         print  len(users)
         for  u in users:
             if u.verified == True and u.name == actor:
                 player = u.screen_name
                 time.sleep(5)
                 user = api.get_user(player)
                 print "done"
                 row_data = {}
                 row_data['full_name'] = user.name
                 row_data['screen_name'] = user.screen_name
                 row_data['twitter_id'] = user.id
                 row_data['created'] = user.created_at
                 row_data['description'] = user.description
                 row_data['num_of_followers'] = user.followers_count
                 row_data['num_of_tweets'] = user.statuses_count
                 row_data['website_URL'] = user.url
                 print row_data
                 column_data = ''
                 column_name = ''
                 tablename = "twitter"
                 for key in row_data:
                    column_data += '%(' +key + ')s' + ","
                    column_name += key + ','
                    print('end')
                 column_data = column_data[0:-1]
                 column_name = column_name[0:-1]
                 print(column_data)
                 insert_cur.execute("INSERT INTO " + tablename+"("+ column_name+")  VALUES ("+ column_data +")", row_data)
                 con.commit()    
                 #insert_into_twitter('twitter', row_data)
                 time.sleep(5)
                 timeline = api.user_timeline(screen_name=user.screen_name, include_rts=True, count=1)
                 print "got timeline"
                 print len(timeline)
                 for tweet in timeline:
                     print "some tweet"
                     tweet_data = {}
                     tweet_data['tweet_id'] = tweet.id
                     tweet_data['full_name'] = actor
                     tweet_data['tweet'] = tweet.text
                     tweet_data['created'] = tweet.created_at
                     tweet_data['retweet_count'] = tweet.retweet_count
                     tweet_data['retweets'] = tweet.retweeted
                     tweet_data['source'] = tweet.source
                     tablename = 'twitter_tweets'
                     column_data = ''
                     column_name = ''
                     for key in tweet_data:
                        column_data += '%(' +key + ')s' + ","
                        column_name += key + ','
                     print('end')
                     column_data = column_data[0:-1]
                     column_name = column_name[0:-1]
                     print "tweet table"
                     print(column_data)
                     insert_cur.execute("INSERT INTO " + tablename+"("+ column_name+")  VALUES ("+ column_data +")", tweet_data)
                     con.commit()    
                 count+=1
             else:
                print "unverified account"
                otherusers.append(u.screen_name)
                flag+=1
     #except:
         print "exception!!"
         
         
def insert_into_twitter(tablename, result):
        row_data =  result
        print (row_data)
        column_data = ''
        column_name = ''
        for key in row_data:
            column_data += '%(' +key + ')s' + ","
            column_name += key + ','
            #print('end')
        column_data = column_data[0:-1]
        column_name = column_name[0:-1]
        print(column_data)
        insert_cur.execute("INSERT INTO " + tablename+"("+ column_name+")  VALUES ("+ column_data +")", row_data)
        con.commit()    
