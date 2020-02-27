from bs4 import BeautifulSoup
import requests
from twilio.rest import Client
import config
import mysql.connector


def main():
    course = 'CSC335'
    link = 'http://www.u.arizona.edu/~jmisurda/teaching/csc335/spring2020/index.html'
    soup = getSoup(link)
    announcements = getAnnouncements(soup)
    checkDB(course, announcements, link)

    course = 'CSC352'
    link = 'http://www.u.arizona.edu/~jmisurda/teaching/csc352/spring2020/index.html'
    soup = getSoup(link)
    announcements = getAnnouncements(soup)
    checkDB(course, announcements, link)


def getSoup(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, features='html.parser')
    return soup


def sendMessage(message, number):

    client = Client(config.account_sid, config.auth_token)
    print("Sent to " + number)
    message = client.messages \
                    .create(
                        body=message,
                        from_=config.from_,
                        to=number
                    )
    
    print(message.sid)


def getAnnouncements(soup):

    a_list = soup.find('a', attrs= {'id':'Announcements'}).next_element.next_element.next_element

    announcements = []
    for item in a_list.find_all('li'):
        announcement = {}
        announcement['id']   = myHash(item.p.text)
        announcement['date'] = item.p.text[1:9]
        announcement['text'] = item.p.text[13:]
        announcements.append(announcement)

    return announcements

def myHash(str):
    idx = 0
    for c in str:
        idx += ord(c)
    return idx*37*len(str)


def checkDB(course, announcements, link):
    if course == 'CSC335':
        number = config.andrew
    elif course == 'CSC352':
        number = config.duncan

    conn = mysql.connector.connect(**config.mysql)

    cursor = conn.cursor()

    sql = f"INSERT INTO {course} (id, date, text) VALUES (%s, %s, %s)"

    for announcement in announcements:
        _id = announcement.get('id')
        date = announcement.get('date')
        text = announcement.get('text')
        val = (_id, date, text)
        try:
            cursor.execute(sql, val)
        except:
            pass
        else:
            print(f"Sent message for announcement {_id}")
            message = f"{course} on {date}: {text} \n {link}"
            sendMessage(message, number)
            conn.commit()

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
