import configparser

db_path = "sqlite_db//db/podcast.db"

download_path = "C:\\Users\\Sutton Page\\Desktop\\python-projects\\podcast-rss\\downloads\\"

podcast_cover_path = "C:\\Users\\Sutton Page\\Desktop\\python-projects\\podcast-rss\\config\\podcast_covers\\"

podcasts = {}

podcasts["changelog"] = "https://changelog.com/podcast/feed"

podcasts["js-party"] = "https://changelog.com/jsparty/feed"

podcasts["noble-blood"] = "https://feeds.megaphone.fm/nobleblood"

podcasts["darknet-diaries"] = "https://feeds.megaphone.fm/darknetdiaries"

podcasts["indicator-npr"] = "https://feeds.npr.org/510325/podcast.xml"

podcasts["planet-money"] = "https://feeds.npr.org/510289/podcast.xml"

podcasts["political-gabfest"] = "https://feeds.megaphone.fm/slatespoliticalgabfest"

podcasts["trade-talks"] = "https://www.tradetalkspodcast.com/feed/podcast"

podcasts["U.S-Intelligence-Squard-Debates"] = "https://feeds.megaphone.fm/PNP1207584390"

podcasts["slow-burn"] = "https://feeds.megaphone.fm/watergate"

podcasts["whistlestop"] = "https://feeds.megaphone.fm/slateswhistlestop"

podcasts['revisionist-history'] = "https://feeds.megaphone.fm/revisionisthistory"

podcasts['anncast'] = 'https://www.animenewsnetwork.com/anncast/rss.xml?podcast=audio'

podcasts['the-gist'] = "https://feeds.megaphone.fm/slatesthegist"


gen_config = configparser.ConfigParser()

gen_config["podcasts"] = {}

gen_config['paths'] = {}

gen_config['paths']['download_path'] = download_path

gen_config['paths']['podcast_cover_path'] = podcast_cover_path



for item in podcasts.keys():

    gen_config['podcasts'][item] = podcasts[item]



with open('podcast_sub.ini','w') as configfile:
    gen_config.write(configfile)




