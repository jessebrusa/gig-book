from flask import Flask, render_template, redirect, url_for, request, make_response
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from form import AddressBookForm, weekdays, venue_type_list, performance_type_list, \
feedback_list_items, LoginForm, MassEmailForm, InvoiceForm, AddTitleForm
from resources import ext_phone, phone_to_string, format_duration, compare_field, last_item, image_url, \
format_url_date, compare_field_return_data, compare_field_address, edit_data_method,  edit_address_method, \
date_key, edit_mass_email_method, set_list_form_submit, generate_hash_salt, bible_url, params, \
send_email_with_attachment, attachment_url, check_for_data_return_last, return_list, edit_database, \
format_time, edit_two_database, return_table_list, format_date, marketing_form_submit, \
remove_unwanted_char_phone, MAPS_DIRECTIONS_API_KEY, ORIGIN, date_add_days, format_float_as_string
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from functools import wraps
from werkzeug.utils import secure_filename
import requests
from datetime import datetime
from collections import OrderedDict
import os
import re


app = Flask(__name__)
app.config['SECRET_KEY'] = 'das;jklfaowye83oi;jkasdofiu8ow11'
app.config['UPLOAD_FOLDER'] = './static/location_img'
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digital-contact.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)



class DataBase(db.Model):
    __tablename__ = 'database'
    id = db.Column(db.Integer, primary_key=True)
    facility = db.Column(db.String(250), nullable=False)
    town = db.Column(db.String(250), nullable=False)
    street = db.Column(db.String(250), nullable=False)
    state = db.Column(db.String(250), nullable=False)
    zip_code = db.Column(db.String(250), nullable=False)
    distance_hour = db.Column(db.Integer)
    distance_min = db.Column(db.Integer)
    location_img_url = db.Column(db.String(250))
    mass_email = db.Column(db.Boolean)
    mileage = db.Column(db.Integer)

    contact_person = db.relationship('ContactTable')
    email = db.relationship('EmailTable')
    phone_number = db.relationship('PhoneNumberTable')
    preferred_day_time = db.relationship('PreferredDayTimeTable')
    venue_type = db.relationship('VenueTypeTable')
    performance_type = db.relationship('PerformanceTypeTable')
    duration = db.relationship('DurationTable')
    price_date = db.relationship('PriceDateTable')
    setlist = db.relationship('SetlistTable')
    marketing = db.relationship('MarketingTable')
    comments = db.relationship('CommentsTable')
    feedback = db.relationship('FeedbackTable')
    testimonials = db.relationship('TestimonialTable')
    invoice = db.relationship('InvoiceTable')


class ContactTable(db.Model):
    __tablename__ = 'contact_table'
    id = db.Column(db.Integer, primary_key=True)
    contact_person = db.Column(db.String(250), nullable=False)

    data_base_id = db.Column(db.Integer, db.ForeignKey('database.id'))


class PhoneNumberTable(db.Model):
    __tablename__ = 'phone_number_table'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(250), nullable=False)

    data_base_id = db.Column(db.Integer, db.ForeignKey('database.id'))


class EmailTable(db.Model):
    __tablename__ = 'email_table'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250))

    data_base_id = db.Column(db.Integer, db.ForeignKey('database.id'))


class VenueTypeTable(db.Model):
    __tablename__ = 'venue_type_table'
    id = db.Column(db.Integer, primary_key=True)
    venue = db.Column(db.String(250))

    data_base_id = db.Column(db.Integer, db.ForeignKey('database.id'))


class PerformanceTypeTable(db.Model):
    __tablename__ = 'performance_type_table'
    id = db.Column(db.Integer, primary_key=True)
    performance = db.Column(db.String(250))

    data_base_id = db.Column(db.Integer, db.ForeignKey('database.id'))


class DurationTable(db.Model):
    __tablename__ = 'duration_table'
    id = db.Column(db.Integer, primary_key=True)
    hour = db.Column(db.Integer)
    minute = db.Column(db.Integer)

    data_base_id = db.Column(db.Integer, db.ForeignKey('database.id'))    


class PreferredDayTimeTable(db.Model):
    __tablename__ = 'preferred_day_time_table'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(250))
    time = db.Column(db.String(250))

    data_base_id = db.Column(db.Integer, db.ForeignKey('database.id'))


class PriceDateTable(db.Model):
    __tablename__ = 'price_date_table'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    date = db.Column(db.String)

    data_base_id = db.Column(db.Integer, db.ForeignKey('database.id'))


class SetlistTable(db.Model):
    __tablename__ = 'setlist_table'
    id = db.Column(db.Integer, primary_key=True)
    setlist = db.Column(db.String(250))
    
    data_base_id = db.Column(db.Integer, db.ForeignKey('database.id'))


class MarketingTable(db.Model):
    __tablename__ = 'marketing_table'
    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String(250))
    date = db.Column(db.String(250))

    data_base_id = db.Column(db.Integer, db.ForeignKey('database.id'))


class CommentsTable(db.Model):
    __tablename__ = 'comments_table'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(250))

    data_base_id = db.Column(db.Integer, db.ForeignKey('database.id'))


class FeedbackTable(db.Model):
    __tablename__ = 'feedback_table'
    id = db.Column(db.Integer, primary_key=True)
    feedback = db.Column(db.String(250))
    date = db.Column(db.String(250))

    data_base_id = db.Column(db.Integer, db.ForeignKey('database.id'))


class TestimonialTable(db.Model):
    __tablename__ = 'testimonial_table'
    id = db.Column(db.Integer, primary_key=True)
    testimonial = db.Column(db.String(250))
    date = db.Column(db.String(250))

    data_base_id = db.Column(db.Integer, db.ForeignKey('database.id'))


