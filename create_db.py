# create_db.py
from fiskvibe import db, app

with app.app_context():
    db.create_all()  # Creating tables
    print("Database and tables created successfully.") #just to verify
