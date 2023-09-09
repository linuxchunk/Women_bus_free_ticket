from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)

# Configure the database URI (SQLite in this example)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bus_ticket.db'
db = SQLAlchemy(app)

# Define the UserProfile model
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Aadhar_number = db.Column(db.String(10), unique=True, nullable=False)
    is_woman = db.Column(db.String(10), nullable=False)  # 'woman' or 'man'

    def __init__(self, Aadhar_number, is_woman):
        self.Aadhar_number = Aadhar_number
        self.is_woman = is_woman

# Create the database tables
with app.app_context():
    db.create_all()

# Define a function to import data from the CSV file
def import_data_from_csv():
    with open('data.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            Aadhar_number = row['Aadhar_number']
            is_woman = row['is_woman']

            # Check if the user already exists in the database
            existing_user = UserProfile.query.filter_by(Aadhar_number=Aadhar_number).first()
            if existing_user is None:
                user = UserProfile(Aadhar_number=Aadhar_number, is_woman=is_woman)
                db.session.add(user)
                db.session.commit()

# Define a route to trigger the CSV data import
@app.route('/import_csv')
def trigger_csv_import():
    import_data_from_csv()
    return 'CSV data import complete.'

if __name__ == '__main__':
    app.run(debug=True)