class InvoiceTable(db.Model):
    __tablename__ = 'invoice_table'
    id = db.Column(db.Integer, primary_key=True)
    facility = db.Column(db.String(250))
    street = db.Column(db.String(250))
    town = db.Column(db.String(250))
    state = db.Column(db.String(250))
    zip_code = db.Column(db.String(250))
    date = db.Column(db.String(250))
    due_date = db.Column(db.String(250))
    price = db.Column(db.String(250))
    title = db.Column(db.String(250))
    description = db.Column(db.String(250))
    paid = db.Column(db.Boolean, default=False)
    paid_on = db.Column(db.String(250))

    data_base_id = db.Column(db.Integer, db.ForeignKey('database.id'))
    

class PerformanceTitle(db.Model):
    __tablename__ = 'performance_title'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)


class SubscriptionTable(db.Model):
    __tablename__ = 'subscription_table'
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(250))
    date = db.Column(db.String(250))
    price = db.Column(db.Float)
    rate = db.Column(db.Integer)
    charged_date = db.Column(db.String(250))


class ExpenseTable(db.Model):
    __tablename__ = 'expense_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    price = db.Column(db.Float)
    date = db.Column(db.String(250))


class ProfitTable(db.Model):
    __tablename__ = 'profit_table'
    id = db.Column(db.String(250), primary_key=True)
    name = db.Column(db.String(250))
    price = db.Column(db.Float)
    date = db.Column(db.String(250))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(250), nullable=False)
    l_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def logged_in_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if current_user.is_authenticated:
                return f(*args, **kwargs)
            else:
                return redirect(url_for('login_page'))
        except AttributeError:
            return redirect(url_for('login_page'))
    return decorated_function


@app.route('/', methods=['GET', 'POST'])
# @logged_in_only
def home():
    facilities = DataBase.query.all()
    
    facilities = sorted(facilities, key=lambda x: x.facility)

    facility_names = [facility.facility for facility in facilities]
    length = len(facility_names)

    facility_contacts = [
    check_for_data_return_last(facility.contact_person, 'contact_person') if facility.contact_person else None
    for facility in facilities
    ]

    facility_id = [facility.id for facility in facilities]

    facility_towns = [facility.town for facility in facilities]

    response = requests.get(bible_url, params=params)
    bible_verse = response.text

    town_check = None


    if request.method == 'POST':
        if request.form.get('search_'):
            request_name = request.form.get('search_')

            facilities = DataBase.query.all()
    
            facilities = sorted(facilities, key=lambda x: x.facility)      

            facilities = [facility for facility in facilities 
                          if request_name.lower() in facility.facility.lower() 
                          or request_name.lower() in facility.town.lower()
                          or any(request_name.lower() in contact.contact_person.lower() for contact in facility.contact_person)]

            facility_names = [facility.facility for facility in facilities]
            length = len(facility_names)

            facility_contacts = [
                check_for_data_return_last(facility.contact_person, 'contact_person') if facility.contact_person else None
                for facility in facilities
                ]

            facility_id = [facility.id for facility in facilities]

            facility_towns = [facility.town for facility in facilities]

            town_check = None

        elif request.form.get('option_'):
            if request.form.get('option_') == 'Name':
                facilities = DataBase.query.all()
    
                facilities = sorted(facilities, key=lambda x: x.facility)

                facility_names = [facility.facility for facility in facilities]
                length = len(facility_names)

                facility_contacts = [
                check_for_data_return_last(facility.contact_person, 'contact_person') if facility.contact_person else None
                for facility in facilities
                ]

                facility_id = [facility.id for facility in facilities]

                facility_towns = [facility.town for facility in facilities]

                town_check = None

            
            elif request.form.get('option_') == 'Town':

                facilities = DataBase.query.all()
    
                facilities = sorted(facilities, key=lambda x: x.town)

                facility_names = [facility.facility for facility in facilities]
                length = len(facility_names)

                facility_contacts = [
                    check_for_data_return_last(facility.contact_person, 'contact_person') if facility.contact_person else None
                    for facility in facilities
                    ]

                facility_id = [facility.id for facility in facilities]

                facility_towns = [facility.town for facility in facilities]

                town_check = True


    return render_template('index.html', facility_names=facility_names, facility_contacts=facility_contacts, 
                           length=length, facility_id=facility_id, facility_towns=facility_towns, bible_verse=bible_verse,
                           town_check=town_check)


