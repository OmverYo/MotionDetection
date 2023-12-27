from flask import Flask, render_template, Response
import mysql.connector
import mainScreen, gameRun, basicRun

app = Flask(__name__)

@app.route('/gameRun')
def game():
    return render_template('gameRun.html')

@app.route('/basicRun')
def basic():
    return render_template('basicRun.html')

@app.route('/mainScreen')
def main():
    return render_template('mainScreen.html')

@app.route('/video_feed')
def video_feed():
    return Response(gameRun.gameRun(), mimetype='multipart/x-mixed-replace; boundary=image')

@app.route('/video_basic')
def video_basic():
    return Response(basicRun.basicRun(), mimetype='multipart/x-mixed-replace; boundary=image')

@app.route('/video_main')
def video_main():
    return Response(mainScreen.mainScreen(), mimetype='multipart/x-mixed-replace; boundary=image')

if __name__ == '__main__':
    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "0000", database = "metaports")

    if not mydb:
        exit()
    
    app.run(debug=True)