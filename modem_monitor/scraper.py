from bs4 import BeautifulSoup
import requests
import config
import time
import mysql.connector


def main():
    status_URL = 'http://192.168.100.1/RgConnect.asp'
    # log_URL = ''

    soup = getSoup(status_URL)
    ds_levels, us_levels = getStatus(soup)

    insert_into_db('downstream', ds_levels)
    insert_into_db('upstream', us_levels)


def getSoup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features='html.parser')
    return soup


def getStatus(soup):
    tables = soup.findAll('table')
    downstream_table = tables[2].findAll('tr')[2:]
    upstream_table = tables[3].findAll('tr')[2:]
    now = int(time.time())

    downstream_info = []
    for row in downstream_table:
        cols = row.findAll('td')
        status = cols[1].string.strip()
        channel = int(cols[0].string)
        frequency = int(cols[4].string[:-4])/1000000
        power = float(cols[5].string[:-5])
        snr = float(cols[6].string[:-3])
        corrected = int(cols[7].string)
        uncorrected = int(cols[8].string)
        if status == "Locked":
            channel_info = { 'id': myHash(now, channel),
                        'timestamp': now,
                        'frequency': frequency,
                        'power': power,
                        'snr': snr,
                        'corrected': corrected,
                        'uncorrected': uncorrected
            }
            downstream_info.append(channel_info)

    upstream_info = []
    for row in upstream_table:
        cols = row.findAll('td')
        status = cols[1].string.strip()
        channel = int(cols[0].string)
        frequency = float(cols[5].string[:-4])/1000000
        power = float(cols[6].string[:-5])
        if status == "Locked":
            channel_info = { 'id': myHash(now, channel),
                        'timestamp': now,
                        'frequency': frequency,
                        'power': power
            }
            upstream_info.append(channel_info)
    
    return (downstream_info, upstream_info)

def myHash(timestamp, channel):
    ch = str(channel)
    if len(ch) < 2:
        ch = '0' + ch
    key = str(timestamp) + ch
    return int(key)


def insert_into_db(table, data):
    conn = mysql.connector.connect(**config.mysql)
    cursor = conn.cursor()

    for entry in data:
        placeholders = ', '.join(['%s'] * len(entry))
        cols = ', '.join(entry.keys())
        sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        print(sql)
        print(entry.values())

        try:
            cursor.execute(sql, list(entry.values()))
        except mysql.connector.Error as err:
            print(f"ERROR: {err}")
        else:
            print("SUCCESS!!")
            conn.commit()

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