@app.route('/form', methods=['GET', 'POST'])
# @logged_in_only
def form():
    form = AddressBookForm()

    if request.method == 'POST':

        if form.location_img_url.data:
            url_items = image_url(form.location_img_url.data, 
                                  form.facility.data)
            file = url_items[0]
            file_string = url_items[1]
            file_type = url_items[2]

            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   app.config['UPLOAD_FOLDER'],
                                   secure_filename(f'{file_string}{file_type}')))
            location_img_url = f'../static/location_img/{file_string}{file_type}'
        else:
            location_img_url = None
              

        if form.state.data or form.town.data or form.street or form.zip_code:
            destination_address = f'{form.street.data}, {form.town.data}, {form.state.data}, {form.zip_code.data}'
            maps_url = f'https://maps.googleapis.com/maps/api/directions/json?origin={ORIGIN}&destination={destination_address}&key={MAPS_DIRECTIONS_API_KEY}'

            response = requests.get(maps_url)
            data = response.json()

            if data['status'] == 'OK':
                duration_text = data['routes'][0]['legs'][0]['duration']['text']
                distance_text = data['routes'][0]['legs'][0]['distance']['text']
                parts = duration_text.split(' ')
                travel_hours, travel_minutes = 0, 0  
                for i in range(len(parts)):
                    if parts[i] == 'hour' or parts[i] == 'hours':
                        travel_hours = int(parts[i - 1])
                        if travel_hours == 0:
                            travel_hours = None
                    elif parts[i] == 'min' or parts[i] == 'mins':
                        travel_minutes = int(parts[i - 1])
                        if travel_minutes == 0:
                            travel_minutes = None
                distance_numeric = re.search(r'\d+', distance_text)
    
                if distance_numeric:
                    distance_numeric = int(distance_numeric.group())
                else:
                    distance_numeric = None  
                



        new_entry = DataBase(
            facility = form.facility.data,
            state = form.state.data,
            town = form.town.data,
            street = form.street.data,
            zip_code = form.zip_code.data,
            distance_hour = travel_hours,
            distance_min = travel_minutes,
            location_img_url = location_img_url,
            mass_email = form.mass_email.data,
            mileage = distance_numeric,
        )
        db.session.add(new_entry)
        db.session.commit()

        if form.contact_person.data:
            new_contact = ContactTable(
                contact_person = form.contact_person.data,
                data_base_id = new_entry.id,
            )

            db.session.add(new_contact)
            db.session.commit()


        if form.email.data:
            new_email = EmailTable(
                email = form.email.data,
                data_base_id = new_entry.id
            )

            db.session.add(new_email)
            db.session.commit()


        if form.phone_number.data:
            phone_string = remove_unwanted_char_phone(form.phone_number.data)
            new_phone_number = PhoneNumberTable(
                phone_number = phone_string,
                data_base_id = new_entry.id
            )
            db.session.add(new_phone_number)
            db.session.commit()


        if form.preferred_day.data or form.preferred_time.data:
            if form.preferred_day.data != 'None':
                preferred_day = form.preferred_day.data
            else:
                preferred_day = None
            if form.preferred_time.data:
                preferred_time = format_time(preferred_time)
            else:
                preferred_time = None
            if preferred_day or preferred_time:
                new_preferred_day_time = PreferredDayTimeTable(
                    day = preferred_day,
                    time = preferred_time,
                    data_base_id = new_entry.id
                )
                db.session.add(new_preferred_day_time)
                db.session.commit()


        if form.venue_type.data:
            if form.venue_type.data != 'None':
                venue_type = form.venue_type.data
                new_venue = VenueTypeTable(
                    venue = venue_type,
                    data_base_id = new_entry.id
                )
                db.session.add(new_venue)
                db.session.commit()


        if form.performance_type.data:
            if form.performance_type.data != 'None':
                performance_type = form.performance_type.data
                new_performance = PerformanceTypeTable(
                    performance = performance_type,
                    data_base_id = new_entry.id
                )
                db.session.add(new_performance)
                db.session.commit()


        if form.duration_hour.data or form.duration_min.data:
            new_duration = DurationTable(
                hour = form.duration_hour.data,
                minute = form.duration_min.data,
                data_base_id = new_entry.id
            )
            db.session.add(new_duration)
            db.session.commit()


        if form.price.data or form.price_date.data:
            if form.price_date.data:
                price_date = format_date(str(form.price_date.data))
            else:
                price_date = None
            new_price_date = PriceDateTable(
                price = form.price.data,
                date = price_date,
                data_base_id = new_entry.id
            )
            db.session.add(new_price_date)
            db.session.commit()


        setlist_list = set_list_form_submit(form)
        if setlist_list:
            for item in setlist_list:
                new_setlist = SetlistTable(
                    setlist = item,
                    data_base_id = new_entry.id
                )
                db.session.add(new_setlist)
                db.session.commit()


        marketing_list_date = marketing_form_submit(form)
        if marketing_list_date:
            marketing_list = marketing_list_date[0]
            if marketing_list_date[1]:
                date = marketing_list_date[1]
                date = format_date(date)
            else:
                date = None
            for item in marketing_list:
                new_marketing = MarketingTable(
                    material = item,
                    date = date,
                    data_base_id = new_entry.id
                )
                db.session.add(new_marketing)
                db.session.commit()


        if form.comment.data:
            new_comment = CommentsTable(
                comment = form.comment.data,
                data_base_id = new_entry.id,
            )
            db.session.add(new_comment)
            db.session.commit()


        if form.feedback.data:
            form_feedback = form.feedback.data
            if form_feedback != 'None':
                if form.feedback_date.data:
                    date = format_date(form.feedback_date.data)
                else:
                    date = None
                new_feedback = FeedbackTable(
                    feedback = form_feedback,
                    date = date,
                    data_base_id = new_entry.id,
                )
                db.session.add(new_feedback)
                db.session.commit()


        if form.testimonial.data:
            if form.testimonial_date.data:
                testimonial_date = format_date(form.testimonial_date.data)
            else:
                testimonial_date = None
            new_testimonial = TestimonialTable(
                testimonial = form.testimonial.data,
                date = testimonial_date,
                data_base_id = new_entry.id,
            )
            db.session.add(new_testimonial)
            db.session.commit()


        return redirect(url_for('facility_page', id=new_entry.id))

    return render_template('form.html', form=form)


@app.route('/facility/<int:id>', methods=['GET', 'POST'])
# @logged_in_only
def facility_page(id):
    facility = DataBase.query.filter_by(id=id).first()

    contact_person = check_for_data_return_last(facility.contact_person, 'contact_person')

    distance_hour = facility.distance_hour
    distance_min = facility.distance_min

    phone_number = check_for_data_return_last(facility.phone_number, 'phone_number')
    phone_ext = ext_phone(phone_number)
    phone_string = phone_to_string(phone_number)

    email = check_for_data_return_last(facility.email, 'email')

    venue_type = return_list(facility.venue_type, 'venue')

    performance_type = return_list(facility.performance_type, 'performance')

    duration_list = [[hour_min.hour, hour_min.minute] for hour_min in facility.duration]

    day_time_list = [[day_time.day, day_time.time] for day_time in facility.preferred_day_time]

    price_date_list = [[price_date.price, price_date.date] for price_date in facility.price_date]

    setlist = return_list(facility.setlist, 'setlist')
    if setlist:
        setlist = sorted(setlist)      
 
    market_date_table = return_list(facility.marketing, 'date')
    if market_date_table:
        market_date_list = []
        date_list = []
        facility_marketing = facility.marketing
        
        for date in market_date_table:
            if date not in date_list:
                materials = [item.material for item in facility_marketing if item.date == date]
                market_date_list.append([materials, date])
                date_list.append(date)
    else:
        market_date_list = None

    comments_list = return_list(facility.comments, 'comment')

    feedback_list = [[item.feedback, item.date] for item in facility.feedback]

    testimonials = facility.testimonials


    return render_template('facility-page.html', facility=facility, price_date_list=price_date_list, setlist=setlist,
                           market_date_list=market_date_list, contact_person=contact_person, id=id,
                           phone_number=phone_number, email=email, venue_type=venue_type, performance_type=performance_type, 
                           day_time_list=day_time_list,comments_list=comments_list, duration_list=duration_list,
                           feedback_list=feedback_list, testimonials=testimonials,
                           phone_string=phone_string, 
                           phone_ext=phone_ext, distance_hour=distance_hour, distance_min=distance_min)


