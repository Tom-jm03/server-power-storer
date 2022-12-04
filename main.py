import requests, time, sqlite3, datetime

conn = sqlite3.connect('usage.db')
c = conn.cursor()
print("Starting")
c.execute("""CREATE TABLE IF NOT EXISTS power_consumption (
            day INTEGER NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            hour INTEGER NOT NULL,
            average_watt TEXT NOT NULL
            )""")
conn.commit()
counter = 1
while True:
    minute = []
    hours = []
    if counter < 2:
        current = datetime.datetime.now()
        print(f"Waiting {60 - time.localtime().tm_min} minutes to be accurate. {current.strftime('%H:%M:%S')}\nSo i should start at {current.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)}\n")
        time.sleep((60 - time.localtime().tm_min) * 60)
    counter += 1
    print("Starting to get data")
    for i in range(60):
        print(f"{i} minutes")
        hour = time.localtime().tm_hour
        day = time.localtime().tm_mday
        month = time.localtime().tm_mon
        year = time.localtime().tm_year
        for i in range(1, 60):
            print(f"Getting data for second {i}")
            time.sleep(1)
            r = requests.get('http://192.168.180.45/status')
            watts = r.json()['meters'][0]['power']
            minute.append(watts)
        avg_minute = sum(minute) / len(minute)
    hours.append(avg_minute)
    avg_hour = sum(hours) / len(hours)
    print(f"{avg_hour} {hour} {day} {month} {year}")
    try:
        c.execute("INSERT INTO power_consumption VALUES (?,?,?,?,?)", (day, month, year, hour, avg_hour, ))
    except Exception as e:
        print(e)
        pass
    conn.commit()
