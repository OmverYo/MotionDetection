import mysql.connector

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "0000", database = "metaports")
mycursor = mydb.cursor()

# perfect_frame = 1
# awesome_frame = 2
# good_frame = 3
# ok_frame = 4
# bad_frame = 5

# totalAccuracyList = []

# i = 0
# j = 0

# while i < 10:
#     totalAccuracyList.append([i, j])
#     i += 1
#     j += 10

# total = 0

# for x in range(0, len(totalAccuracyList)):
#     total = total + totalAccuracyList[x][1]

# total = int(total / len(totalAccuracyList))

# print(total)

# sql = "INSERT INTO player_data (total, perfect_frame, awesome_frame, good_frame, ok_frame, bad_frame) VALUES (%s, %s, %s, %s, %s, %s)"
# mycursor.execute(sql, (total, perfect_frame, awesome_frame, good_frame, ok_frame, bad_frame))

sql = "INSERT INTO background (isVR) VALUES (1)"
mycursor.execute(sql)
mydb.commit()

sql = "SELECT * FROM background"
# SQL 코드를 실행 합니다
mycursor.execute(sql)
# 실행한 SQL 코드의 출력 결과를 불러옵니다
myresult = mycursor.fetchall()[0][1]

if myresult == 1:
    isVR = True

else:
    isVR = False

print(isVR)

sql = "INSERT INTO program_running (isRunning) VALUES (1)"
mycursor.execute(sql)
mydb.commit()

sql = "SELECT * FROM program_running"
# SQL 코드를 실행 합니다
mycursor.execute(sql)
# 실행한 SQL 코드의 출력 결과를 불러옵니다
myresult = mycursor.fetchall()[0][1]

print(myresult)

# mydb.commit()