@app.route('/add/<int:id>/<field>', methods=['GET', 'POST'])
# @logged_in_only
def add_data(id, field):
    facility = DataBase.query.filter_by(id=id).first()
    form = AddressBookForm()

    location_img = compare_field('image', field)
    contact_person = compare_field('contact_person', field)
    phone_number = compare_field('phone_number', field)
    email = compare_field('email', field)
    venue_type_box = compare_field('venue_type', field)
    preferred_day_time = compare_field('preferred_day_time', field)
    date_price = compare_field('date_price', field)
    market_date = compare_field('market_date',field)
    comments = compare_field('comments', field)
    feedback = compare_field('feedback', field)
    testimonial = compare_field('testimonial', field)

    return render_template('add.html', form=form, facility=facility, contact_person=contact_person,
                           phone_number=phone_number, email=email, venue_type_box=venue_type_box,
                           preferred_day_time=preferred_day_time, date_price=date_price, comments=comments,
                           feedback=feedback, testimonial=testimonial, market_date=market_date, field=field,
                           venue_type_list=venue_type_list, performance_type_list=performance_type_list, 
                           weekdays=weekdays, feedback_list_items=feedback_list_items, location_img=location_img)


@app.route('/commit-add/<int:id>/<field>', methods=['GET', 'POST'])
# @logged_in_only
def commit_add_data(id, field):
    facility = DataBase.query.filter_by(id=id).first()
    form = AddressBookForm()
    
    if request.method == 'POST':       

        if field == 'contact_person':
            new_contact = ContactTable(
                contact_person = request.form.get('contact_person_'),
                data_base_id = id,
            )
            db.session.add(new_contact)
        

        if field == 'image':
            image_file_string_type = image_url(form.location_img_url.data, facility.facility)
            if image_file_string_type:
                image_file_string_type[0].save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                    app.config['UPLOAD_FOLDER'],
                                    secure_filename(f'{image_file_string_type[1]}{image_file_string_type[2]}'))) 
                facility.location_img_url = f'../static/location_img/{image_file_string_type[1]}{image_file_string_type[2]}'


        if field == 'phone_number':
            new_phone_number = PhoneNumberTable(
                phone_number = request.form.get('phone_number_'),
                data_base_id = id,
            )
            db.session.add(new_phone_number)


        if field == 'email':
            new_email = EmailTable(
                email = request.form.get('email_'),
                data_base_id = id,
            )
            db.session.add(new_email)
            db.session.commit()

        if field == 'venue_type':
            request_venue = request.form.get('venue_type_')
            request_performance = request.form.get('performance_type_')
            request_duration_hour = request.form.get('duration_hour_')
            request_duration_min = request.form.get('duration_min_')

            if request_venue:
                new_venue = VenueTypeTable(
                    venue = request_venue,
                    data_base_id = id,
                )
                db.session.add(new_venue)
                db.session.commit()

            if request_performance:
                new_performance = PerformanceTypeTable(
                    performance = request_performance,
                    data_base_id = id,
                )
                db.session.add(new_performance)
                db.session.commit()

            if request_duration_hour or request_duration_min:
                new_duration = DurationTable(
                    hour = request_duration_hour,
                    minute = request_duration_min,
                    data_base_id = id,
                )
                db.session.add(new_duration)
                db.session.commit()
                

        if field == 'preferred_day_time':
            day = request.form.get('preferred_day_')
            time = request.form.get('time_')
            if time:
                time = format_time(time)
            if day or time:
                new_preferred_day_time = PreferredDayTimeTable(
                    day = day,
                    time = time,
                    data_base_id = id
                )
                db.session.add(new_preferred_day_time)
                db.session.commit()
                   

        if field == 'date_price':
            if request.form.get('date_'):
                price_date = format_date(str(request.form.get('date_')))
            else:
                price_date = None
            if len(request.form.get('price_')) == 0:
                pass
            else:
                new_price_date = PriceDateTable(
                    price = request.form.get('price_'),
                    date = price_date,
                    data_base_id = id,
                )
                db.session.add(new_price_date)
                db.session.commit()


        if field == 'market_date':
            marketing_list_date = marketing_form_submit(form)
            if marketing_list_date:
                marketing_list = marketing_list_date[0]
                if marketing_list_date[1]:
                    date = format_date(marketing_list_date[1])
                else:
                    date = None
                for item in marketing_list:
                    new_marketing = MarketingTable(
                        material = item,
                        date = date,
                        data_base_id = id,
                    )
                    db.session.add(new_marketing)
                    db.session.commit()


        if field == 'comments':
            if form.comment.data:
                new_comment = CommentsTable(
                    comment = form.comment.data,
                    data_base_id = id,
                )
                db.session.add(new_comment)
                db.session.commit()


        if field == 'feedback':
            if request.form.get('date_'):
                date = request.form.get('date_')
            else:
                date = None
            if request.form.get('feedback_'):
                feedback = request.form.get('feedback_')
            else:
                feedback = None
            if feedback:
                new_feedback = FeedbackTable(
                    feedback = feedback,
                    date = date,
                    data_base_id = id,
                )
                db.session.add(new_feedback)
                db.session.commit()


        if field == 'testimonial':
            date = request.form.get('date_')
            if date:
                date = format_date(date)
            else:
                date = None
            new_testimonial = TestimonialTable(
                testimonial = form.testimonial.data,
                date = date,
                data_base_id = id,
            )
            db.session.add(new_testimonial)
            db.session.commit()


        db.session.commit()
    return redirect(url_for('facility_page', id=id))


