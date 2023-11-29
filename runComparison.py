import moveComparison
import mysql.connector

mc = moveComparison

# 데이터 베이스로 접속 할 정보를 입력합니다
mydb = mysql.connector.connect(host = "localhost", user = "root", password = "0000", database = "metaports")
mycursor = mydb.cursor()

# 데이터 베이스에서 가져올 정보를 입력합니다
sql = "SELECT video_id FROM model_name WHERE video_id = 'easyDance.mp4'"

# SQL 코드를 실행 합니다
mycursor.execute(sql)

# 실행한 SQL 코드의 출력 결과를 불러옵니다
myresult = mycursor.fetchall()[0][1]

# 출력될 모델의 영상은 데이터 베이스에서 가져온 해당 영상으로 지정합니다
benchmark_video = myresult
# 유저의 영상이 캠일 경우 0으로 지정
user_video = 0

# 준비된 두 영상을 실행하고 비교 알고리즘 모듈을 실행합니다
mc.compare_positions(benchmark_video, user_video)

# 정확도를 불러옵니다
accuracyList = mc.accuracyList

# 데이터 베이스에 정확도를 업로드합니다
sql = "INSERT INTO MT_TRAINING_RESULT (capture_time, accuracy) VALUES (%s, %s)"

# 해당 SQL 코드를 실행 후
mycursor.executemany(sql, accuracyList)

# 커밋을 하여 저장합니다
mydb.commit()