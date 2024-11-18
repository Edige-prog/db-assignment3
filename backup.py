import os
import urllib.parse

from flask import Flask, render_template, abort
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
import app.forms as f
from sqlalchemy import (
    create_engine, Column, String, Integer, BigInteger, ForeignKey, Date, func, Table, inspect
)
from sqlalchemy.orm import relationship, declarative_base


app = Flask(__name__, template_folder='app/templates')
Bootstrap5(app)


encoded_password = urllib.parse.quote_plus('edigescode')
# Load environment variables or use default if not set

DATABASE_URL = "postgresql://edigeakimali:xT7iTshsBmjufB6ZELMPDgDLAWsm3IUH@dpg-csto23ogph6c739hoacg-a/assignment3_z0bg"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
engine = create_engine(DATABASE_URL, echo=False)  # echo=True enables SQL logging


db = SQLAlchemy(app)

Base = declarative_base()

# Define Country table
class User(db.Model):
    __table__ = db.Table('users', db.metadata, autoload_with=engine)

class Doctor(db.Model):
    __table__ = db.Table('doctor', db.metadata, autoload_with=engine)

class Patient(db.Model):
    __table__ = db.Table('patients', db.metadata, autoload_with=engine)

class PatientDisease(db.Model):
    __table__ = db.Table('patientdisease', db.metadata, autoload_with=engine)

class Country(db.Model):
    __table__ = db.Table('country', db.metadata, autoload_with=engine)

class Record(db.Model):
    __table__ = db.Table('record', db.metadata, autoload_with=engine)

class Specialize(db.Model):
    __table__ = db.Table('specialize', db.metadata, autoload_with=engine)

class PublicServant(db.Model):
    __table__ = db.Table('publicservant', db.metadata, autoload_with=engine)

class Disease(db.Model):
    __table__ = db.Table('disease', db.metadata, autoload_with=engine)

class DiseaseType(db.Model):
    __table__ = db.Table('diseasetype', db.metadata, autoload_with=engine)

class Discover(db.Model):
    __table__ = db.Table('discover', db.metadata, autoload_with=engine)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('base.html')

@app.route('/users', methods=['GET', 'POST'])
def users():
    users = User.query.all()
    return '<br>'.join([f"{data.email} - {data.name} - {data.surname} - {data.salary} - {data.phone} - {data.cname}" for data in users])

@app.route('/doctor', methods=['GET', 'POST'])
def doctor():
    doctors = Doctor.query.all()
    return '<br>'.join([f"{data.email} - {data.degree}" for data in doctors])
@app.route('/patients', methods=['GET', 'POST'])
def patients():
    patients = Patient.query.all()
    return '<br>'.join([f"{data.email}" for data in patients])

@app.route('/patientdisease', methods=['GET', 'POST'])
def patientdisease():
    patientdisease = PatientDisease.query.all()
    return '<br>'.join([f"{data.email} - {data.disease_code}" for data in patientdisease])
@app.route('/country', methods=['GET', 'POST'])
def country():
    countries = Country.query.all()
    return '<br>'.join([f"{data.cname} - {data.population}" for data in countries])
@app.route('/record', methods=['GET', 'POST'])
def record():
    records = Record.query.all()
    return '<br>'.join([f"{data.email} - {data.cname} - {data.disease_code} - {data.total_deaths} - {data.total_patients}" for data in records])


@app.route('/specialize', methods=['GET', 'POST'])
def specialize():
    specialize = Specialize.query.all()
    return '<br>'.join([f"{data.email} - {data.id}" for data in specialize])

@app.route('/publicservant', methods=['GET', 'POST'])
def publicservant():
    publicservants = PublicServant.query.all()
    return '<br>'.join([f"{data.email} - {data.department}" for data in publicservants])

@app.route('/disease', methods=['GET', 'POST'])
def disease():
    disease = Disease.query.all()
    return '<br>'.join([f"{data.disease_code} - {data.pathogen} - {data.description} - {data.id}" for data in disease])

