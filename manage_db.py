from app import app, db
from app.models import User, Event
import json
from datetime import datetime
import os

def backup_database():
    """Backup the database to JSON files"""
    try:
        # Backup Users
        users = User.query.all()
        users_data = []
        for user in users:
            users_data.append({
                'username': user.username,
                'email': user.email,
                'password_hash': user.password_hash,
                'user_type': user.user_type,
                'department': user.department
            })
        
        with open('backup_users.json', 'w') as f:
            json.dump(users_data, f, indent=4)
            
        # Backup Events
        events = Event.query.all()
        events_data = []
        for event in events:
            events_data.append({
                'title': event.title,
                'description': event.description,
                'date': event.date.strftime('%Y-%m-%d'),
                'start_time': event.start_time.strftime('%H:%M:%S'),
                'end_time': event.end_time.strftime('%H:%M:%S'),
                'venue': event.venue,
                'conducted_by': event.conducted_by,
                'incharge': event.incharge,
                'contact': event.contact,
                'registration_link': event.registration_link,
                'organizer_id': event.organizer_id,
                'status': event.status
            })
            
        with open('backup_events.json', 'w') as f:
            json.dump(events_data, f, indent=4)
            
        print("Database backup completed successfully!")
        
    except Exception as e:
        print(f"Error during backup: {str(e)}")

def restore_database():
    """Restore the database from JSON files"""
    try:
        # Create tables
        with app.app_context():
            db.create_all()
            
            # Restore Users
            if os.path.exists('backup_users.json'):
                with open('backup_users.json', 'r') as f:
                    users_data = json.load(f)
                    
                for user_data in users_data:
                    user = User(
                        username=user_data['username'],
                        email=user_data['email'],
                        password_hash=user_data['password_hash'],
                        user_type=user_data['user_type'],
                        department=user_data['department']
                    )
                    db.session.add(user)
                
                db.session.commit()
                print("Users restored successfully!")
                
            # Restore Events
            if os.path.exists('backup_events.json'):
                with open('backup_events.json', 'r') as f:
                    events_data = json.load(f)
                    
                for event_data in events_data:
                    event = Event(
                        title=event_data['title'],
                        description=event_data['description'],
                        date=datetime.strptime(event_data['date'], '%Y-%m-%d').date(),
                        start_time=datetime.strptime(event_data['start_time'], '%H:%M:%S').time(),
                        end_time=datetime.strptime(event_data['end_time'], '%H:%M:%S').time(),
                        venue=event_data['venue'],
                        conducted_by=event_data['conducted_by'],
                        incharge=event_data['incharge'],
                        contact=event_data['contact'],
                        registration_link=event_data['registration_link'],
                        organizer_id=event_data['organizer_id'],
                        status=event_data['status']
                    )
                    db.session.add(event)
                
                db.session.commit()
                print("Events restored successfully!")
                
        print("Database restore completed successfully!")
        
    except Exception as e:
        print(f"Error during restore: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python manage_db.py [backup|restore]")
        sys.exit(1)
        
    command = sys.argv[1].lower()
    
    if command == "backup":
        backup_database()
    elif command == "restore":
        restore_database()
    else:
        print("Invalid command. Use 'backup' or 'restore'") 