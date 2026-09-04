from flask import Blueprint, render_template, redirect

from extensions import db
from models.beneficiary import Beneficiary
from models.distribution import Distribution


volunteer_bp = Blueprint(
    "volunteer",
    __name__
)


@volunteer_bp.route("/scanner")
def scanner():

    return render_template(
        "volunteer/scanner.html"
    )


@volunteer_bp.route("/verify/<token>")
def verify(token):

    beneficiary = Beneficiary.query.filter_by(
        qr_token=token
    ).first()

    if not beneficiary:
        return "Invalid QR Code"

    distribution = Distribution.query.filter_by(
        beneficiary_id=beneficiary.id
    ).first()

    return render_template(
        "volunteer/verify.html",
        beneficiary=beneficiary,
        distribution=distribution
    )


@volunteer_bp.route("/distribute/<int:beneficiary_id>")
def distribute(beneficiary_id):

    existing_distribution = Distribution.query.filter_by(
        beneficiary_id=beneficiary_id
    ).first()

    if existing_distribution:
        return "Food Already Distributed"

    distribution = Distribution(
        beneficiary_id=beneficiary_id
    )

    db.session.add(distribution)
    db.session.commit()

    return redirect("/distribution-success")


@volunteer_bp.route("/distribution-success")
def distribution_success():

    return render_template(
        "volunteer/distribution_success.html"
    )