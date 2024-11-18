from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, Length


# WTForm for creating a blog post
class CreateUser(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(max=60, message="Description must not exceed 60 characters.")])
    name = StringField("Name", validators=[DataRequired(), Length(max=30, message="Description must not exceed 30 characters.")] )
    surname = StringField("Surname", validators=[DataRequired(), Length(max=40, message="Description must not exceed 40 characters.")])
    phone = StringField("Phone", validators=[DataRequired(), Length(max=20, message="Description must not exceed 20 characters.")])
    salary = IntegerField("Salary")
    cname = SelectField("Country Name", choices = [("", "Select")], validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, users, *args, **kwargs):
        super(CreateUser, self).__init__(*args, **kwargs)
        self.cname.choices += [(user, user) for user in users]

class DeleteUser(FlaskForm):
    email = SelectField("Select email to delete", choices=[("", "Select")], validators=[DataRequired()])
    submit = SubmitField("Submit")


    def __init__(self, users, *args, **kwargs):
        super(DeleteUser, self).__init__(*args, **kwargs)
        self.email.choices += [(user, user) for user in users]

class CreateDoctor(FlaskForm):
    email = SelectField("User", choices=[("", "Select")], validators=[DataRequired()])
    degree = SelectField("Degree", choices = [("", "Select"), ("PHD", "PHD"), ("Master's", "Master's"), ("Bachelor's", "Bachelor's")])
    submit = SubmitField("Submit")

    def __init__(self, users, *args, **kwargs):
        super(CreateDoctor, self).__init__(*args, **kwargs)
        self.email.choices += [(user, user) for user in users]

class CreatePatient(FlaskForm):
    email = SelectField("User", choices=[("", "Select")], validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, users, *args, **kwargs):
        super(CreatePatient, self).__init__(*args, **kwargs)
        self.email.choices += [(user, user) for user in users]

class CreatePublicServant(FlaskForm):
    email = SelectField("User", choices=[("", "Select")], validators=[DataRequired()])
    department = SelectField("Department", choices=[("", "Select"),
                                        ("Health", "Health"),
                                        ("Infectious Diseases", "Infectious Diseases"),
                                        ("Public Safety", "Public Safety"),
                                        ("Public Safety", "Public Safety"),
                                        ("Research", "Research"),
                                        ("Community Health", "Community Health"),
                                        ("Environmental Health", "Environmental Health"),
                                        ("Epidemiology", "Epidemiology"),
                                        ("Emergency Response", "Emergency Response"),
                                        ("Child Health", "Child Health"),
                                        ("Maternal Health", "Maternal Health"),
                                            ], validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, users, *args, **kwargs):
        super(CreatePublicServant, self).__init__(*args, **kwargs)
        self.email.choices += [(user, user) for user in users]





class CreateCountry(FlaskForm):
    cname = StringField("Country Name", validators=[DataRequired(), Length(max=50, message="Description must not exceed 140 characters.")])
    population = IntegerField("Population", validators=[DataRequired()])
    submit = SubmitField("Submit")


class DeleteCountry(FlaskForm):
    cname = SelectField("Select country to delete", choices=[("", "Select")], validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, countries, *args, **kwargs):
        super(DeleteCountry, self).__init__(*args, **kwargs)
        self.cname.choices += [(data.cname, data.cname) for data in countries]

class CreateDiseaseType(FlaskForm):
    description = StringField("Disease description", validators=[DataRequired(), Length(max=140, message="Description must not exceed 140 characters.")])
    submit = SubmitField("Submit")

class DeleteDisease(FlaskForm):
    disease_code = SelectField("Select disease code to delete", choices=[("", "Select")], validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, diseases, *args, **kwargs):
        super(DeleteDisease, self).__init__(*args, **kwargs)
        self.disease_code.choices += [(data.disease_code, data.disease_code) for data in diseases]

class DeletePatientDisease(FlaskForm):
    ans = SelectField("Select Patient Disease to delete", choices=[("", "Select")], validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, diseases, *args, **kwargs):
        super(DeletePatientDisease, self).__init__(*args, **kwargs)
        self.ans.choices += [(data, [data.email, data.disease_code]) for data in diseases]


class DeleteSpecialist(FlaskForm):
    ans = SelectField("Select country to delete", choices=[("", "Select")], validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, specialists, *args, **kwargs):
        super(DeleteSpecialist, self).__init__(*args, **kwargs)
        self.ans.choices += [(data, data.email) for data in specialists]


class CreateSpecialist(FlaskForm):
    id = SelectField("Disease Type", choices=[("", "Select")], validators=[DataRequired()])
    email = SelectField("Doctor", choices=[("", "Select")], validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, doctors, diseasetypes, *args, **kwargs):
        super(CreateSpecialist, self).__init__(*args, **kwargs)
        self.id.choices += diseasetypes
        self.email.choices += [(user, user) for user in doctors]

class CreatePatientDisease(FlaskForm):
    disease_code = SelectField("Disease", choices=[("", "Select")], validators=[DataRequired()])
    email = SelectField("Patient", choices=[("", "Select")], validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, patients, diseasetypes, *args, **kwargs):
        super(CreatePatientDisease, self).__init__(*args, **kwargs)
        self.disease_code.choices += diseasetypes
        self.email.choices += patients

class CreateDisease(FlaskForm):
    disease_code = StringField("Disease code", validators=[DataRequired(), Length(max=50, message="Description must not exceed 50 characters.")])
    pathogen = StringField("Pathogen", validators=[DataRequired(), Length(max=20, message="Description must not exceed 20 characters.")])
    description = StringField("Description", validators=[DataRequired(), Length(max=140, message="Description must not exceed 140 characters.")])
    id = SelectField("Disease Type: ", choices=[("", "Select")], validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, diseasetypes, *args, **kwargs):
        super(CreateDisease, self).__init__(*args, **kwargs)
        self.id.choices += diseasetypes

class Add_discover(FlaskForm):
    disease_code = SelectField("Disease", choices=[("", "Select")], validators=[DataRequired()])
    cname = SelectField("Country: ", choices=[("", "Select")], validators=[DataRequired()])
    first_enc_date = DateField("First Encounter Date", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, diseasetypes, countries, *args, **kwargs):
        super(Add_discover, self).__init__(*args, **kwargs)
        self.disease_code.choices += diseasetypes
        self.cname.choices+=countries

class DeleteDiscover(FlaskForm):
    ans = SelectField("Select discover to delete", choices=[("", "Select")], validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, diseases, *args, **kwargs):
        super(DeleteDiscover, self).__init__(*args, **kwargs)
        self.ans.choices += [(data, [data.disease_code, data.cname]) for data in diseases]



class Add_record(FlaskForm):
    disease_code = SelectField("Disease", choices=[("", "Select")], validators=[DataRequired()])
    cname = SelectField("Country: ", choices=[("", "Select")], validators=[DataRequired()])
    email = SelectField("Public Servant", choices=[("", "Select")], validators=[DataRequired()])
    total_deaths = IntegerField("Total Deaths", validators=[DataRequired()])
    total_patients = IntegerField("Total Patients", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, diseasetypes, countries, publicservants, *args, **kwargs):
        super(Add_record, self).__init__(*args, **kwargs)
        self.disease_code.choices += diseasetypes
        self.cname.choices+=countries
        self.email.choices+=publicservants

class DeleteRecord(FlaskForm):
    ans = SelectField("Select record to delete", choices=[("", "Select")], validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, diseases, *args, **kwargs):
        super(DeleteRecord, self).__init__(*args, **kwargs)
        self.ans.choices += [(data, [data.email, data.cname, data.disease_code]) for data in diseases]