@app.route('/edit-field/<int:id>/<field>', methods=['GET', 'POST'])
# @logged_in_only
def edit_field(id, field):
    facility = DataBase.query.filter_by(id=id).first()
    form = AddressBookForm()

    venue = last_item(compare_field_return_data('facility', field, facility.facility))

    if 'contact_person' == field:
        contacts = return_table_list(facility.contact_person)
    else:
        contacts = None

    if 'distance_time' == field:
        distance_hour = facility.distance_hour
        distance_min = facility.distance_min
    else:
        distance_hour = None
        distance_min = None

    location_img = compare_field_return_data('location_img', field, facility.location_img_url)
    address = compare_field_address('address', field, facility.street, facility.town,
                                    facility.state, facility.zip_code)
    
    if 'phone_number' == field:
        phone_numbers = return_table_list(facility.phone_number)
    else:
        phone_numbers = None

    if 'email' == field:
        emails = return_table_list(facility.email)
        mass_email = facility.mass_email
    else:
        emails = None
        mass_email = None
    
    if 'preferred_day_time' == field:
        days_times = [[day_time.id, day_time.day, day_time.time] for day_time in facility.preferred_day_time]
    else:
        days_times = None


    if 'venue_type' == field or 'performance_type' == field or 'duration_list' == field:
        venue_box = True
        venue_types = return_table_list(facility.venue_type)
        performance_types = return_table_list(facility.performance_type)
        duration_list = [[hour_min.hour, hour_min.minute, hour_min.id] for hour_min in facility.duration]
    else:
        venue_box = None
        venue_types = None
        performance_types = None
        duration_list = None


    if 'date_price' == field:
        price_date_list = [[price_date.price, price_date.date, price_date.id] for price_date in facility.price_date]
    else:
        price_date_list = None

    if 'set_list' == field:
        setlist = return_list(facility.setlist, 'setlist')
        setlist_true = True 
    else:
        setlist = None
        setlist_true = None


    if 'market_date' == field:
        market_date_table = return_list(facility.marketing, 'date')
        if market_date_table:
            market_date_list = []
            date_list = []
            facility_marketing = facility.marketing
            for date in market_date_table:
                if date not in date_list:
                    materials = [item.material for item in facility_marketing if item.date == date]
                    url_date = format_url_date(date)
                    market_date_list.append([materials, date, url_date])
                    date_list.append(date)
    else:
        market_date_list = None


    if 'comments' == field:
        comments = facility.comments
    else:
        comments = None

    if 'feedback' == field:
        feedback_list = facility.feedback
    else:
        feedback_list = None

    if 'testimonial' == field:
        testimonials = facility.testimonials
    else:
        testimonials = facility.testimonials


    return render_template('edit-field.html', id=id, facility=facility, form=form, field=field, venue=venue, contacts=contacts,
                           distance_hour=distance_hour, distance_min=distance_min, setlist_true=setlist_true,
                           phone_numbers=phone_numbers, location_img=location_img, address=address, emails=emails, mass_email=mass_email, days_times=days_times,
                           venue_types=venue_types, venue_type_list=venue_type_list, performance_types=performance_types,
                           performance_type_list=performance_type_list, duration_list=duration_list, venue_box=venue_box, price_date_list=price_date_list,
                           weekdays=weekdays, 
                           setlist=setlist, market_date_list=market_date_list,
                           comments=comments, feedback_list=feedback_list,
                           feedback_list_items=feedback_list_items,
                           testimonials=testimonials)


