from main import db


class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    barista_id = db.Column(db.Integer, db.ForeignKey("baristas.id"), nullable=False)
    status = db.Column(db.String(), default="pending")
