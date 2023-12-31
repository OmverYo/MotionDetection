from flask import Flask, render_template, Response
import mainScreen, gameRun, basicRun, onAir, kneePunch, balanceTest, squatJump
import api

app = Flask(__name__)

@app.route('/gameRun')
def game():
    return render_template('gameRun.html')

@app.route('/basicRun')
def basic():
    return render_template('basicRun.html')

@app.route('/onAir')
def air():
    return render_template('onAir.html')

@app.route('/kneePunch')
def knee():
    return render_template('kneePunch.html')

@app.route('/balanceTest')
def balance():
    return render_template('balanceTest.html')

@app.route('/squatJump')
def squat():
    return render_template('squatJump.html')

@app.route('/mainScreen')
def main():
    return render_template('mainScreen.html')

@app.route('/video_feed')
def video_feed():
    return Response(gameRun.gameRun(), mimetype='multipart/x-mixed-replace; boundary=image')

@app.route('/video_basic')
def video_basic():
    return Response(basicRun.basicRun(), mimetype='multipart/x-mixed-replace; boundary=image')

@app.route('/video_air')
def video_air():
    return Response(onAir.air(), mimetype='multipart/x-mixed-replace; boundary=image')

@app.route('/video_kneePunch')
def video_kneePunch():
    return Response(kneePunch.kneePunch(), mimetype='multipart/x-mixed-replace; boundary=image')

@app.route('/video_balance')
def video_balance():
    return Response(balanceTest.balanceTest(), mimetype='multipart/x-mixed-replace; boundary=image')

@app.route('/video_squat')
def video_squat():
    return Response(squatJump.squatJump(), mimetype='multipart/x-mixed-replace; boundary=image')

@app.route('/video_main')
def video_main():
    return Response(mainScreen.mainScreen(), mimetype='multipart/x-mixed-replace; boundary=image')

if __name__ == '__main__':
    variable = [0, 0, 0, 0]

    result = api.gamedata_api("/HandData", "GET", variable)

    if result:
        pass
    
    else:
        exit()

    app.run(debug=True)