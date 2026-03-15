from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cockatiel_breeder.db'
db = SQLAlchemy(app)

class Breeder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cockatiels = db.relationship('Cockatiel', backref='breeder', lazy=True)

class Cockatiel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breeder_id = db.Column(db.Integer, db.ForeignKey('breeder.id'), nullable=False)

class BreedingPair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    male_cockatiel_id = db.Column(db.Integer, db.ForeignKey('cockatiel.id'), nullable=False)
    female_cockatiel_id = db.Column(db.Integer, db.ForeignKey('cockatiel.id'), nullable=False)

class Clutch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    breeding_pair_id = db.Column(db.Integer, db.ForeignKey('breeding_pair.id'), nullable=False)
    hatch_date = db.Column(db.Date, nullable=False)
    health_records = db.relationship('HealthRecord', backref='clutch', lazy=True)

class HealthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clutch_id = db.Column(db.Integer, db.ForeignKey('clutch.id'), nullable=False)
    DATE = db.Column(db.Date, nullable=False)
    notes = db.Column(db.String(200), nullable=True)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cockatiel_id = db.Column(db.Integer, db.ForeignKey('cockatiel.id'), nullable=False)
    sale_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/breeders', methods=['POST'])
def create_breeder():
    data = request.get_json()
    new_breeder = Breeder(name=data['name'])
    db.session.add(new_breeder)
    db.session.commit()
    return jsonify({'id': new_breeder.id}), 201

@app.route('/cockatiels', methods=['POST'])
def create_cockatiel():
    data = request.get_json()
    new_cockatiel = Cockatiel(name=data['name'], breeder_id=data['breeder_id'])
    db.session.add(new_cockatiel)
    db.session.commit()
    return jsonify({'id': new_cockatiel.id}), 201

@app.route('/breeding_pairs', methods=['POST'])
def create_breeding_pair():
    data = request.get_json()
    new_pair = BreedingPair(male_cockatiel_id=data['male_cockatiel_id'], female_cockatiel_id=data['female_cockatiel_id'])
    db.session.add(new_pair)
    db.session.commit()
    return jsonify({'id': new_pair.id}), 201

@app.route('/clutches', methods=['POST'])
def create_clutch():
    data = request.get_json()
    new_clutch = Clutch(breeding_pair_id=data['breeding_pair_id'], hatch_date=data['hatch_date'])
    db.session.add(new_clutch)
    db.session.commit()
    return jsonify({'id': new_clutch.id}), 201

if __name__ == '__main__':
    db.create_all()  # Create SQL tables
    app.run(debug=True)
