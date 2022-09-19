from main import db


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    comments = db.Column(db.String(), default="No comments were left.")
    rating = db.Column(db.Integer, nullable=False)
    barista_id = db.Column(db.Integer, db.ForeignKey("baristas.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