@app.route('/commit-edit/<int:id>/<string:field>', methods=['GET', 'POST'])
# @logged_in_only
def commit_edit(id, field):
    facility = DataBase.query.filter_by(id=id).first()
    form = AddressBookForm()

    if request.method == 'POST':

        edit_facility = edit_data_method('facility', field, facility.facility, 'facility_')
        if edit_facility:
            facility.facility = edit_facility


        if field == 'contact_person':
            edit_database(facility.contact_person, 'contact_', ContactTable, 'contact_person')


        if field == 'distance_time':
            if request.form.get('distance_hour_') or request.form.get('distance_min_'):
                facility.distance_hour = request.form.get('distance_hour_')
                facility.distance_min = request.form.get('distance_min_')

        if field == 'location_img':
            if form.location_img_url.data:
                edit_img_file_string_type = image_url(form.location_img_url.data, 
                                                      facility.facility, 
                                                      old_file=facility.location_img_url)
                edit_img_file_string_type[0].save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                    app.config['UPLOAD_FOLDER'],
                                    secure_filename(f'{edit_img_file_string_type[1]}{edit_img_file_string_type[2]}')))
                facility.location_img_url = f'../static/location_img/{edit_img_file_string_type[1]}{edit_img_file_string_type[2]}'
                
            else:
                edit_img_file_string_type = None

        
        edit_address = edit_address_method('address', field, facility)
        if edit_address:
            facility.street = edit_address[0]
            facility.town = edit_address[1]
            facility.state = edit_address[2]
            facility.zip_code = edit_address[3]

            destination_address = f'{edit_address[0]}, {edit_address[1]}, {edit_address[2]}, {edit_address[3]}'
            maps_url = f'https://maps.googleapis.com/maps/api/directions/json?origin={ORIGIN}&destination={destination_address}&key={MAPS_DIRECTIONS_API_KEY}'

            response = requests.get(maps_url)
            data = response.json()

            if data['status'] == 'OK':
                duration_text = data['routes'][0]['legs'][0]['duration']['text']
                distance_text = data['routes'][0]['legs'][0]['distance']['text']
                parts = duration_text.split(' ')
                travel_hours, travel_minutes = 0, 0  
                for i in range(len(parts)):
                    if parts[i] == 'hour' or parts[i] == 'hours':
                        travel_hours = int(parts[i - 1])
                        if travel_hours == 0:
                            travel_hours = None
                    elif parts[i] == 'min' or parts[i] == 'mins':
                        travel_minutes = int(parts[i - 1])
                        if travel_minutes == 0:
                            travel_minutes = None
                distance_numeric = re.search(r'\d+', distance_text)
    
                if distance_numeric:
                    distance_numeric = int(distance_numeric.group())
                else:
                    distance_numeric = None 

                if travel_hours:
                    facility.distance_hour = travel_hours
                if travel_minutes:
                    facility.distance_min = travel_minutes
                if distance_numeric:
                    facility.mileage = distance_numeric


        if field == 'phone_number':
            edit_database(facility.phone_number, 'phone_number_', PhoneNumberTable, 'phone_number')


        if field == 'email':
            edit_database(facility.email, 'email_', EmailTable, 'email')

            edit_mass_email = edit_mass_email_method('email', field)
            if edit_mass_email == 'True':
                facility.mass_email = True
            elif edit_mass_email == 'False':
                facility.mass_email = False
            

        if field == 'preferred_day_time':
            edit_two_database(facility.preferred_day_time, 'day_', 'time_', 
                              PreferredDayTimeTable, 'day', 'time')


        if field == 'venue_type':
            edit_database(facility.venue_type, 'venue_type_', VenueTypeTable, 'venue')
            edit_database(facility.performance_type, 'performance_type_', PerformanceTypeTable, 'performance')
            edit_two_database(facility.duration, 'duration_hour_', 'duration_min_', DurationTable,
                          'hour', 'minute')


        if field == 'date_price':
            edit_two_database(facility.price_date, 'price_', 'date_', PriceDateTable, 
                              'price', 'date')
  

        if field == 'set_list':
            original_list = return_list(facility.setlist, 'setlist')
            original_list_table = return_table_list(facility.setlist)
            new_setlist_list = set_list_form_submit(form)
            if new_setlist_list:
                new_item = [item for item in new_setlist_list if item not in original_list]
                if new_item:
                    for item in new_item:
                        new_setlist = SetlistTable(
                            setlist = item,
                            data_base_id = id,
                        )
                        db.session.add(new_setlist)
                        db.session.commit()
                delete_item = [item.id for item in original_list_table if item.setlist not in new_setlist_list]
                if delete_item:
                    for item in delete_item:
                        delete_setlist = SetlistTable.query.filter_by(id=item).first()
                        db.session.delete(delete_setlist)
                        db.session.commit()
            else:
                delete_item = [item.id for item in original_list_table]
                for item in delete_item:
                    delete_setlist = SetlistTable.query.filter_by(id=item).first()
                    db.session.delete(delete_setlist)
                    db.session.commit()


        if 'feedback' == field:
            edit_two_database(facility.feedback, 'feedback_', 'date_',
                              FeedbackTable, 'feedback', 'date')


        db.session.commit()
    
    if 'paid' == field:
        pay_invoice = InvoiceTable.query.filter_by(id=id).first()
        pay_invoice.paid = True

        today = datetime.today()
        today = today.strftime('%m/%d/%Y')
        pay_invoice.paid_on = today

        db.session.commit()
        return redirect(url_for('invoice_list'))
    

    return redirect(url_for('facility_page', id=id))


@app.route('/wtformedit/<int:id>/<field>/<data>', methods=['GET', 'POST'])
# @logged_in_only
def wtform_edit(id, field, data):
    facility = DataBase.query.filter_by(id=id).first()
    form = AddressBookForm()

    if 'market_date' == field:
        market_date_table = return_list(facility.marketing, 'date')
        if market_date_table:
            date = format_date(data)
            materials = [item.material for item in facility.marketing if item.date == date]
            url_date = format_url_date(date)

            market_date_list = [materials, date, url_date]
        else:
            market_date_list = None
    else:
        market_date_list = None


    if 'comments' == field:
        comment = CommentsTable.query.filter_by(id=data).first()
    else:
        comment = None


    if 'testimonial' == field:
        testimonial = TestimonialTable.query.filter_by(id=data).first()
    else:
        testimonial = None

    
    return render_template('wtformedit.html', id=id, field=field, data=data, facility=facility, form=form,
                           market_date_list=market_date_list,
                           comment=comment, testimonial=testimonial
                           )


@app.route('/wtformcommit/<int:id>/<field>/<data>', methods=['GET', 'POST'])
# @logged_in_only
def wtform_commit(id, field, data):
    facility = DataBase.query.filter_by(id=id).first()
    form = AddressBookForm()


    if request.method == 'POST':

        if 'market_date' == field:
            date = format_date(data)
            new_date = form.marketing_date.data
            new_material_list = marketing_form_submit(form)

            material_delete_list = [item.id for item in facility.marketing if item.date == date]
            if len(material_delete_list) >= 0:
                for item in material_delete_list:
                    delete_material = MarketingTable.query.filter_by(id=item).first()
                    db.session.delete(delete_material)
                    db.session.commit()

            material_add_list = [item for item in new_material_list][0]
            if new_date:
                date = format_date(new_date)
            if len(material_add_list) >= 0:
                for item in material_add_list:
                    new_material = MarketingTable(
                        material = item,
                        date = date,
                        data_base_id = id,
                    )
                    db.session.add(new_material)
                    db.session.commit()

            if len(facility.marketing) == 0:
                return redirect(url_for('facility_page', id=id))
            

        if 'comments' == field:
            if form.comment.data:
                edit_comment = CommentsTable.query.filter_by(id=data).first()
                edit_comment.comment = form.comment.data
                db.session.commit()
            
        
        if 'testimonial' == field:
            if form.testimonial.data or request.form.get('date_'):
                testimonial = form.testimonial.data
                date = request.form.get('date_')
                edit_testimonial = TestimonialTable.query.filter_by(id=data).first()
                if date:
                    date = format_date(date)
                    edit_testimonial.date = date
                if testimonial:
                    edit_testimonial.testimonial = form.testimonial.data
                db.session.commit()


    return redirect(url_for('edit_field', id=id, field=field))


@app.route('/previous-contact-data/<int:id>')
# @logged_in_only
def previous_contact(id):
    facility = DataBase.query.filter_by(id=id).first()

    contact_list = return_list(facility.contact_person, 'contact_person')

    phone_list = return_list(facility.phone_number, 'phone_number')

    email_list = return_list(facility.email, 'email')


    return render_template('previous.html', id=id, contact_list=contact_list, 
                           phone_list=phone_list, email_list=email_list)


