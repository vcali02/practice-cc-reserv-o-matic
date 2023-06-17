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

    @validates("name")
    def validate_name(self, key, name):
        if not name or len(name) < 1:
            raise ValueError("Customer must have a name")
        return name

    @validates("email")
    def validate_email(self, key, email):
        if "@" not in email:
            raise ValueError("Failed basic e-mail check")
        return email

    # relationships
    reservations = db.relationship("Reservation", back_populates="customer")
    locations = association_proxy("reservations", "location")
    serialize_rules = ("-reservations.customer",)

    def __repr__(self):
        return f"<Customer name={self.name}, email={self.email}>"


class Location(db.Model, SerializerMixin):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    max_party_size = db.Column(db.Integer, nullable=False)

    customers = association_proxy("reservations", "customer")
    # relationships
    reservations = db.relationship("Reservation", back_populates="location")
    serialize_rules = ("-reservations.location",)

    @validates("name")
    def validate_name(self, key, name):
        if not name or len(name) < 1:
            raise ValueError("Location must have a name")
        return name

    @validates("max_party_size")
    def validate_max_party_size(self, key, max_party_size):
        if not isinstance(max_party_size, int):
            raise TypeError("Max party size must be an integer")
        return max_party_size


class Reservation(db.Model, SerializerMixin):
    __tablename__ = "reservations"
    __table_args__ = (
        UniqueConstraint("location_id", "customer_id", "reservation_date"),
    )
    id = db.Column(db.Integer, primary_key=True)
    party_name = db.Column(db.String, nullable=False)

    # locations and relationships
    location_id = db.Column(
        db.Integer, db.ForeignKey("locations.id"), nullable=False
    )
    location = db.relationship("Location", back_populates="reservations")
    # customer and relationship
    customer_id = db.Column(
        db.Integer, db.ForeignKey("customers.id"), nullable=False
    )
    customer = db.relationship("Customer", back_populates="reservations")
    party_size = db.Column(db.Integer, nullable=False)
    reservation_date = db.Column(db.Date, nullable=False)
    serialize_rules = ("-location.reservations", "-customer.reservations")

    @validates("party_name")
    def validate_name(self, key, party_name):
        if not party_name or len(party_name) < 1:
            raise ValueError("Reservation party must have a name")
        return party_name

    @validates("customer_id")
    def validate_customer_id(self, key, customer_id):
        if not customer_id or not isinstance(customer_id, int):
            raise ValueError(
                "Reservation must have a customer specified by an integer"
            )
        return customer_id

    @validates("location_id")
    def validate_location_id(self, key, location_id):
        if not location_id or not isinstance(location_id, int):
            raise ValueError(
                "Location must have a location_id and it must be an integer"
            )
        return location_id

    @validates("reservation_date")
    def validate_date(self, key, reservation_date):
        if not isinstance(reservation_date, datetime.date):
            raise TypeError("Reservation_date must be a date")
        return reservation_date


# add any models you may need.