@app.route('/diseasetype', methods=['GET', 'POST'])
def diseasetype():
    diseasetype = DiseaseType.query.all()
    return '<br>'.join([f"{data.id} - {data.description}" for data in diseasetype])

@app.route('/discover', methods=['GET', 'POST'])
def discover():
    discover = Discover.query.all()
    return '<br>'.join([f"{data.cname} - {data.disease_code} - {data.first_enc_date}" for data in discover])



@app.route('/main_users', methods=['GET', 'POST'])
def main_users():
    return render_template('users.html')
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    country = db.session.query(Country).all()
    form = f.CreateUser([data.cname for data in country])
    if form.validate_on_submit():
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            surname=form.surname.data,
            phone=form.phone.data,
            salary = form.salary.data,
            cname=form.cname.data
        )
        db.session.add(new_user)
        db.session.commit()
        return 'Successfully created'
    return render_template("create.html", form=form)

@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    country = db.session.query(Country).all()
    form = f.CreateUser([data.cname for data in country])
    if form.validate_on_submit():
        user_to_update = db.get_or_404(User, form.email.data)

        user_to_update.name = form.name.data
        user_to_update.surname = form.surname.data
        user_to_update.phone = form.phone.data
        user_to_update.salary = form.salary.data
        user_to_update.cname = form.cname.data
        db.session.commit()
        return 'Successfully updated'
    return render_template("create.html", form=form)

@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    users = db.session.query(User).all()
    form = f.DeleteUser([data.email for data in users])
    if form.validate_on_submit():
        user_to_delete = db.get_or_404(User, form.email.data)
        db.session.delete(user_to_delete)
        db.session.commit()
        return 'Successfully deleted'
    return render_template("create.html", form=form)

@app.route('/create_doctor', methods=['GET', 'POST'])
def create_doctor():
    users = db.session.query(User).all()
    form = f.CreateDoctor([data.email for data in users])
    if form.validate_on_submit():
        new_doctor = Doctor(
            email = form.email.data,
            degree = form.degree.data,
        )
        db.session.add(new_doctor)
        db.session.commit()
        return 'Successfully created'
    return render_template("create.html", form=form)

@app.route('/update_doctor', methods=['GET', 'POST'])
def update_doctor():
    doctors = db.session.query(Doctor).all()
    form = f.CreateDoctor([data.email for data in doctors])
    if form.validate_on_submit():
        user_to_update = db.get_or_404(Doctor, form.email.data)
        user_to_update.degree = form.degree.data
        db.session.commit()
        return 'Successfully updated'
    return render_template("create.html", form=form)

@app.route('/delete_doctor', methods=['GET', 'POST'])
def delete_doctor():
    doctors = db.session.query(Doctor).all()
    form = f.DeleteUser([data.email for data in doctors])
    if form.validate_on_submit():
        user_to_delete = db.get_or_404(User, form.email.data)
        db.session.delete(user_to_delete)
        db.session.commit()
        return 'Successfully deleted'
    return render_template("create.html", form=form)


@app.route('/create_patient', methods=['GET', 'POST'])
def create_patient():
    users = db.session.query(User).all()
    form = f.CreatePatient([data.email for data in users])
    if form.validate_on_submit():
        new_patient = Patient(
            email = form.email.data,
        )
        db.session.add(new_patient)
        db.session.commit()
        return 'Successfully created'
    return render_template("create.html", form=form)

@app.route('/update_patient', methods=['GET', 'POST'])
def update_patient():
    patients = db.session.query(Patient).all()
    form = f.CreatePatient([data.email for data in patients])
    if form.validate_on_submit():
        user_to_update = db.get_or_404(Patient, form.email.data)
        user_to_update.email = form.email.data
        db.session.commit()
        return 'Successfully updated'
    return render_template("create.html", form=form)