@app.route('/delete/<int:id>/<field>/<data>', methods=['GET', 'POST'])
# @logged_in_only
def delete_data(id, field, data):
    facility = DataBase.query.filter_by(id=id).first()
    data = data


    if field == 'contact_person':
        if len(facility.contact_person) == 1:
            return redirect(url_for('facility_page', id=id))
        else:
            delete_contact = ContactTable.query.filter_by(id=data).first()
            db.session.delete(delete_contact)


    if field == 'phone_number':
        if len(facility.contact_person) == 1:
            return redirect(url_for('facility_page', id=id))
        else:
            delete_phone_number = PhoneNumberTable.query.filter_by(id=data).first()
            db.session.delete(delete_phone_number)


    if field == 'email':
        delete_email = EmailTable.query.filter_by(id=data).first()
        db.session.delete(delete_email)
        if return_table_list(facility.email) is None:
            db.session.commit()
            return redirect(url_for('facility_page', id=id))


    if field == 'preferred_day_time':
        delete_day_time = PreferredDayTimeTable.query.filter_by(id=data).first()
        db.session.delete(delete_day_time)
        if return_table_list(facility.preferred_day_time) is None:
            db.session.commit()
            return redirect(url_for('facility_page', id=id))
        

    if field == 'venue_type':
        delete_venue = VenueTypeTable.query.filter_by(id=data).first()
        db.session.delete(delete_venue)
        db.session.commit()

    if field == 'performance_type':
        delete_performance = PerformanceTypeTable.query.filter_by(id=data).first()
        db.session.delete(delete_performance)
        db.session.commit()

    if field == 'duration_list':
        delete_duration = DurationTable.query.filter_by(id=data).first()
        db.session.delete(delete_duration)
        db.session.commit()

    if field == 'venue_type' or field == 'performance_type' or field == 'duration_list':
        if return_table_list(facility.venue_type) is None and return_table_list(facility.performance_type) is None \
            and return_table_list(facility.duration) is None:
            return redirect(url_for('facility_page', id=id))


    if field == 'date_price':
        delete_price_date = PriceDateTable.query.filter_by(id=data).first()
        db.session.delete(delete_price_date)
        if return_table_list(facility.price_date) is None:
            db.session.commit()
            return redirect(url_for('facility_page', id=id))

    if field == 'market_date':
        facility_marketing = facility.marketing
        if data == 'NONE':
            delete_items = [item for item in facility_marketing if item.date is None]
        else:
            date = format_date(data)
            delete_items = [item for item in facility_marketing if item.date == date]
        for item in delete_items:
            delete_marketing = MarketingTable.query.filter_by(id=item.id).first()
            db.session.delete(delete_marketing)
            db.session.commit()
            if return_table_list(facility.marketing) is None:
                db.session.commit()
                return redirect(url_for('facility_page', id=id))


    if field == 'comments':
        delete_comment = CommentsTable.query.filter_by(id=data).first()
        db.session.delete(delete_comment)
        if return_table_list(facility.comments) is None:
            db.session.commit()
            return redirect(url_for('facility_page', id=id))


    if field == 'feedback':
        delete_feedback = FeedbackTable.query.filter_by(id=data).first()
        db.session.delete(delete_feedback)
        if return_table_list(facility.feedback) is None:
            db.session.commit()
            return redirect(url_for('facility_page', id=id))


    if field == 'testimonial':
        delete_testimonial = TestimonialTable.query.filter_by(id=data).first()
        db.session.delete(delete_testimonial)
        if return_table_list(facility.testimonials) is None:
            db.session.commit()
            return redirect(url_for('facility_page', id=id))


    if field == 'title':
        delete_title = PerformanceTitle.query.filter_by(id=data).first()
        db.session.delete(delete_title)
        db.session.commit()
        return redirect(url_for('add_title', id=id))


    if field == 'invoice':
        print(data)
        delete_invoice = InvoiceTable.query.filter_by(id=data).first()
        db.session.delete(delete_invoice)
        db.session.commit()
        return redirect(url_for('invoice_list'))


    db.session.commit()
    return redirect (url_for('edit_field', id=id, field=field))


@app.route('/delete-confirm/<int:id>/<string:field>', methods=['GET', 'POST'])
def confirm_page(id, field):
    if field == 'facility':
        facility = DataBase.query.filter_by(id=id).first()
    else: 
        facility = None

    if field == 'invoice':
        invoice = InvoiceTable.query.filter_by(id=id).first()
    else:
        invoice = None


    return render_template('confirm.html', facility=facility, id=id, invoice=invoice)

@app.route('/delete-contact/<int:id>', methods=['GET', 'POST'])
# @logged_in_only
def delete_contact(id):
    facility = DataBase.query.filter_by(id=id).first()

    db.session.delete(facility)
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login_form = LoginForm()
    email_invalid = None
    password_invalid = None

    if request.method == 'POST':
        login_email = login_form.email.data
        login_password = login_form.password.data

        try:
            user = User.query.filter_by(email=login_email).first()
            password_match = check_password_hash(user.password, login_password)

            if password_match:
                login_user(user)

                return redirect(url_for('home'))

            else:
                password_invalid = True

        except:
            email_invalid = True

    return render_template('login.html', form=login_form, email_invalid=email_invalid, password_invalid=password_invalid)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    login_form = LoginForm()

    if request.method == 'POST':
        if login_form:
            f_name = login_form.f_name.data.title()
            l_name = login_form.l_name.data.title()
            email = login_form.email.data
            password = generate_hash_salt(login_form.register_password.data)

            new_user = User(
                f_name = f_name,
                l_name = l_name,
                email = email,
                password = password
            )

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            return redirect(url_for('home'))

    return render_template('register.html', form=login_form)


