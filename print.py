import mysql.connector

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "0000", database = "metaports")
mycursor = mydb.cursor()

perfect_frame = 1
awesome_frame = 2
good_frame = 3
ok_frame = 4
bad_frame = 5

totalAccuracyList = []

i = 0
j = 0

while i < 10:
    totalAccuracyList.append([i, j])
    i += 1
    j += 10

total = 0

for x in range(0, len(totalAccuracyList)):
    total = total + totalAccuracyList[x][1]

total = int(total / len(totalAccuracyList))

print(total)

sql = "INSERT INTO player_data (total, perfect_frame, awesome_frame, good_frame, ok_frame, bad_frame) VALUES (%s, %s, %s, %s, %s, %s)"
mycursor.execute(sql, (total, perfect_frame, awesome_frame, good_frame, ok_frame, bad_frame))
mydb.commit()