import moveComparison
import mysql.connector

mc = moveComparison

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "0000",
    database = "metaports"
)

mycursor = mydb.cursor()

benchmark_video = 'BX_Dance01_01_FV_A113C177.mp4'
user_video = 0 # replace with 0 for webcam

mc.compare_positions(benchmark_video, user_video)

accuracy = mc.accuracy

sql = "INSERT INTO MT_TRAINING_RESULT (TOTAL) VALUES (%s)"
val = (accuracy, )

mycursor.execute(sql, val)

mydb.commit()