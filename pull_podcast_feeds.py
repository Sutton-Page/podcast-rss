import feed_parser_funcs
from feed_parser_funcs import pull_rss_feed

import concurrent.futures

import crud
from crud import *

import feed_parser_funcs

from feed_parser_funcs import download_podcast_cover

import configparser

config_path = ".//config//podcast_sub.ini"

config_data = open(config_path,"r").read()

config_parser = configparser.ConfigParser()

config_parser.read_string(config_data)


podcast_config = config_parser["podcasts"]

config_keys = []

for look in podcast_config.keys():
    config_keys.append(look)



total_episode_data = {}

podcast_data = []

cover_download_messages = []

updated_podcast_counter = 0



with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:

    future_holder = []

    for key in config_keys:

        future = executor.submit(pull_rss_feed,podcast_config[key])

        future_holder.append(future)

    for future in concurrent.futures.as_completed(future_holder):

        try:

            result = future.result()

            podcast_title = result[0]["title"]

            podcast_data.append(result[0])

            print("Parsed the rss feed for "+podcast_title)

            total_episode_data[podcast_title] = result[1]

        except Exception as exc:

            print('generated an exception: %s' % (exc))

        
        

db = create_connection(db_path)

cur = db.cursor()


podcast_id_query = ''' select podcast_id,episode_count from podcast where title = ?'''

print("-----------------------------------")

print("Downloading podcast covers")

for podcast in podcast_data:
    podcast_title = podcast["title"]
    podcast_id = None
    podcast_episode_count = None
    result =cur.execute(podcast_id_query,(podcast_title,))

    # download podcast cover image
    
    result_message = download_podcast_cover(config_path,podcast_title,podcast['cover_url'])

    if result_message!=None:

        cover_download_messages.append(result_message)
 
    for res in result:
        podcast_id = res[0]
        podcast_episode_count = res[1]

    if podcast_id == None:
        podcast_pair = podcast.items()

        colms = []
        values = []

        for p in podcast_pair:
            colms.append(p[0])
            values.append(p[1])

        colms = tuple(colms)

        values =tuple(values)

        # generating podcast insert queries

        queryA = 'insert into podcast'+str(colms)

        queryA = queryA.replace("'","")

        place_holders = []

        for i in range(len(values)):

            place_holders.append("?")


        place_holders = tuple(place_holders)

        queryB = 'VALUES'+str(place_holders)

        queryB = queryB.replace("'","")

        final_query = queryA+queryB

        # Adding podcast to the database

        insert_result = insert_data(db,final_query,values)

        print("---------------------------------------")

        print("Added the podcast "+podcast_title+" to the database")

        # getting new podcast index

        podcast_id = ""

        res = cur.execute(podcast_id_query,(podcast_title,))

        for value in res:

            podcast_id = value[0]


        # done inserting data

        episode_data = total_episode_data[podcast_title]

        # for update testing

        #episode_data = episode_data[:15]

        data_holder = []

        for look in episode_data:

            new_list = look

            new_list.append(podcast_id)

            data_holder.append(tuple(new_list))


        # generating episode query
        retrieve_episode_cols = cur.execute("select * from episode")

        place_holders = []

        episode_cols = []

        for col in retrieve_episode_cols.description:

            episode_cols.append(col[0])


        for i in range(len(episode_cols)):

            place_holders.append('?')


        episode_col_query = "insert into episode "+str(tuple(episode_cols))

        episode_value_query = " VALUES"+str(tuple(place_holders))

        episode_value_query = episode_value_query.replace("'","")

        final_episode_query = episode_col_query+episode_value_query

        #inserting podcast_data

        insert_result = insert_data(db,final_episode_query,data_holder,many=True)

        print(" Added episodes to the database sucessfully")

        print("-------------------------------------------------------------")

        
    else:

         parsed_episode_data = total_episode_data[podcast_title]

         # updating podcast lst pull date

         update_query = " UPDATE podcast set lst_pull_date = ? where podcast_id = ?"

         new_pull_date = podcast["lst_pull_date"]

         cur.execute(update_query,(new_pull_date,podcast_id))

         db.commit()

         # setting episode indexs

         new_episode_indexes = []

         for episode in parsed_episode_data:

             episode_index = episode[len(episode)-1]

             new_episode_indexes.append(episode_index)

        # grabbing current episode indexes

         index_query = """ select episode_num from episode where podcast_index = ? """

         res = cur.execute(index_query,(podcast_id,))

         db_episode_indexes = []

         for db_index in res:

             temp_index = db_index[0]

             db_episode_indexes.append(temp_index)


         # check each index

         new_podcast_data = []

         data_row_counter = 0

         for index in new_episode_indexes:

             if db_episode_indexes.__contains__(index) == False:

                 temp_list = parsed_episode_data[data_row_counter]

                 temp_list.append(podcast_id)

                 new_podcast_data.append(tuple(temp_list))

             data_row_counter+=1


        # generating episode update query

         retrieve_episode_cols = cur.execute("select * from episode")

         episode_cols = []

         for col in retrieve_episode_cols.description:

             episode_cols.append(col[0])


         place_holders = []

         for i in range(len(episode_cols)):

             place_holders.append('?')


         episode_cols_query = "insert into episode"+str(tuple(episode_cols))

         episode_value_query = " VALUES"+str(tuple(place_holders))

         episode_value_query = episode_value_query.replace("'","")

         final_episode_query = episode_cols_query+episode_value_query


         new_episode_count = len(db_episode_indexes)+len(new_podcast_data)

         # update episode count query

         update_episode_count = ''' UPDATE podcast set episode_count = ? where podcast_id = ?'''

         if len(new_podcast_data)!=0:

             print("-----------------------")

             # updating episode count

             print("added "+str(len(new_podcast_data))+" episodes to the podcast "+podcast_title)

             cur.execute(update_episode_count,(new_episode_count,podcast_id))

             db.commit()

             #############################################

             print(" Added episodes to the podcast "+podcast_title)

             insert_data(db,final_episode_query,new_podcast_data,many=True)

             print("-----------------------------------------")

             updated_podcast_counter+=1


        

         
    






print("-----------------------------")


for message in cover_download_messages:

    print(message)
         
        
            
if len(cover_download_messages)==0:

    print("No new podcast covers to download")


if updated_podcast_counter!=0:

    print(str(updated_podcast_counter)+" podcasts updated ")



if updated_podcast_counter == 0:

    print(" None of the podcasts updated")
         

         
        
         

         
         

        

        
    
    
    
        
