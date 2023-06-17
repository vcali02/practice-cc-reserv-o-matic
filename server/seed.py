from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Customer, Location, Reservation

fake = Faker()


def create_customers():
    customers = []
    for _ in range(100):
        customer = Customer(name=fake.name(), email=fake.email())
        customers.append(customer)

    return customers


def create_locations():
    locations = []
    for _ in range(8):
        location = Location(
            name=fake.company(), max_party_size=rc(range(8, 20))
        )
        locations.append(location)

    return locations


def create_reservations(customers, locations):
    reservations = []
    for _ in range(50):
        reservation = Reservation(
            reservation_date=fake.date_this_month(),
            customer_id=rc([customer.id for customer in customers]),
            location_id=rc([location.id for location in locations]),
            party_size=rc(range(2, 6)),
            party_name=fake.word(
                ext_word_list=["birthday", "family", "work", "fun", "nothing"]
            ),
        )
        reservations.append(reservation)
        # print(
        #     reservation.customer_id,
        #     reservation.location_id,
        #     reservation.reservation_date,
        # )
    return reservations


if __name__ == "__main__":
    with app.app_context():
        print("Clearing db...")
        Reservation.query.delete()
        Customer.query.delete()
        Location.query.delete()

        print("Seeding customers...")
        customers = create_customers()
        db.session.add_all(customers)
        db.session.commit()

        print("Seeding locations...")
        locations = create_locations()
        db.session.add_all(locations)
        db.session.commit()

        print("Seeding reservations...")
        reservations = create_reservations(customers, locations)
        db.session.add_all(reservations)
        db.session.commit()

        print("Done seeding!")
