from  key_change import custom_dictionary
import psycopg2
from psycopg2.extras import RealDictRow
import string


integer_values = ['duplicate','weight', 'yellow', 'red', 'assist', 'age', 'fouls', 'shots', 'games_played', 'goals', 'minutes', 'points', 'register_num',  'wins', 'losses','ties','games_for',
                   'games_against', 'home_wins','home_losses','home_ties','home_games_for','home_games_against','away_wins','away_losses', 'away_ties','away_games_for','away_games_against',
                   'home_games_played', 'home_points', 'away_games_played', 'away_points', 'goal_difference', 'home_goal_difference', 'away_goal_difference', 'streaks', 'home_streaks',
                   'away_streaks'];
float_values = ['height']

def change_dict_key(data, name):
    row  =  dict(data)
    #print(row)
    for key in row.keys():
        try:
            new_key = key.replace(key,custom_dictionary[key])
            if new_key != key:
                row[new_key] = row[key]
                del row[key]
        except: 
            pass
    row['source'] = name
    if name == 'WhoscoredTeamForm3' or name == 'WhoscoredTeamForm6' or name == 'WhoscoredTeamPerformances' or name == 'WhoscoredTeamStreaks':
        row['source'] = 'WhoScored'
    row['duplicate'] = '0'
    #print(row)
    clean_rowdata(row, name)

def clean_rowdata(row, name):
    if row['source'] == 'NASLPlayer' or row['source'] == 'SBNationPlayer' or row['source'] == 'USLPlayerStat' or row['source'] == 'USLPlayerRos':
        if  'full_name' in row:
            row['first_name'] = ''
            row['last_name'] = ''
            row['middle_name'] = ''
            num_of_spaces = row['full_name'].count(' ')
            split_string = row['full_name'].split(' ')
            if num_of_spaces == 0: 
                row['first_name'] = row['full_name']
            if num_of_spaces == 1:
                row['first_name'] = split_string[0]
                row['last_name'] = split_string[1]
            if num_of_spaces == 2:
                row['first_name'] = split_string[0]
                row['last_name'] = split_string[2]
                row['middle_name'] = split_string[1]
        else:
            row['full_name'] = '' 
            if 'first_name' in row:
                row['full_name'] += row['first_name'] + " "
            else:
                row['first_name'] = '' 
            if 'middle_name' in row:
                row['full_name'] += row['middle_name'] + " "
            else:
                row['middle_name'] = ''
            if 'last_name' in row:
                row['full_name'] += row['last_name'] + " "
            else:
                row['last_name'] = ''
                     
    for key in row:
        #print(key, type(key))
        if  key in integer_values:
            if row[key] != '':
                for c in  row[key]:
                    if c in string.ascii_letters or c in string.punctuation:  
                        row[key] = row[key].replace(c, "") 
            #print(row[key])
        elif key in float_values:
            if row[key] != '':
                for c in  row[key]:
                    if c in string.ascii_letters or c in string.punctuation and c != '.':  
                        row[key] = row[key].replace(c, "")     
        elif type(row[key]) == str:
            for c in  row[key]:
                if  c in string.punctuation and c != '.' and c!= ',':  
                    row[key] = row[key].replace(c, "")
    change_dataTypes(row)
    identify_duplicates(row)
   

