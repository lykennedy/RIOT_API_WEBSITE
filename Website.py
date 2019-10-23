

from flask import Flask, render_template, url_for, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
import sys
import jsonpickle # used to serialize python object so that javascript can use
from sqlalchemy_utils import ScalarListType
sys.path.insert(1, r'/Users/kennedy/Desktop/Python_Projects/RIOT_API')
import RIOT_API
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'dc024df49e9184e4b14e88c116592bcd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///champs.db'
counter = 0
change = False
test = 0
class Champ_Info(db.Model):
    name = db.Column(db.String(30), primary_key=True)
    title = db.Column(db.String(50))
    lore = db.Column(db.Text, nullable=False)
    #skills = db.Column(ScalarListType(), nullable=False)

Champs = Champ_Info.query.all()

@app.route("/")
def home():
    free_rotation = RIOT_API.free_rotation()
    return render_template('home.html', free_champs=free_rotation, Champs=Champs, data=jsonpickle.encode(Champs))


@app.route('/button', methods=["GET", "POST"])
def button():
    return render_template("json.html")


@app.route('/status')
def status():
    return render_template('status.html', status=RIOT_API.get_status())


@app.route('/history', methods=["GET", "POST"])
def history():
    global counter, change
    champ = None
    num = None
    if request.method == "POST":
        if counter == 0: # This section returns the champions played for that summoner
            summoner = request.form['text'] # This is the information sent by the text input form
            RIOT_API.get_summoner_name(summoner)
            RIOT_API.get_match_history(champ, num)
            counter += 1
        elif counter == 1:
            champ = request.form['btn']
            RIOT_API.get_match_history(champ, num)
            counter += 1
            return render_template('history.html', matches=RIOT_API.requested_matches, change=change, counter=counter)
        else:
            num = request.form['send']
            RIOT_API.get_match_history(champ, num)
            return render_template('history.html', team0=RIOT_API.team0, team1=RIOT_API.team1, match_info=RIOT_API.match_info)
    return render_template('history.html', champ_hist=RIOT_API.champs_played, change=change, counter=counter, test=test)


@app.route('/testing') # For Testing
def testing():
    free_rotation = RIOT_API.free_rotation()
    #return jsonify(suckme=["Element1", "Elemtn2", "Element3"])
    #return Response(jsonpickle.encode(Champs), mimetype='application/json')
    return render_template('testing.html', data=free_rotation)

"""
@app.route('/testing', methods=['POST']) # For testing.
def handle_data():
    print(True)
    text = request.form['text']
    processed_text = text.upper()
    print(processed_text)
    return processed_text
"""

if __name__ == "__main__":

    app.run(debug=True)
