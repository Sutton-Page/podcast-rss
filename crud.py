import sqlite3
from sqlite3 import Error



db_path = "sqlite_db//db//podcast.db"





def create_connection(db_path):

    conn = None

    try:

        conn = sqlite3.connect(db_path)

    except Error as e:

        print(e)


    return conn



def insert_data(db,query,data,many=False):

    cur = db.cursor()

    if many==False:

        cur.execute(query,data)

        db.commit()

    if many==True:

        cur.executemany(query,data)

        db.commit()

    return cur.lastrowid



def get_podcast_data(cur,podcast_table_name):

    podcast_query = "select * from "+podcast_table_name

    podcast_result = cur.execute(podcast_query)

    podcast_data = {}

    podcast_index = 0

    for podcast in podcast_result:

        podcast_data[podcast_index] = podcast

        podcast_index+=1


    podcast_cols = []

    for cols in podcast_result.description:

        podcast_cols.append(cols[0])

        


    podcast_data['cols'] = tuple(podcast_cols)

    return podcast_data

        

def return_podcast_episodes(cur,episode_table_name,podcast_num):

    query = 'select * from episode where podcast_index = ? ORDER BY episode_num DESC'

    podcat_cols = ""

    podcast_data = {}

    podcast_id = 1

    podcast_index = 0

    while podcast_id <=podcast_num:

        temp_episode_dict = {}

        podcast_col_holder = []

        episode_index = 0

        result = cur.execute(query,(podcast_id,))

        for episode in result:

            temp_episode_dict[episode_index] = episode

            episode_index+=1


        for col in result.description:

            podcast_col_holder.append(col[0])


        podcast_data[podcast_index] = temp_episode_dict

        podcast_data['cols'] = tuple(podcast_col_holder)

        

        podcast_index+=1

        podcast_id+=1


    return podcast_data    

        

        

   

    

    
    

    
