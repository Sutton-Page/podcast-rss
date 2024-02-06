import sqlite3

db_path = "..//sqlite_db//db//podcast.db"

con = sqlite3.connect(db_path)

cur = con.cursor()


# returns table schema
# pragma table_info (table_name)


podcast_cols = []

podcast_schema_data = []

res = cur.execute("pragma table_info('podcast')")

for item in res:

    podcast_schema_data.append(item)

    podcast_cols.append(item[1])



res2 = cur.execute('select * from podcast')

podcasts = []

for podcast in res2:

    podcasts.append(podcast)




podcast_data = {}

for podcast in podcasts:

    item_index = 0

    temp_dict = {}

    podcast_id = podcast[0]

    for value in podcast:

        temp_dict[podcast_cols[item_index]] = value

        item_index+=1

    podcast_data[podcast_id] = temp_dict
    


# episode schema


res3 = cur.execute('pragma table_info("episode")')

episode_schema = []

episode_cols = []

for item in res3:

    episode_schema.append(item)

    episode_cols.append(item[1])



podcast_episode_data = []

for key in podcast_data.keys():

    query = 'select * from episode where podcast_index = ? ORDER BY episode_num DESC'

    pod_res = cur.execute(query,(key,))

    temp = []

    for episode in pod_res:

        temp.append(episode)
    podcast_episode_data.append(temp)

    

