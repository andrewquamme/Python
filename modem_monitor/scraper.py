from bs4 import BeautifulSoup
import requests
import config
# import mysql.connector


def main():
    status_URL = 'http://192.168.100.1/RgConnect.asp'
    linkLog = ''

    soup = getSoup(status_URL)
    levels = getStatus(soup)


def getSoup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features='html.parser')
    return soup


def getStatus(soup):

    tables = soup.findAll('table')
    downstream_table = tables[2].findAll('tr')[2:]
    upstream_table = tables[3].findAll('tr')[2:]

    downstream_info = []
    for row in downstream_table:
        cols = row.findAll('td')
        status = cols[1].string.strip()
        frequency = int(cols[4].string[:-4])/1000000
        power = float(cols[5].string[:-5])
        snr = float(cols[6].string[:-3])
        corrected = int(cols[7].string)
        uncorrected = int(cols[8].string)
        if status == "Locked":
            channel = { 'frequency': frequency,
                        'power': power,
                        'snr': snr,
                        'corrected': corrected,
                        'uncorrected': uncorrected
            }
            print(channel)
            downstream_info.append(channel)

    upstream_info = []
    for row in upstream_table:
        cols = row.findAll('td')
        status = cols[1].string.strip()
        frequency = int(cols[5].string[:-4])/1000000
        power = float(cols[6].string[:-5])
        if status == "Locked":
            channel = { 'frequency': frequency,
                        'power': power
            }
            print(channel)
            upstream_info.append(channel)

# def myHash(str):
#     idx = 0
#     for c in str:
#         idx += ord(c)
#     return idx*37*len(str)


# def checkDB(course, announcements, link):
#     if course == 'CSC335':
#         number = config.andrew
#     elif course == 'CSC352':
#         number = config.duncan

#     conn = mysql.connector.connect(**config.mysql)

#     cursor = conn.cursor()

#     sql = f"INSERT INTO {course} (id, date, text) VALUES (%s, %s, %s)"

#     for announcement in announcements:
#         _id = announcement.get('id')
#         date = announcement.get('date')
#         text = announcement.get('text')
#         val = (_id, date, text)
#         try:
#             cursor.execute(sql, val)
#         except:
#             pass
#         else:
#             print(f"Sent message for announcement {_id}")
#             message = f"{course} on {date}: {text} \n {link}"
#             sendMessage(message, number)
#             conn.commit()

#     cursor.close()
#     conn.close()


if __name__ == "__main__":
    main()