@app.route('/delete_patient', methods=['GET', 'POST'])
def delete_patient():
    patients = db.session.query(Patient).all()
    form = f.DeleteUser([data.email for data in patients])
    if form.validate_on_submit():
        user_to_delete = db.get_or_404(User, form.email.data)
        db.session.delete(user_to_delete)
        db.session.commit()
        return 'Successfully deleted'
    return render_template("create.html", form=form)

@app.route('/create_publicservant', methods=['GET', 'POST'])
def create_publicservant():
    users = db.session.query(User).all()
    form = f.CreatePublicServant([data.email for data in users])
    if form.validate_on_submit():
        new_publicservant = PublicServant(
            email = form.email.data,
            department = form.department.data
        )
        db.session.add(new_publicservant)
        db.session.commit()
        return 'Successfully created'
    return render_template("create.html", form=form)

@app.route('/delete_publicservant', methods=['GET', 'POST'])
def delete_publicservant():
    publicservants = db.session.query(PublicServant).all()
    form = f.DeleteUser([data.email for data in publicservants])
    if form.validate_on_submit():
        user_to_delete = db.get_or_404(User, form.email.data)
        db.session.delete(user_to_delete)
        db.session.commit()
        return 'Successfully deleted'
    return render_template("create.html", form=form)

@app.route('/update_publicservant', methods=['GET', 'POST'])
def update_publicservant():
    users = db.session.query(User).all()
    form = f.CreatePublicServant([data.email for data in users])
    if form.validate_on_submit():
        user_to_update = db.get_or_404(User, form.email.data)
        user_to_update.department = form.department.data
        db.session.commit()
        return 'Successfully updates'
    return render_template("create.html", form=form)

@app.route('/add_country', methods=['GET', 'POST'])
def add_country():
    form = f.CreateCountry()
    if form.validate_on_submit():
        new_country = Country(
            cname = form.cname.data,
            population = form.population.data
        )
        db.session.add(new_country)
        db.session.commit()
        return 'Successfully created'
    return render_template("create.html", form=form)


@app.route('/delete_country', methods=['GET', 'POST'])
def delete_country():
    countries = db.session.query(Country).all()
    form = f.DeleteCountry([data for data in countries])
    if form.validate_on_submit():
        data_to_delete = db.get_or_404(Country, form.cname.data)
        db.session.delete(data_to_delete)
        db.session.commit()
        return 'Successfully deleted'
    return render_template("create.html", form=form)

@app.route('/update_country', methods=['GET', 'POST'])
def update_country():
    form = f.CreateCountry()
    if form.validate_on_submit():
        user_to_update = db.get_or_404(Country, form.cname.data)
        user_to_update.cname = form.cname.data
        user_to_update.population = form.population.data
        db.session.commit()
        return 'Successfully updated'
    return render_template("create.html", form=form)


@app.route('/add_diseasetype', methods=['GET', 'POST'])
def add_diseasetype():
    form = f.CreateDiseaseType()
    max_id = db.session.query(func.max(DiseaseType.id)).scalar()
    if form.validate_on_submit():
        new_diseasetype = DiseaseType(
            description = form.description.data,
            id = max_id + 1
        )
        db.session.add(new_diseasetype)
        db.session.commit()
        return 'Successfully created'

    return render_template("create.html", form=form)

@app.route('/delete_diseasetype', methods=['GET', 'POST'])
def delete_diseasetype():
    diseases = db.session.query(Disease).all()
    form = f.DeleteDisease([data for data in diseases])
    if form.validate_on_submit():
        data_to_delete = db.get_or_404(Disease, form.disease_code.data)
        db.session.delete(data_to_delete)
        db.session.commit()
        return 'Successfully deleted'
    return render_template("create.html", form=form)

