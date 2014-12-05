import ConfigParser
import psycopg2
import Util

DB_INFO_SECTION = 'DbInfo'

def get_connection(config_path):
	config = ConfigParser.ConfigParser()

	config.read(config_path)

	host = config.get(DB_INFO_SECTION, 'host')
	port = config.get(DB_INFO_SECTION, 'port')
	database_name = config.get(DB_INFO_SECTION, 'database_name')
	user = config.get(DB_INFO_SECTION, 'user')
	password = config.get(DB_INFO_SECTION, 'password')

	conn_string = "";
	conn_string += "dbname='" +database_name+ "' " 
	conn_string += "user='" +user+ "' " 
	conn_string += "host='" +host+ "' " 
	conn_string += "password='" +password+ "'" 
	Util.debug(conn_string)
	try:
		conn = psycopg2.connect(conn_string)
		Util.debug("Connected succesfully")
		return conn
	except:
		Util.error("cannot connect to db")
		return None

