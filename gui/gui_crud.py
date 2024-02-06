import sqlite3
from sqlite3 import Error
import configparser
import os

db_path = "..//sqlite_db//db//podcast.db"

config_path = "..//config//podcast_sub.ini"



def create_connection(db_path):

    conn = None

    try:

        conn = sqlite3.connect(db_path)

    except Error as e:

        print(e)


    return conn



       
def return_podcast_data(cur,config_path,podcast_table_name):

    podcast_query = "select * from "+podcast_table_name

    podcast_holder = {}

    if os.path.exists(config_path)==True:

        config = configparser.ConfigParser()

        config.read(config_path)

        cover_path = config['paths']['podcast_cover_path']

        # retrieving podcast from database

        result = cur.execute(podcast_query)

        podcast_cols = []

        podcast_index = 0

        cover_path_dict = {}

        for cols in result.description:

            podcast_cols.append(cols[0])


        for podcast in result:

            title_index = podcast_cols.index("title")

            podcast_title = podcast[title_index]

            cover_path_dict[podcast_index] = cover_path+podcast_title+".jpg"

            data_dict = {}

            cols_index = 0

            for value in podcast:

                data_dict[podcast_cols[cols_index]] = value

                cols_index+=1


            podcast_holder[podcast_index] = data_dict

            

            podcast_index+=1

        podcast_holder['cover_paths'] = cover_path_dict
        
        return podcast_holder
    

    else:

        print("The config path given does not exist")

        


def retrieve_episode_data(cur,episode_table_name,total_podcast_num):

    query = "select * from "+episode_table_name+" where podcast_index = ? ORDER BY episode_num DESC"

    podcast_index = 0

    podcast_id = 1

    podcast_key_dict = {}

    while podcast_id <=total_podcast_num:

        episode_key_dict = {}

        episode_cols = []

        episode_result = cur.execute(query,(podcast_id,))

        for col in episode_result.description:

            episode_cols.append(col[0])
        
        episode_index = 0
        
        for episode in episode_result:

            episode_col_index = 0

            episode_data_dict = {}

            for value in episode:

                episode_data_dict[episode_cols[episode_col_index]] = value

                episode_col_index+=1

            
            episode_key_dict[episode_index] = episode_data_dict

            episode_index+=1

        podcast_key_dict[podcast_index] = episode_key_dict

        podcast_id+=1
        podcast_index+=1
    
    return podcast_key_dict 


        
            

