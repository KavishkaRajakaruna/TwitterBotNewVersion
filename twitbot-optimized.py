def html_doc(entry):
    if hasattr(entry, 'content'):
        return entry.content[0].value
    elif hasattr(entry, 'description'):
        return entry.description
    else:
        return None


def img_src(soup):
    img = soup.find("img")
    if img is not None:
        return img["src"]
    else:
        return None


def media(feed, entry):
    doc = html_doc(entry)
    if doc is not None:
        soup = BeautifulSoup(doc, "html.parser")
        img_url = img_src(soup)
        if img_url is not None:
            media_root = feed.get_media_root()
            # e.g. .png?v=2 becomes just .png # TODO check againt .jpeg and other ext > 3
            media_ext = os.path.splitext(img_url)[1][0:4]
            media_path = media_root + media_ext
            urllib.urlretrieve(img_url, media_path)
            return media_path
        else:
            return None
    else:
        return None


def init_twitter():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api


def post_tweet(api):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS RSSContent (`url`, `title`, `dateAdded`)')

    for feed in FEEDS:
        parsed_feed = feedparser.parse(feed.get_url())

        for entry in parsed_feed.entries:

            c.execute('SELECT * FROM RSSContent WHERE url=?', (entry.link,))
            if not c.fetchall():
                data = (entry.link, entry.title, time.strftime(
                    "%Y-%m-%d %H:%M:%S", entry.updated_parsed))
                c.execute(
                    'INSERT INTO RSSContent (`url`, `title`, `dateAdded`) VALUES (?,?,?)', data)

                hashtag_length = len(feed.get_hashtag())
                body_length = TWEET_NET_LENGTH - hashtag_length

                tweet_body = entry.title.encode('utf-8')[:body_length]
                tweet_url = entry.link.encode('utf-8')
                tweet_hashtag = feed.get_hashtag()

                tweet_text = "%s %s %s" % (
                    tweet_body, tweet_url, tweet_hashtag)
                tweet_media = media(feed, entry)

                if tweet_media is not None:
                    api.update_with_media(tweet_media, tweet_text)
                else:
                    api.update_status(tweet_text)

                print " ", time.strftime("%c"), "-", tweet_text

    conn.commit()
    conn.close()
