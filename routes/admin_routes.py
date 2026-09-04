from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session
)

from extensions import db

from models.admin import Admin
from models.beneficiary import Beneficiary
from models.distribution import Distribution

from utils.qr_generator import generate_qr

import uuid


admin_bp = Blueprint(
    "admin",
    __name__
)


# ----------------------------
# Admin Login
# ----------------------------

@admin_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(
            username=username,
            password=password
        ).first()

        if admin:

            session["admin_id"] = admin.id

            return redirect("/admin/dashboard")

        return "Invalid Credentials"

    return render_template(
        "admin/login.html"
    )


# ----------------------------
# Admin Logout
# ----------------------------

@admin_bp.route("/admin/logout")
def logout():

    session.pop("admin_id", None)

    return redirect("/admin/login")


# ----------------------------
# Admin Dashboard
# ----------------------------

@admin_bp.route("/admin/dashboard")
def dashboard():

    if "admin_id" not in session:
        return redirect("/admin/login")

    total_registered = Beneficiary.query.count()

    total_approved = Beneficiary.query.filter_by(
        status="Approved"
    ).count()

    total_distributed = Distribution.query.count()

    total_pending = Beneficiary.query.filter_by(
        status="Pending"
    ).count()

    return render_template(
        "admin/dashboard.html",
        total_registered=total_registered,
        total_approved=total_approved,
        total_distributed=total_distributed,
        total_pending=total_pending
    )


# ----------------------------
# Beneficiaries List
# ----------------------------

@admin_bp.route("/admin/beneficiaries")
def beneficiaries():

    if "admin_id" not in session:
        return redirect("/admin/login")

    all_beneficiaries = Beneficiary.query.all()

    return render_template(
        "admin/beneficiaries.html",
        beneficiaries=all_beneficiaries
    )


# ----------------------------
# Approve Beneficiary
# ----------------------------

@admin_bp.route("/admin/approve/<int:id>")
def approve_beneficiary(id):

    if "admin_id" not in session:
        return redirect("/admin/login")

    beneficiary = Beneficiary.query.get_or_404(id)

    token = str(uuid.uuid4())

    beneficiary.status = "Approved"
    beneficiary.qr_token = token
    qr_url = f"https://packet-distribution-system.onrender.com/verify/{token}"

    generate_qr(qr_url)

    db.session.commit()

    return redirect("/admin/beneficiaries")