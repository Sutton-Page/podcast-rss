DROP TABLE IF EXISTS podcast;
DROP TABLE IF EXISTS episode;

CREATE TABLE podcast (
	podcast_id integer PRIMARY KEY AUTOINCREMENT,
	title text NOT NULL,
	home_page_url text,
	feed_url text,
	desc text NOT NULL,
	cover_url text,
	lst_pull_date text NOT NULL,
	episode_count integer NOT NULL
);


create TABLE episode(
	title text NOT NULL,
	desc text NOT NULL,
	pub_date text NOT NULL,
	episode_runtime integer NOT NULL,
	episode_url text NOT NULL,
	episode_num integer NOT NULL,
	podcast_index integer NOT NULL,
	FOREIGN KEY (podcast_index) REFERENCES podcast (podcast_id)
	PRIMARY KEY (podcast_index,episode_num)

);