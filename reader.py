from bs4 import BeautifulSoup
import urllib.request
from urllib.request import *
import crud
from crud import *

feed_url = "https://feeds.npr.org/510325/podcast.xml"


data = urllib.request.urlopen(feed_url).read()


soup = BeautifulSoup(data,'xml')


podcast_desc = soup.find("description").text

podcast_title = soup.find("title").text

podcast_feed_link = soup.find("atom:link")["href"]

podcast_website_link = soup.findAll("link")[1].text

image_holder = soup.find("image")

podcast_thumb = image_holder.find("url")

if podcast_thumb!=None:
    podcast_thumb = podcast_thumb.text


episode_titles = []
episode_desc = []
episode_pub_date = []
episode_urls = []

podcast_episodes = soup.findAll("item")

for episode in podcast_episodes:

    title = episode.find("title").text

    desc = episode.find("description").text

    pub_date = episode.find("pubDate").text

    url = episode.find("enclosure")["url"]

    episode_titles.append(title)

    episode_desc.append(desc)

    episode_pub_date.append(pub_date)

    episode_urls.append(url)
