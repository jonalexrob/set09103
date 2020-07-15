from flask import Flask, render_template, url_for, redirect, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
app.config['GOOGLEMAPS_KEY'] = "AIzaSyCfU7QSQgPXg3vfhh9GKnHk30guaIzcs-8"
GoogleMaps(app)

class checklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(200), nullable=False, unique=True)
    have = db.Column(db.Boolean)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/where")
def where():
    edimap = Map(
        identifier="edimap",
        lat=55.947871,
        lng=-3.363518,
        markers=[
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat':  -55.947871,
                'lng':  -3.3635189,
                'infobox': "<b>Edinburgh Airport</b>"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': 55.941201, 
                'lng': -3.216940,
                'infobox': "<b>Fountain Park"
            },
            {
                'icon': '.3.',
                'lat': 55.951937, 
                'lng': -3.191791,
                'infobox': "waverly"
            },
            {
                'icon': '.4.',
                'lat': 55.935981, 
                'lng': -3.228747,
                'infobox': "Slateford Road Accomodation"
            },
            {
                'icon': '.5.',
                'lat': 55.940198,
                'lng': -3.216225,
                'infobox': "Bainfield Accomodation"
            },
            {
                'icon': 'orlock',
                'lat': 55.941928, 
                'lng': -3.220841,
                'infobox': "orlock"
            },
            {
                'icon': 'merc campus',
                'lat': 55.932961,
                'lng': -3.213266,
                'infobox': "merc campus"
            },
            {
                'icon': 'craig campus',
                'lat': 55.919503,
                'lng': -3.237919,
                'infobox': "craig campus"
            },
            {
                'icon': 'sighthill campus',
                'lat': 55.924510,
                'lng': -3.288041,
                'infobox': "sighthill campus"
            },
            {
                'icon': 'haymarket',
                'lat': 55.945856,
                'lng': -3.218195,
                'infobox': "sighthill campus"
            },
            {
                'icon': 'slateford station',
                'lat': 55.926290,
                'lng': -3.243945,
                'infobox': "slateford station"
            }
        ]
    )
    return render_template('where.html', edimap=edimap)

@app.route("/checklist")
def checklist():
    missing = checklist.query.filter_by(have=False).all()
    have = checklist.query.filter_by(have=True).all()

    return render_template('checklist.html', missing=missing, have=have)

@app.route('/add', methods=['POST'])
def add():
    checklist = checklist(text=request.form['checklistitem'], have=False)
    db.session.add(checklist)
    db.session.commit()

    return redirect(url_for('checklist'))

@app.route('/have/<id>')
def have(id):

    checklist = checklist.query.filter_by(id=int(id)).first()
    checklist.have = True
    db.session.commit()
    
    return redirect(url_for('checklist'))
    return render_template("checklist.html")
    
@app.route("/checklistalt")
def checklistalt():
    return render_template('checklistalt.html')

if __name__ == "__main__":
    app.run(debug=True)