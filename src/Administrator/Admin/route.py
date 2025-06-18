from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.Models.Admin import Admin
from .form import AdminForm
from src.db import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def index():
    admins = Admin.query.all()
    return render_template('Admin/admin/index.html', admins=admins)

@admin_bp.route('/create', methods=['GET', 'POST'])
def create():
    form = AdminForm()
    if form.validate_on_submit():
        admin = Admin(
            username=form.username.data,
            email=form.email.data
        )
        admin.set_password(form.password.data)
        db.session.add(admin)
        db.session.commit()
        flash('Admin created successfully!', 'success')
        return redirect(url_for('admin.index'))
    return render_template('Admin/admin/create.html', form=form)

@admin_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    admin = Admin.query.get_or_404(id)
    form = AdminForm(obj=admin)
    if form.validate_on_submit():
        admin.username = form.username.data
        admin.email = form.email.data
        if form.password.data:
            admin.set_password(form.password.data)
        db.session.commit()
        flash('Admin updated successfully!', 'success')
        return redirect(url_for('admin.index'))
    return render_template('Admin/admin/edit.html', form=form, admin=admin)

@admin_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    admin = Admin.query.get_or_404(id)
    db.session.delete(admin)
    db.session.commit()
    flash('Admin deleted successfully!', 'success')
    return redirect(url_for('admin.index'))
