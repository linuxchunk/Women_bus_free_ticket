from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import qrcode
import csv
from datetime import datetime



app = Flask(__name__, static_url_path='/static')


# Configure the database URI (SQLite in this example)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bus_ticket.db'
db = SQLAlchemy(app)

# Define the BusRoute model
class BusRoute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.Integer, unique=True, nullable=False)
    mobile_number = db.Column(db.String(10), nullable=False)
    start_point = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, serial_number, mobile_number, start_point, destination):
        self.serial_number = serial_number
        self.mobile_number = mobile_number
        self.start_point = start_point
        self.destination = destination

    


# Define the UserProfile model for phone numbers and gender
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Aadhar_number = db.Column(db.String(10), unique=True, nullable=False)
    is_woman = db.Column(db.String(10), default=False)

    def __init__(self, Aadhar_number, is_woman=False):
        self.Aadhar_number = Aadhar_number
        self.is_woman = is_woman

# Create the database tables
with app.app_context():
    db.create_all()

## Define a function to import data from the CSV file
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

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    qr_code = None

    if request.method == 'POST':
        start_point = request.form['startPoint']
        destination = request.form['destination']
        Aadhar_number = request.form['mobileNumber']

        # Check if the user exists in the database
        user_profile = UserProfile.query.filter_by(Aadhar_number=Aadhar_number).first()

        if user_profile:
            if user_profile.is_woman == "True":
                # Generate a unique ticket ID (you may want to use a more robust method)
                ticket_id = random.randint(10000, 99999)
                # Create a QR code for the ticket
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(f'Ticket ID: {ticket_id}\nStart: {start_point}\nDestination: {destination}')
                qr.make(fit=True)
                qr_img = qr.make_image(fill_color="black", back_color="white")

                # Save the QR code image
                qr_img.save(f'static/ticket_{ticket_id}.png')

                return render_template('indextemp.html', qr_code=f'static/ticket_{ticket_id}.png')

            else:
                message = "Mens are not allowed for free ticket"
        else:
            message = "User not found in database"


    return render_template('indextemp.html', message=message, qr_code=qr_code)

@app.route('/ticket_count')
def ticket_count():
    total_tickets = Ticket.query.count()
    return render_template('ticket_count.html', total_tickets=total_tickets)


@app.route('/import_csv')
def trigger_csv_import():
    import_data_from_csv()
    return 'CSV data import complete.'


if __name__ == '__main__':
    app.run(debug=True,port=5600)