@app.route('/update_diseasetype', methods=['GET', 'POST'])
def update_diseasetype():
    form = f.CreateDiseaseType()
    max_id = db.session.query(func.max(DiseaseType.id)).scalar()
    if form.validate_on_submit():
        new_diseasetype = DiseaseType(
            description = form.description.data,
            id = max_id + 1
        )
        db.session.add(new_diseasetype)
        db.session.commit()
        return 'Successfully created'

    return render_template("create.html", form=form)

@app.route('/add_specialist', methods=['GET', 'POST'])
def add_specialist():
    diseasetypes = db.session.query(DiseaseType).all()
    doctors = db.session.query(Doctor).all()
    form = f.CreateSpecialist([data.email for data in doctors], [(data.id, data.description) for data in diseasetypes])

    if form.validate_on_submit():
        new_specialist = Specialize(
            id=form.id.data,
            email=form.email.data
        )
        db.session.add(new_specialist)
        db.session.commit()
        return 'Successfully created'

    return render_template("create.html", form=form)


@app.route('/delete_specialist', methods=['GET', 'POST'])
def delete_specialist():
    specialists = db.session.query(Specialize).all()
    form = f.DeleteSpecialist([data for data in specialists])
    if form.validate_on_submit():
        d = ''.join(form.ans.data)
        d = d.split(' ')
        id = d[1][:-1]
        email = d[2][:-1]
        print(id, email)
        data_to_delete = Specialize.query.filter_by(email=email, id=int(id)).first()

        # Check if the record exists, otherwise raise 404
        if data_to_delete is None:
            abort(404)
        db.session.delete(data_to_delete)
        db.session.commit()
        return 'Successfully deleted'
    return render_template("create.html", form=form)

@app.route('/add_patientDisease', methods=['GET', 'POST'])
def add_patientDisease():
    patients = db.session.query(Patient).all()
    diseases = db.session.query(Disease).all()

    form = f.CreatePatientDisease([(data.email, data.email) for data in patients],
                            [(data.disease_code, data.description) for data in diseases])

    if form.validate_on_submit():
        new_patientdisease = PatientDisease(
            email=form.email.data,
            disease_code=form.disease_code.data
        )
        db.session.add(new_patientdisease)
        db.session.commit()
        return 'Successfully created'

    return render_template("create.html", form=form)

@app.route('/delete_patientdisease', methods=['GET', 'POST'])
def delete_patientdisease():
    patientdisease = db.session.query(PatientDisease).all()
    form = f.DeletePatientDisease([data for data in patientdisease])
    if form.validate_on_submit():
        d = ''.join(form.ans.data)
        d = d.split(' ')
        email = d[1][:-1]
        disease_code = d[2][:-1]
        data_to_delete = PatientDisease.query.filter_by(email=email, disease_code=disease_code).first()

        # Check if the record exists, otherwise raise 404
        if data_to_delete is None:
            abort(404)
        db.session.delete(data_to_delete)
        db.session.commit()
        return 'Successfully deleted'
    return render_template("create.html", form=form)


@app.route('/main_disease', methods=['GET', 'POST'])
def main_disease():
    return render_template('disease.html')
@app.route('/main_doctor', methods=['GET', 'POST'])
def main_doctor():
    return render_template('doctor.html')
@app.route('/main_publicservants', methods=['GET', 'POST'])
def main_publicservants():
    return render_template('public_servant.html')
@app.route('/main_patients', methods=['GET', 'POST'])
def main_patients():
    return render_template('patient.html')

@app.route('/main_record', methods=['GET', 'POST'])
def main_record():
    return render_template('record.html')
@app.route('/main_country', methods=['GET', 'POST'])
def main_country():
    return render_template('countries.html')

@app.route('/main_specialists', methods=['GET', 'POST'])
def main_specialists():
    return render_template('specialists.html')

@app.route('/main_patientdisease', methods=['GET', 'POST'])
def main_patientdisease():
    return render_template('patientdisease.html')

@app.route('/main_diseasetype', methods=['GET', 'POST'])
def main_diseasetype():
    return render_template('diseasetype.html')

