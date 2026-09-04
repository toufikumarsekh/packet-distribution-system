from flask import Blueprint, render_template, request, redirect

from extensions import db
from models.beneficiary import Beneficiary


beneficiary_bp = Blueprint(
    "beneficiary",
    __name__
)


@beneficiary_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        beneficiary = Beneficiary(
            name=request.form["name"],
            roll_number=request.form["roll_number"],
            year=request.form["year"],
            department=request.form["department"],
            genesis_role=request.form["genesis_role"]
        )

        db.session.add(beneficiary)
        db.session.commit()

        return redirect("/register")

    return render_template("register.html")


@beneficiary_bp.route("/search_qr", methods=["GET", "POST"])
def search_qr():

    beneficiary = None

    if request.method == "POST":

        roll_number = request.form["roll_number"]
        beneficiary = Beneficiary.query.filter_by(
            roll_number=roll_number
            ).first()

    return render_template(
        "beneficiary/search_qr.html",
        beneficiary=beneficiary
    )