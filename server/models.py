from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, UniqueConstraint
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import datetime

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)


    #RELATIONSHIPS
    #A Customer has many Reservations
    reservations_of_cur_customer = db.relationship("Reservation", back_populates="customer")


    #ASSOCIATION PROXY
    #A Customer has been to many Locations through Reservations
    locations_of_cur_customer = association_proxy("reservations_of_cur_customer", "location")


    #SERIALIZE RULES
    serializer_rules = (
        "-locations_of_cur_customer.customers_of_cur_location",
        "-reservations_of_cur_customer.customer",
        "-reservations_of_cur_customer.location"
        )


    #VALIDATIONS
    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Input must have a name.")
        return name
    
    #####REVIEW THIS SYNTAX#####
    @validates("email")
    def validate_email(self, key, email):
        emails = db.session.query(Customer.email).all()
        if email in emails:
            raise ValueError("Must be a unique email.")
        return email





class Location(db.Model, SerializerMixin):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    max_party_size = db.Column(db.Integer, nullable=False)

    #RELATIONSHIPS
    #A Location has many Reservations
    reservations_of_cur_location = db.relationship("Reservation", back_populates="location")


    #ASSOCIATION PROXY
    #A Location has many Customers through Reservations
    customers_of_cur_location = association_proxy("reservations_of_cur_location", "customer")


    #SERIALIZE RULES
    serialize_rules = (
        "-customers_of_cur_location.location",
        "-reservations_of_cur_location.location",
    )


    #VALIDATIONS
    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Input must have a name.")
        return name
    
    @validates("max_party_size")
    def validate_max_party_size(self, key, max_party_size):
        if not max_party_size:
            raise ValueError("Input must have a max party size.")
        return max_party_size




class Reservation(db.Model, SerializerMixin):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    party_name = db.Column(db.String)
    party_size = db.Column(db.Integer)
    reservation_date = db.Column(db.Date, nullable=False)
    #reservation_date = db.Column(db.DateTime, server_default=db.func().now())
    #FOREIGN KEYS
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))

    #RELATIONSHIPS
    #A Reservation belongs to a Customer
    customer = db.relationship("Customer", back_populates="reservations_of_cur_customer")
    #reservations_of_cur_customer = db.relationship("Reservation", back_populates="customer")

    #A Reservation belongs to a Customer and a Location
    location = db.relationship("Location", back_populates="reservations_of_cur_location")
    #reservations_of_cur_location = db.relationship("Reservation", back_populates="location")


    #SERIALIZE RULES
    serialize_rules = (
        "-location.reservations_of_cur_location",
        "-customer.reservations_of_cur_customer"
    )


    #VALIDATIONS
    @validates("reservation_date")
    def validate_reservation_date(self, key, reservation_date):
        if not reservation_date:
            raise ValueError("Input must have a reservation date.")
        return reservation_date

    @validates("party_name")
    def validate_party_name(self, key, party_name):
        if not party_name:
            raise ValueError("Input must have a party name.")
        return party_name

    @validates("customer_id")
    def validate_customer_id(self, key, customer_id):
        if not customer_id:
            raise ValueError("Input must have a customer id.")
        return customer_id

    @validates("location_id")
    def validate_location_id(self, key, location_id):
        if not location_id:
            raise ValueError("Input must have a location id.")
        return location_id

        #?????????????
        #a customer cannot have more than one reservation for the same date and location