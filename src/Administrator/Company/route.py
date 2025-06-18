from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.Models.Company import *
from .form import CompanyForm

company_bp = Blueprint('company', __name__, url_prefix='/companies')
service = CompanyService()

@company_bp.route('/')
def index():
    companies = service.get_all()
    return render_template('companies/index.html', companies=companies)

@company_bp.route('/create', methods=['GET', 'POST'])
def create():
    form = CompanyForm()
    if form.validate_on_submit():
        service.create(form.data)
        flash('Company created successfully!', 'success')
        return redirect(url_for('company.index'))
    return render_template('companies/create.html', form=form)

@company_bp.route('/<int:company_id>')
def view(company_id):
    company = service.get(company_id)
    if not company:
        flash('Company not found.', 'danger')
        return redirect(url_for('company.index'))
    return render_template('companies/view.html', company=company)

@company_bp.route('/<int:company_id>/edit', methods=['GET', 'POST'])
def edit(company_id):
    company = service.get(company_id)
    if not company:
        flash('Company not found.', 'danger')
        return redirect(url_for('company.index'))
    form = CompanyForm(obj=company)
    if form.validate_on_submit():
        service.update(company_id, form.data)
        flash('Company updated successfully!', 'success')
        return redirect(url_for('company.view', company_id=company_id))
    return render_template('companies/edit.html', form=form, company=company)

@company_bp.route('/<int:company_id>/delete', methods=['POST'])
def delete(company_id):
    if service.delete(company_id):
        flash('Company deleted.', 'success')
    else:
        flash('Company not found.', 'danger')
    return redirect(url_for('company.index'))
