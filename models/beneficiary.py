from extensions import db


class Beneficiary(db.Model):
    __tablename__ = "beneficiaries"

    id = db.Column(db.Integer, primary_key=True)
    

    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(
    db.String(30),
    unique=True,
    nullable=False
)

    year = db.Column(db.String(20), nullable=False)

    department = db.Column(db.String(100), nullable=False)

    genesis_role = db.Column(db.String(100), nullable=False)

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    qr_token = db.Column(
        db.String(100),
        unique=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<Beneficiary {self.name}>"