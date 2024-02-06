from bs4 import BeautifulSoup
import urllib.request
from urllib.request import *
import time
import os
import configparser


# index 0 podcast_info
# index 1 episode_titles
# index 2 episode_desc
# index 3 episode_pub_date
# index 4 episode urls
# index 5 episode num


def pull_rss_feed(feed_url):

    feed_data = urllib.request.urlopen(feed_url).read()

    soup = BeautifulSoup(feed_data,'xml')


    # total data holder

    total_data = []

    # grabing podcast info

    podcast_info = {}

    podcast_desc = soup.find("description").text

    podcast_title = soup.find("title").text

    podcast_feed_link = soup.find("atom:link")

    podcast_website_link = soup.findAll("link")[1].text

    image_holder = soup.find("image")

    thumb_holder = image_holder.find("url")


    # setting values

    podcast_info["title"] = podcast_title

    podcast_info["desc"] = podcast_desc

    podcast_info["home_page_url"] = podcast_website_link

    # sets time feed was pulled

    podcast_info["lst_pull_date"] = time.ctime()

    if podcast_feed_link!=None:

        podcast_info["feed_url"] = podcast_feed_link["href"]


    if podcast_feed_link == None:

        podcast_info['feed_url'] = ""


    # grabbing podcast cover image

    if thumb_holder!=None:

        podcast_info["cover_url"] = thumb_holder.text

    if thumb_holder == None:

        cover_image = soup.find("itunes:image")

        if cover_image!=None:

            podcast_info["cover_url"] = cover_image["href"]

        


    # grab episode data

    
    total_episode_data = []
    
    podcast_episodes = soup.findAll("item")

    episode_count = len(podcast_episodes)

    # set episode_count

    podcast_info["episode_count"] = episode_count

    ############################################

    for episode in podcast_episodes:

        temp = []

        title = episode.find("title").text

        desc = episode.find("description").text

        pub_date = episode.find("pubDate").text

        # grabbing episode duration

        episode_duration_value = episode.find('itunes:duration')

        episode_runtime = 0

        if episode_duration_value!=None:

            episode_runtime = episode_duration_value.text

            try:

                runtime_num = int(episode_runtime)

                episode_runtime = round((runtime_num/60))


            except ValueError:

                pass

            

        ######################################################

        url = episode.find("enclosure")["url"]

        temp.append(title)

        temp.append(desc)

        temp.append(pub_date)

        temp.append(episode_runtime)

        temp.append(url)

        temp.append(episode_count)

        total_episode_data.append(temp)

        episode_count-=1



    

    total_data.append(podcast_info)

    total_data.append(total_episode_data)

    return total_data


# returns a message

def download_podcast_cover(config_file_path,podcast_title,cover_url):

    if os.path.exists(config_file_path)==True:

        config = configparser.ConfigParser()

        config.read(config_file_path)

        podcast_cover_path = config['paths']['podcast_cover_path']

        cover_path = podcast_cover_path+podcast_title+".jpg"

        if os.path.exists(cover_path)==False:

            data = urllib.request.urlopen(cover_url).read()

            file_handle = open(cover_path,'wb')

            file_handle.write(data)

            file_handle.close()


            return "Successfully downloaded the cover for the podcast "+podcast_title
    

    else:

        print("-------------------------------------------------------")

        print("The path to the config file given does not exist")

        print("---------------------------------------------------------")
