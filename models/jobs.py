from main import db


class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    start_time = db.Column(db.Time(), nullable=False)
    finish_time = db.Column(db.Time(), nullable=False)
    pay_rate = db.Column(db.Integer)
    status = db.Column(db.String(), default="To be fulfilled")
    barista_id = db.Column(db.Integer, db.ForeignKey("baristas.id"))
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)
    applications = db.relationship("Application", backref="job", cascade="all, delete")
    reviews = db.relationship("Review", backref="job", cascade="all, delete")
