from app import app, db
from models.user import User
from models.property import Property

def create_db():
    with app.app_context():
        db.create_all()
        print("Database and tables created.")

if __name__ == "__main__":
    create_db()