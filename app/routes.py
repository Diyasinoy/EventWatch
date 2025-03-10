from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.models import User, Event
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import calendar as cal

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('calendar'))
        flash('Invalid email or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        user_type = request.form.get('user_type')
        department = request.form.get('department')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return render_template('register.html')
        
        user = User(
            email=email,
            username=username,
            user_type=user_type,
            department=department
        )
        user.password_hash = generate_password_hash(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/calendar')
@login_required
def calendar():
    # Get current date
    today = date.today()
    
    # Get calendar for current month
    month_calendar = cal.monthcalendar(today.year, today.month)
    
    # Get all events for current month
    first_day = date(today.year, today.month, 1)
    if today.month == 12:
        last_day = date(today.year + 1, 1, 1)
    else:
        last_day = date(today.year, today.month + 1, 1)
    
    # Query events
    events = Event.query.filter(
        Event.date >= first_day,
        Event.date < last_day
    ).all()
    
    # Create set of dates with events
    event_dates = {event.date for event in events}
    
    # Prepare calendar data
    calendar_data = []
    for week in month_calendar:
        week_data = []
        for day in week:
            if day != 0:
                current_date = date(today.year, today.month, day)
                day_data = {
                    'day': day,
                    'date': current_date.strftime('%Y-%m-%d'),
                    'has_event': current_date in event_dates,
                    'is_today': current_date == today
                }
            else:
                day_data = {
                    'day': None,
                    'date': None,
                    'has_event': False,
                    'is_today': False
                }
            week_data.append(day_data)
        calendar_data.append(week_data)
    
    return render_template('calendar.html', 
                         calendar_data=calendar_data, 
                         now=today,
                         month_name=today.strftime('%B'),
                         year=today.year)

@app.route('/events/<date>')
@login_required
def events_by_date(date):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        events = Event.query.filter_by(date=date_obj).all()
        return render_template('events_list.html', 
                             events=events, 
                             selected_date=date_obj.strftime('%B %d, %Y'))
    except Exception as e:
        flash('Error loading events. Please try again.')
        return redirect(url_for('calendar'))

@app.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    if request.method == 'POST':
        try:
            new_event = Event(
                title=request.form.get('title'),
                description=request.form.get('description'),
                date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date(),
                start_time=datetime.strptime(request.form.get('start_time'), '%H:%M').time(),
                end_time=datetime.strptime(request.form.get('end_time'), '%H:%M').time(),
                venue=request.form.get('venue'),
                conducted_by=request.form.get('conducted_by'),
                incharge=request.form.get('incharge'),
                contact=request.form.get('contact'),
                registration_link=request.form.get('registration_link'),
                organizer_id=current_user.id
            )
            db.session.add(new_event)
            db.session.commit()
            flash('Event added successfully!')
            return redirect(url_for('calendar'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding event. Please try again.')
    
    return render_template('add_event.html')

@app.route('/event/<int:event_id>')
@login_required
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_details.html', event=event)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500