@app.route('/mass-email', methods=['GET', 'POST'])
# @logged_in_only
def mass_email_page():
    mass_email_form = MassEmailForm()

    if request.method == 'POST':
        attachment = mass_email_form.attachment.data
        if attachment:
            attachment_items = attachment_url(mass_email_form)
            attachment_items[0].save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   'static/temp',
                                   secure_filename(f'{attachment_items[1]}')))
            attachment_path = f'static/temp/{attachment_items[1]}'
        else:
             attachment_path = None
        subject = mass_email_form.subject.data
        body = mass_email_form.body.data

        facilities = DataBase.query.all()
        facilities_email_true = [facility for facility in facilities if facility.mass_email]
        facility_email_list = [facility.email[-1].email for facility in facilities_email_true]
        
        if attachment_path:
            for email in facility_email_list:
                send_email_with_attachment(subject, body, email, attachment=attachment_path)
            os.remove(attachment_path)
        else:
            for email in facility_email_list:
                send_email_with_attachment(subject, body, email)


        return redirect(url_for('home'))

    return render_template('mass-email.html', form=mass_email_form)


@app.route('/invoice-form/<int:id>', methods=['GET', 'POST'])
# @logged_in_only
def invoice_form(id):
    facility = DataBase.query.filter_by(id=id).first()
    form = InvoiceForm()

    title_objects = PerformanceTitle.query.all()
    titles = [title.title for title in title_objects]
    form.title.choices = [(title) for title in titles]

    if request.method == 'POST':
        form_title = form.title.data
        form_date = format_date(form.date.data)
        form_price = form.price.data
        form_description = form.description.data

        form_price = format_float_as_string(form_price)

        new_invoice = InvoiceTable (
            facility = facility.facility,
            street = facility.street,
            town = facility.town,
            state = facility.state,
            zip_code = facility.zip_code,
            date = form_date,
            due_date = date_add_days(form_date, 30),
            price = form_price,
            title = form_title,
            description = form_description,
            data_base_id = id,
        )
        db.session.add(new_invoice)
        db.session.commit()

        invoice_id = new_invoice.id

        return redirect(url_for('invoice', invoice_id=invoice_id))


    return render_template('invoice-form.html', id=id, form=form)


@app.route('/add-title/<int:id>', methods=['GET', 'POST'])
# @logged_in_only
def add_title(id):
    form = AddTitleForm()
    titles = PerformanceTitle.query.all()

    if request.method == 'POST':
        form_title = form.title.data

        if form_title:
            new_title = PerformanceTitle(
                title = form_title
            )
            db.session.add(new_title)
            db.session.commit()

            return redirect(url_for('invoice_form', id=id))


    return render_template('add-title.html', form=form, id=id, titles=titles)


@app.route('/invoice/<int:invoice_id>', methods=['GET', 'POST'])
# @logged_in_only
def invoice(invoice_id):
    invoice = InvoiceTable.query.filter_by(id=invoice_id).first()

    return render_template('invoice.html', invoice=invoice)


@app.route('/invoice-list', methods=['GET', 'POST'])
# @logged_in_only
def invoice_list():
    invoices = InvoiceTable.query.all()
    sorted_invoices = sorted(invoices, key=lambda x: x.date)
    today = datetime.now().replace(hour=23, minute=59, second=59)
    current_year = today.year

    unpaid_invoices = []
    paid_invoices = []
    paid_total = 0
    for invoice in sorted_invoices:
        if invoice.paid:
            paid_invoices.append(invoice)
            paid = float(invoice.price)
            paid_total += paid
        else:
            unpaid_invoices.append(invoice)

    paid_invoices = sorted(paid_invoices, key=lambda x: x.date, reverse=True)

    this_year_paid_invoices = []
    paid_invoices_by_year = {}
    yearly_totals = {} 

    for invoice in paid_invoices:
        invoice_date = datetime.strptime(invoice.date, "%m/%d/%Y")
        invoice_year = invoice_date.year
        
        if invoice_year < current_year:
            if invoice_year not in paid_invoices_by_year:
                paid_invoices_by_year[invoice_year] = []
            paid_invoices_by_year[invoice_year].append(invoice)
        else:
            this_year_paid_invoices.append(invoice)

    for year, invoices in paid_invoices_by_year.items():
        total = sum(float(invoice.price) for invoice in invoices)
        yearly_totals[year] = format_float_as_string(total)

    for year, total in yearly_totals.items():
        yearly_totals[year] = format_float_as_string(float(total))

    paid_invoices_by_year = OrderedDict(sorted(paid_invoices_by_year.items(), key=lambda x: x[0], reverse=True))


    future_invoices = []
    future_total = 0
    overdue_invoices = []
    overdue_total = 0
    current_invoices = []
    current_total = 0
    for invoice in unpaid_invoices:
        due_date = datetime.strptime(invoice.due_date, '%m/%d/%Y')
        start_date = datetime.strptime(invoice.date, '%m/%d/%Y')
        if start_date > today:
            future_invoices.append(invoice)
            future = float(invoice.price)
            future_total += future
        elif due_date < today:
            overdue_invoices.append(invoice)
            overdue = float(invoice.price)
            overdue_total += overdue
        else:
            current_invoices.append(invoice)
            current = float(invoice.price)
            current_total += current

    paid_total = format_float_as_string(paid_total)
    future_total = format_float_as_string(future_total)
    overdue_total = format_float_as_string(overdue_total)
    current_total = format_float_as_string(current_total)

    return render_template('invoice-list.html', this_year_paid_invoices=this_year_paid_invoices, 
                           current_invoices=current_invoices, overdue_invoices=overdue_invoices, 
                           paid_total=paid_total, overdue_total=overdue_total,current_total=current_total, 
                           future_invoices=future_invoices, future_total=future_total, 
                           paid_invoices_by_year=paid_invoices_by_year, yearly_totals=yearly_totals)


@app.route('/profit-expenses', methods=['GET', 'POST'])
# @logged_in_only
def profit_expenses():
    return render_template('profit-expenses.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page'))


if __name__ == "__main__":
    app.run(port=5001, debug=True, host="0.0.0.0")