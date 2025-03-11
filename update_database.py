from app import app, db
from sqlalchemy import text

def update_database():
    with app.app_context():
        try:
            # Add new columns to User table
            with db.engine.connect() as conn:
                # User table updates
                try:
                    conn.execute(text('ALTER TABLE user ADD COLUMN user_type VARCHAR(20)'))
                except Exception as e:
                    print(f"user_type column might already exist: {e}")
                
                try:
                    conn.execute(text('ALTER TABLE user ADD COLUMN department VARCHAR(50)'))
                except Exception as e:
                    print(f"department column might already exist: {e}")

                # Event table updates
                try:
                    conn.execute(text('ALTER TABLE event ADD COLUMN conducted_by VARCHAR(100)'))
                except Exception as e:
                    print(f"conducted_by column might already exist: {e}")
                
                try:
                    conn.execute(text('ALTER TABLE event ADD COLUMN incharge VARCHAR(100)'))
                except Exception as e:
                    print(f"incharge column might already exist: {e}")
                
                try:
                    conn.execute(text('ALTER TABLE event ADD COLUMN contact VARCHAR(20)'))
                except Exception as e:
                    print(f"contact column might already exist: {e}")
                
                try:
                    conn.execute(text('ALTER TABLE event ADD COLUMN registration_link VARCHAR(200)'))
                except Exception as e:
                    print(f"registration_link column might already exist: {e}")

            print("Database update completed!")
            
        except Exception as e:
            print(f"Error updating database: {str(e)}")

if __name__ == "__main__":
    update_database() 