def identify_duplicates(row_data):
    connect_DB();
    if row_data['source'] == 'NASLPlayer' or row_data['source'] == 'SBNationPlayer' or row_data['source'] == 'USLPlayerStat' or row_data['source'] == 'USLPlayerRos':
        cursor.execute("SELECT * FROM PLAYER WHERE FULL_NAME = '"+ row_data['full_name']+"'")
        duplicate_rows = cursor.fetchall()
        #print(cursor.rowcount)
        if cursor.rowcount <= 0:
            insert_into_db(row_data)
        else:
            for row in duplicate_rows:
                if row['source'] == row_data['source']:
                    update_cursor.execute("delete from player where source ='" + row['source']+"' and full_name ='"+  row_data['full_name'] +"'")
                    #print('insert into')
                    insert_into_db(row_data)
                elif row['source'] == 'USLPlayerStat' and row_data['source'] == 'USLPlayerRos':
                    update_cursor.execute("update  player  set last_team =  %s   , height =  %s , weight = %s ,approved =  %s  where source = %s and full_name = %s" , 
                                          (row_data['last_team'] , row_data['height'],  row_data['weight'],  row_data ['approved'], row['source'], row['full_name']  ))
                    #print('update usl stat with roster')
                elif row['source'] == 'USLPlayerRos' and row_data['source'] == 'USLPlayerStat':   
                    #print('update usl roster with stat')
                    update_cursor.execute('update  player  set nick_name =  %s ,  games_played = %s  ,  goals = %s , points = %s , minutes = %s, fouls =%s , shots= %s, assist = %s, pending=  %s  where source = %s  and full_name = %s', 
                                           (row_data['nick_name'], row_data['games_played'], row_data['goals'], row_data ['points'], row_data['minutes'], row_data['fouls'], row_data['shots'],  row_data['assist'], row_data['pending'], row['source'], row_data['full_name']   ) )
                else:
                    row_data['duplicate'] = '1'
                    insert_into_db(row_data)
    if row_data['source'] == 'NASLTeam' or row_data['source'] == 'USLTeam' or row_data['source'] == 'WhoScored':
        cursor.execute("SELECT * FROM TEAM WHERE TEAM_NAME = '" + row_data['team_name']+ "'")
        duplicate_rows = cursor.fetchall()
        if cursor.rowcount <= 0:
            insert_into_db(row_data)
        else:
            for row in duplicate_rows:
                if row['source'] == row_data['source']:
                    update_cursor.execute("delete from team where source='"+  row['source'] +"' and team_name='"+row_data['team_name'] +"'")
                    insert_into_db(row_data)
                else:
                    row_data['duplicate' ] = '1'
                    insert_into_db(row_data)
    commit_database()
    
def change_dataTypes(data):
    if data['source'] == 'USLPlayerRos':
        if data['height_foot'] == '':
            data['height_foot'] = '0'
        if data['height_inches'] =='':
            data['height_inches'] = '0'
        data['height'] = data['height_foot'] + "." + data['height_inches']
        del data['height_foot']
        del data['height_inches']
        data['height'] = float(data['height'])
    for key in data:
        if  key in integer_values:
            if data[key] != '':
                data[key] = int(data[key])
            else:
                data[key] = None
        if key in float_values:
            if data[key] != '':
                data[key] = float(data[key])
            else:
                data[key] = None
        
def insert_into_db(row_data):
    
    column_data = ''
    column_name = ''
    for key in row_data:
        column_data += '%(' +key + ')s'
        column_name += key + ','
        column_data += ','
    column_data = column_data[0:-1]
    column_name = column_name[0:-1]
        
    #print(column_name)
    #print(column_data) 
    print(row_data)
    'insert from python list into postgres'
    if row_data['source'] == 'NASLPlayer' or row_data['source'] == 'SBNationPlayer'  or row_data['source'] == 'USLPlayerStat' or row_data['source'] == 'USLPlayerRos':
        #print('insert into db');
        cursor.execute("INSERT INTO PLAYER("+column_name+")  VALUES (" + column_data+ ")", row_data)
    elif row_data['source'] == 'NASLTeam' or row_data['source'] == 'USLTeam' or row_data['source'] == 'WhoScored':
        #print('inside team insert')
        cursor.execute("INSERT INTO TEAM("+column_name+")  VALUES (" + column_data+ ")", row_data)
    conn.commit()

def connect_DB():
    HOSTNAME = 'localhost'
    DBNAME = 'webscraping'
    USER = 'postgres'
    PASSWORD = 'postgres'
    conn_string = "host=\'"+ HOSTNAME + "\' dbname=\'" + DBNAME +'\' user=\'' + USER + '\' password=\''+ PASSWORD + '\''
    global conn
    conn = psycopg2.connect(conn_string)
    conn.cursor_factory = RealDictRow
    global cursor
    global update_cursor
    cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    update_cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    
def commit_database():
    conn.commit()