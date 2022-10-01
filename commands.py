from main import db
from flask import Blueprint
from models import Barista, Manager, Venue, Job, Application, Review
from flask_bcrypt import generate_password_hash
from datetime import date, time

db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def creat_db():
    db.create_all()
    print("tables created.")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("tables dropped")


@db_commands.cli.command("seed")
def seed_db():
    barista1 = Barista(
        username="barista1",
        password=generate_password_hash("12345678").decode("utf-8"),
        first_name="Tom",
        last_name="Win",
        email="barista1@email.com",
        contact_number="04322445566",
        address="10 Bundy st, Canberra 2600",
    )

    barista2 = Barista(
        username="barista2",
        password=generate_password_hash("12345678").decode("utf-8"),
        first_name="Lee",
        last_name="Lee",
        email="barista2@email.com",
        contact_number="0411223344",
        address="12 Smith st, Canberra 2610",
    )

    manager1 = Manager(
        username="manager1",
        password=generate_password_hash("12345678").decode("utf-8"),
        first_name="Nick",
        last_name="Martin",
        email="nick@email.com",
        contact_number="0433332222",
    )

    manager2 = Manager(
        username="manager2",
        password=generate_password_hash("12345678").decode("utf-8"),
        first_name="Alan",
        last_name="Ma",
        email="alan@email.com",
        contact_number="0411112222",
    )

    db.session.add(barista1)
    db.session.add(barista2)
    db.session.add(manager1)
    db.session.add(manager2)
    db.session.commit()

    venue1 = Venue(
        venue_name="cafe1",
        address="12 Connell Way Belconnen ACT 2617",
        city="Canberra",
        email="info@cafe1.com",
        abn="180180180",
        contact_number="0261235678",
        manager=manager1
    )

    venue2 = Venue(
        venue_name="cafe2",
        address="112 Benjamin Way Bruce ACT 2617",
        city="Sydney",
        email="info@cafe2.com",
        abn="191191191",
        contact_number="0298765432",
        manager=manager2
    )

    db.session.add(venue1)
    db.session.add(venue2)
    db.session.commit()

    job1 = Job(
        description="Barista required for busy cafe on Sunday",
        date=date(2022, 9, 22),
        start_time=time(hour=10),
        finish_time=time(hour=14),
        pay_rate=35,
        venue=venue1
    )

    job2 = Job(
        description="Barista wanted Saturday",
        date=date(2022, 9, 25),
        start_time=time(hour=8),
        finish_time=time(hour=16),
        pay_rate=35,
        venue=venue2
    )

    db.session.add(job1)
    db.session.add(job2)
    db.session.commit()

    application1 = Application(
        job=job1,
        barista=barista1,
    )

    application2 = Application(
        job=job1,
        barista=barista2,
    )

    db.session.add(application1)
    db.session.add(application2)
    db.session.commit()

    print("table seeded")
