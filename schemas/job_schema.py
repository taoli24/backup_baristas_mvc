from main import ma


class JobSchema(ma.Schema):
    class Meta:
        fields = ("id", "description", "date", "start_time", "finish_time", "pay_rate", "status", "barista_id", "venue_id")
        load_only = ("barista_id",)


job_schema = JobSchema()
jobs_schema = JobSchema(many=True)
