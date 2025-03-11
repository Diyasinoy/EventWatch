from app import app, db
from sqlalchemy import text

def update_database():
    with app.app_context():
        try:
            with db.engine.connect() as conn:
                # Add columns to User table
                try:
                    conn.execute(text('ALTER TABLE user ADD COLUMN user_type VARCHAR(20)'))
                    print("Added user_type column")
                except:
                    print("user_type column already exists")

                try:
                    conn.execute(text('ALTER TABLE user ADD COLUMN department VARCHAR(50)'))
                    print("Added department column")
                except:
                    print("department column already exists")

                # Add columns to Event table
                try:
                    conn.execute(text('ALTER TABLE event ADD COLUMN conducted_by VARCHAR(100)'))
                    print("Added conducted_by column")
                except:
                    print("conducted_by column already exists")

                try:
                    conn.execute(text('ALTER TABLE event ADD COLUMN incharge VARCHAR(100)'))
                    print("Added incharge column")
                except:
                    print("incharge column already exists")

                try:
                    conn.execute(text('ALTER TABLE event ADD COLUMN contact VARCHAR(20)'))
                    print("Added contact column")
                except:
                    print("contact column already exists")

                try:
                    conn.execute(text('ALTER TABLE event ADD COLUMN registration_link VARCHAR(200)'))
                    print("Added registration_link column")
                except:
                    print("registration_link column already exists")

            print("\nDatabase update completed successfully!")
            
        except Exception as e:
            print(f"Error updating database: {str(e)}")

if __name__ == "__main__":
    update_database() 