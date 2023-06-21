#!/usr/bin/env python3

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get(
#     "DB_URI", f"sqlite://{os.path.join(BASE_DIR, 'instance/app.db')}"
# )

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import db, Customer, Location, Reservation
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    BASE_DIR, "instance/app.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def home():
    return ""

#GET /customers
class Customers(Resource):
    def get(self):
        #1. query
        customers = Customer.query.all()
        #2. dict
        customers_dict = [c.to_dict() for c in customers]
        #3. res return
        res = make_response(
            customers_dict,
            200
        )
        return res 
#4. api
api.add_resource(Customers, "/customers")

#GET /customers/int:id
class OneCustomer(Resource):
    def get(self, id):
        try:
            customer = Customer.query.filter_by(id=id).first()
            customer_dict = customer.to_dict()
            res = make_response(
                customer_dict,
                200
            )
            return res
        except:
            return {"error": "404: Customer not found"}, 404
api.add_resource(OneCustomer, "/customers/<int:id>")


#POST /customer
class NewCustomer(Resource):
    def get(self):
        customers = Customer.query.all()
        customers_dict = [c.to_dict() for c in customers]
        res = make_response(
            customers_dict,
            200
        )
        return res
#POST
    def post(self):
        data = request.get_json()
        try:
            new_customer = Customer(
                name= data.get("name"),
                email= data.get("email")
            )
            db.session.add(new_customer)
            db.session.commit()

            new_customer_dict = new_customer.to_dict()

            res = make_response(
                new_customer_dict,
                201
            )
            return res
        except:
            return {"error": "400: Validation error"}, 400
api.add_resource(NewCustomer, "/customer")


#GET /locations
class Locations(Resource):
    def get(self):
        locations = Location.query.all()
        locations_dict = [l.to_dict() for l in locations]
        res = make_response(
            locations_dict,
            200
        )
        return res

api.add_resource(Locations, "/locations")


#POST /reservations
class Reservations(Resource):
    def get(self):
        reservations = Reservation.query.all()
        reservations_dict = [r.to_dict() for r in reservations]
        res = make_response(
            reservations_dict,
            200
        )
        return res
#POST
    def post(self):
        data = request.get_json()
        try:
            new_reservation = Reservation(
                party_name=data.get("party_name"),
                party_size=data.get("party_size"),
                reservation_date=data.get("reservation_date"),
                location_id=data.get("location_id"),
                customer_id=data.get("customer_id")
            )
            db.session.add(new_reservation)
            db.session.commit()

            new_reservation_dict= new_reservation.to_dict()

            res = make_response(
                new_reservation_dict,
                201
            )
            return res
        except:
            return {"error": "400: Validation error"}, 400

api.add_resource(Reservations, "/reservations")


#PATCH /reservations/int:id
class OneReservation(Resource):
    def get(self, id):
        reservation = Reservation.query.filter_by(id=id).first()
        reservation_dict = reservation.to_dict()
        res = make_response(
            reservation_dict,
            200
        )
        return res
#PATCH
    def patch(self, id):
        try:
            reservation = Reservation.query.filter_by(id=id).first()
        except:
            return {"error": "404: Reservation not found"}, 404
        data = request.get_json()
        for attr in data:
            setattr(reservation, attr, data.get(attr))
        db.session.add(reservation)
        db.session.commit()
        return make_response(reservation.to_dict(), 200)

#DELETE /reservations/int:id
    def delete(self, id):
        reservation = Reservation.query.filter_by(id=id).first()
        db.session.delete(reservation)
        db.session.commit()

        return make_response({}, 204)

api.add_resource(OneReservation, "/reservation/<int:id>")




if __name__ == "__main__":
    app.run(port=5555, debug=True)