@app.route('/main_discover', methods=['GET', 'POST'])
def main_discover():
    return render_template('discover.html')



@app.route('/add_disease', methods=['GET', 'POST'])
def add_disease():
    diseasetypes = db.session.query(DiseaseType).all()

    form = f.CreateDisease([(data.id, data.description) for data in diseasetypes])

    if form.validate_on_submit():
        new_disease = Disease(
            disease_code=form.disease_code.data,
            pathogen=form.pathogen.data,
            description=form.description.data,
            id = form.id.data
        )
        db.session.add(new_disease)
        db.session.commit()
        return 'Successfully created'

    return render_template("create.html", form=form)

@app.route('/delete_disease', methods=['GET', 'POST'])
def delete_disease():
    diseases = db.session.query(Disease).all()
    form = f.DeleteDisease([data for data in diseases])
    if form.validate_on_submit():
        data_to_delete = db.get_or_404(Disease, form.disease_code.data)
        db.session.delete(data_to_delete)
        db.session.commit()
        return 'Successfully deleted'
    return render_template("create.html", form=form)

@app.route('/add_discover', methods=['GET', 'POST'])
def add_discover():
    countries = db.session.query(Country).all()
    diseasetypes = db.session.query(Disease).all()

    form = f.Add_discover([(data.disease_code, data.description) for data in diseasetypes],[(data.cname, data.cname) for data in countries])

    if form.validate_on_submit():
        new_discover = Discover(
            cname=form.cname.data,
            disease_code=form.disease_code.data,
            first_enc_date=form.first_enc_date.data,
        )
        db.session.add(new_discover)
        db.session.commit()
        return 'Successfully created'

    return render_template("create.html", form=form)

@app.route('/delete_discover', methods=['GET', 'POST'])
def delete_discover():
    diseases = db.session.query(Discover).all()
    form = f.DeleteDiscover([data for data in diseases])
    if form.validate_on_submit():
        d = ''.join(form.ans.data)
        d = d.split(' ')
        country = d[1][:-1]
        disease_code = d[2][:-1]
        data_to_delete = Discover.query.filter_by(cname=country, disease_code=disease_code).first()

        # Check if the record exists, otherwise raise 404
        if data_to_delete is None:
            abort(404)
        db.session.delete(data_to_delete)
        db.session.commit()
        return 'Successfully deleted'
    return render_template("create.html", form=form)


@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    countries = db.session.query(Country).all()
    diseasetypes = db.session.query(Disease).all()
    publicservants = db.session.query(PublicServant).all()

    form = f.Add_record([(data.disease_code, data.description) for data in diseasetypes],[(data.cname, data.cname) for data in countries], [(data.email, data.email) for data in publicservants])

    if form.validate_on_submit():
        new_record = Record(
            cname=form.cname.data,
            disease_code=form.disease_code.data,
            email=form.email.data,
            total_deaths=form.total_deaths.data,
            total_patients=form.total_patients.data,
        )
        db.session.add(new_record)
        db.session.commit()
        return 'Successfully created'

    return render_template("create.html", form=form)

@app.route('/delete_record', methods=['GET', 'POST'])
def delete_record():
    records = db.session.query(Record).all()
    form = f.DeleteRecord([data for data in records])
    if form.validate_on_submit():
        d = ''.join(form.ans.data)
        d = d.split(' ')
        email = d[1][:-1]
        country = d[2][:-1]
        disease_code = d[3][:-1]
        print(email, country, disease_code)
        data_to_delete = Record.query.filter_by(email = email, cname=country, disease_code=disease_code).first()

        # Check if the record exists, otherwise raise 404
        if data_to_delete is None:
            abort(404)
        db.session.delete(data_to_delete)
        db.session.commit()
        return 'Successfully deleted'
    return render_template("create.html", form=form)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get PORT from environment or default to 5000
    app.run(host="0.0.0.0", port=port, debug=False)
