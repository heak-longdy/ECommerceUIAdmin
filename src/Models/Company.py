from src.db import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    address = db.Column(db.String(256))
    email = db.Column(db.String(128), unique=True)
    phone = db.Column(db.String(32))
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Company {self.name}>'

class CompanyService:
    def get_all(self):
        return Company.query.all()
    def get(self, company_id):
        return Company.query.get(company_id)
    def create(self, data):
        company = Company(**data)
        db.session.add(company)
        db.session.commit()
        return company
    def update(self, company_id, data):
        company = Company.query.get(company_id)
        if not company:
            return None
        for key, value in data.items():
            setattr(company, key, value)
        db.session.commit()
        return company
    def delete(self, company_id):
        company = Company.query.get(company_id)
        if not company:
            return False
        db.session.delete(company)
        db.session.commit()
        return True
