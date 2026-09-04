from extensions import db


class Distribution(db.Model):
    __tablename__ = "distributions"

    id = db.Column(db.Integer, primary_key=True)

    beneficiary_id = db.Column(
        db.Integer,
        db.ForeignKey("beneficiaries.id"),
        nullable=False
    )

    distributed_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    beneficiary = db.relationship(
        "Beneficiary",
        backref="distributions"
    )
