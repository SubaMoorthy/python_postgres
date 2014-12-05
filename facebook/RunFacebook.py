import getFacebookData
import psycopg2
import facebook
import sys
from psycopg2.extras import RealDictRow

def main():
	getFacebookData.setEncode('utf-8')

	authorizer = getFacebookData.Authorizer()
	access_token = authorizer.get_access_token()
	graph = facebook.GraphAPI(access_token)

	# database cursor
	con = None
	playerList = None
	try:
		HOSTNAME = 'localhost'
		DBNAME = 'webscraping'
		USER = 'postgres'
		PASSWORD = 'postgres'
		conn_string = "host=\'"+ HOSTNAME + "\' dbname=\'" + DBNAME +'\' user=\'' + USER + '\' password=\''+ PASSWORD + '\''
		con = psycopg2.connect(conn_string)
		con.cursor_factory = RealDictRow
		cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
		cur.execute("SELECT * FROM players where facebook = true")
		playerList = cur.fetchall()
	except Exception, e:
		print "Error %s" % e
		sys.exit(1)

	for player in playerList:
		name = player['name']
		team =  None
		searchAgent = getFacebookData.SearchParser(graph,name,team)
		pageChecker = getFacebookData.correctPageChecker(graph)
		find = False
		correctId = None
		result = {}
		while True:
			page = searchAgent.pop()
			if page == None:
				break
			if page['category'] == 'Athlete':
				verifyAgent = getFacebookData.VerifiedPageChecker(graph,page['id'])
				if verifyAgent.isVerified():
					correctId = page['id']
					find = True
					break
				else:
					pageChecker.load(page['id'],team)
					if pageChecker.isCorrect():
						correctId = page['id']
						find = True
						break
		if not find:
			#print "Cann't find Player"
			continue
		pageAgent = getFacebookData.pageParser(graph,correctId)
		pageInfo = pageAgent.parse()
		#print pageInfo
		postAgent = getFacebookData.postsParser(graph,correctId)
		postInfo = postAgent.parse()
		#print postInfo
		result['full_name'] = name
		result['facebook_id'] = correctId
		if 'likes' in pageInfo:
			result['likes'] = pageInfo['likes']
		if 'talking_about_count' in pageInfo:
			result['talking_about'] = pageInfo['talking_about_count']
		if 'count' in postInfo:
			result['post_count'] = postInfo['count']
		if 'post_ids'  in postInfo:
			result['post_ids'] = postInfo['post_ids']
		#print result
		insert_into_FBTable('facebook',result);
	
def insert_into_FBTable(tablename, result):
	row_data =  result
	#print (row_data)
	column_data = ''
	column_name = ''
	for key in row_data:
		column_data += '%(' +key + ')s' + ","
		column_name += key + ','
        #print('end')
	column_data = column_data[0:-1]
	column_name = column_name[0:-1]
	connectDB()
	if  tablename == "facebook":
		fb_cur.execute("SELECT *  FROM FACEBOOK WHERE FACEBOOK_ID = '" + result['facebook_id']+ "'")
		duplicate_rows = fb_cur.fetchall()
        #print(cursor.rowcount)
        if fb_cur.rowcount > 0:
        	fb_cur.execute("DELETE FROM FACEBOOK WHERE FACEBOOK_ID = '" +result['facebook_id'] +"'")
	if tablename == "facebook_posts":
   		posts_cur.execute("SELECT *  FROM FACEBOOK_POSTS WHERE POST_ID = '" + result['post_id']+ "'")
		duplicate_rows = posts_cur.fetchall()
        if posts_cur.rowcount > 0:
        	posts_cur.execute("DELETE FROM FACEBOOK_POSTS WHERE POST_ID = '" +result['post_id'] +"'")
	insert_cur.execute("INSERT INTO " + tablename+"("+ column_name+")  VALUES ("+ column_data +")", row_data)
	insert_con.commit()

def connectDB():
	HOSTNAME = 'localhost'
	DBNAME = 'webscraping'
	USER = 'postgres'
	PASSWORD = 'postgres'
	conn_string = "host=\'"+ HOSTNAME + "\' dbname=\'" + DBNAME +'\' user=\'' + USER + '\' password=\''+ PASSWORD + '\''
	global insert_con
	global insert_cur
	global fb_cur
	global posts_cur
	insert_con = psycopg2.connect(conn_string)
	insert_cur = insert_con.cursor()
	fb_cur = insert_con.cursor()
	posts_cur = insert_con.cursor()
	
if __name__ == '__main__':
	main()