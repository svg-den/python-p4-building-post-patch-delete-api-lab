#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = db.session.get(Bakery, id)
    if not bakery:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)

    data = request.form
    if 'name' in data:
        bakery.name = data['name']
    
    db.session.commit()
    return make_response(jsonify(bakery.to_dict()), 200)

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    new_baked_good = BakedGood(name=data['name'], price=data['price'])
    db.session.add(new_baked_good)
    db.session.commit()
    return make_response(jsonify(new_baked_good.to_dict()), 201)

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = db.session.get(BakedGood, id)
    if not baked_good:
        return make_response(jsonify({'error': 'Baked good not found'}), 404)

    db.session.delete(baked_good)
    db.session.commit()
    return make_response(jsonify({'message': 'Baked good deleted successfully'}), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)