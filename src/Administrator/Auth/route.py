from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from src.Models.Admin import Admin
from .form import LoginForm, RegisterForm
from src.db import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Ensure Bcrypt is initialized in your app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if Admin.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))
        admin = Admin(
            username=form.username.data,
            email=form.email.data
        )
        admin.set_password(form.password.data)
        db.session.add(admin)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    try:
        form = LoginForm()
        if form.validate_on_submit():
            admin = Admin.query.filter_by(email=form.email.data).first()
            if admin and admin.check_password(form.password.data):
                access_token = create_access_token(identity=admin.id)
                session['admin_id'] = admin.id 
                # You can return the token as JSON, set it as a cookie, or pass to the template
                flash('Login successful!', 'success')
                return redirect(url_for('customer_bp.customer_list'))
                # return render_template('admin/customers/index.html', form=form, access_token=access_token)
            else:
                flash('Invalid email or password.', 'danger')
        return render_template('auth/login.html', form=form)
    except Exception as e:
        flash(f'Error checking session: {str(e)}', 'danger')
        return str(e)
    

@auth_bp.route('/logout')
def logout():
    session.clear()  # Remove all session data
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login'))
