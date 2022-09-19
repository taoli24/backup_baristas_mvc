from main import db


class Venue(db.Model):
    __tablename__ = "venues"
    id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(), nullable=False, unique=True)
    address = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    abn = db.Column(db.String(), nullable=False)
    contact_number = db.Column(db.String(), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey("managers.id"), nullable=False)
    jobs = db.relationship("Job", backref="venue", cascade="all, delete")

