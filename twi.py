import tweepy
import time
import mysql.connector

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

try:
    api = tweepy.API(auth)
    print("Authentication Success")
except:
    print("Authentication Failed")

db = mysql.connector.connect(
    host="localhost",
    user="usradmin",
    passwd="abc@123",
    database="twitusers"
)
mycursor = db.cursor()

sql = "insert into users (UID,Name) values (%s,%s)"


def usrwtxt():
    for x in range(1, 5):

        timelines = api.home_timeline(page=x)
        # print(timelines[0])

        for timeline in timelines:
                #print(timeline.text+ '    -    ' + timeline.user.name)
            mycursor.execute(
                "select UID from users where UID="+str(timeline.user.id))
            mycursor.fetchone()

            if cursor.rowcount == 1:
                continue
            else:
                val = (timeline.user.id, timeline.user.name)
                print(val)
                try:
                    mycursor.execute(sql, val)
                    db.commit()
                    print(
                        "Database push was successful. Thabot will Repeat this process for several times")
                except Exception:
                    print(
                        "database push error You have to Make the databse connecction available first")


while True:
    usrwtxt()
    time.sleep(100)
