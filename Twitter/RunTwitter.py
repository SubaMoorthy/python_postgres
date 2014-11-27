import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import sys
import psycopg2
import time
from psycopg2.extras import RealDictRow
from webcrawler.postgres.populateDB import identify_duplicates

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

myusers = []
otherusers=[]
others = []
actors = []

t=0
count=0
count1=0

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
    cur.execute("SELECT * FROM player where twitter =  true")
    actors = cur.fetchall()
except Exception, e:
    print "Error %s" % e
    sys.exit(1)

flag=0
count=0

for player in actors:
    try:
        actor = player['full_name']
        time.sleep(5)
        c=0
        others=[]
        users = api.search_users(actor)
        for u in users:
            if u.verified == True and u.name == actor:
                myusers.append(u.screen_name)
                count=count+1
                actor.pop(count)
                #break 
            else:
                others.append(u.screen_name)
        if(others!=[]):
            for player in others: 
                time.sleep(6)
                user = api.get_user(player)
                t=user.followers_count
                #count1=count1+1
                #print t
                if c<t:
                    c=t
                    myplayer=player
                    #count1=count1+1
            others=[]
            count1=count1+1
            otherusers.append(myplayer)
    except:
         # print("exception happened!")
         continue           

print " count of verified accounts : " , count
print "    "
print " count of unverified accounts : " , count1
print "     "
# print others
# print "   "
print myusers
print "     "
print otherusers
     
     
time.sleep(5)
for player in myusers:
    time.sleep(6)
    user = api.get_user(player)    
    row_data = {}
    row_data['full_name'] = user.name
    row_data['screen_name'] = user.screen_name
    row_data['twitter_id'] = user.id
    row_data['created'] = user.created_at
    row_data['description'] = user.description
    row_data['num_of_followers'] = user.followers_count
    row_data['num_of_tweets'] = user.statuses_count
    row_data['website_URL'] = user.url   
    row_data['source'] = "twitter"
    identify_duplicates(row_data)
    time.sleep(5)
    timeline = api.user_timeline(screen_name=user.screen_name, include_rts=True, count=1)
    for tweet in timeline:
        #print "some tweet"
        tweet_data = {}
        tweet_data['tweet_id'] = tweet.id
        tweet_data['full_name'] = actor
        tweet_data['tweet'] = tweet.text
        tweet_data['created'] = tweet.created_at
        tweet_data['retweet_count'] = tweet.retweet_count
        tweet_data['retweets'] = tweet.retweeted
        tweet_data['tweet_source'] = tweet.source
        tweet_data['source']  = 'twitter_tweets'
        identify_duplicates(tweet_data)
        
time.sleep(5)
for player in otherusers:
    time.sleep(6)
    user = api.get_user(player)    
    row_data = {}
    row_data['full_name'] = user.name
    row_data['screen_name'] = user.screen_name
    row_data['twitter_id'] = user.id
    row_data['created'] = user.created_at
    row_data['description'] = user.description
    row_data['num_of_followers'] = user.followers_count
    row_data['num_of_tweets'] = user.statuses_count
    row_data['website_URL'] = user.url   
    row_data['source'] = "twitter"
    identify_duplicates(row_data)
    time.sleep(5)
    timeline = api.user_timeline(screen_name=user.screen_name, include_rts=True, count=1)
    for tweet in timeline:
        #print "some tweet"
        tweet_data = {}
        tweet_data['tweet_id'] = tweet.id
        tweet_data['full_name'] = actor
        tweet_data['tweet'] = tweet.text
        tweet_data['created'] = tweet.created_at
        tweet_data['retweet_count'] = tweet.retweet_count
        tweet_data['retweets'] = tweet.retweeted
        tweet_data['tweet_source'] = tweet.source
        tweet_data['source']  = 'twitter_tweets'
        identify_duplicates(tweet_data)
   