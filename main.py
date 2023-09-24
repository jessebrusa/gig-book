from flask import Flask, render_template, redirect, url_for, \
    flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from form import AddressBookForm, weekdays, venue_type_list, performance_type_list, \
    feedback_list_items, LoginForm, MassEmailForm
from resources import split_list, ext_phone, phone_to_string, format_duration, \
split_break_day_time, split_break_itemOne_itemTwo, split_break, list_length, \
split_colon_market_date, compare_field, add_data_method, last_item, image_url, \
add_two_data_method, add_date_item_method, market_date_method, \
add_ckeditor_comment_testimonial_method, compare_field_return_data, compare_field_address, \
split_break_date_item, edit_data_method, delete_data_method, edit_address_method, \
edit_mass_email_method, edit_data_method_break, set_list_form_submit, split_break_dates, \
wtf_edit_data_market, marketing_list_form_submit, wtf_edit_method, wtf_edit_ckeditor, feedback_dates_values, \
edit_data_date_method, testimonial_dates_values, wtf_edit_testimonial, generate_hash_salt, bible_url, params, \
send_email_with_attachment, attachment_url, check_for_data_return_last
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean
from flask_login import UserMixin, login_user, LoginManager, \
login_required, current_user, logout_user
from functools import wraps
from werkzeug.utils import secure_filename
from datetime import datetime
import requests
import os
import math


app = Flask(__name__)
app.config['SECRET_KEY'] = 'das;jklfaowye83oi;jkasdofiu8ow11'
app.config['UPLOAD_FOLDER'] = './static/location_img'
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///address.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class DataBase(db.Model):
    __tablename__ = 'database'
    id = db.Column(db.Integer, primary_key=True)
    facility = db.Column(db.String(250))
    
    town = db.Column(db.String(250))
    street = db.Column(db.String(250))
    state = db.Column(db.String(250))
    zip_code = db.Column(db.String(250))
    phone_number = db.Column(db.String(250))
    distance_time = db.Column(db.Integer)
    venue_type = db.Column(db.String(250))
    location_img_url = db.Column(db.String(250))
    email = db.Column(db.String(250))
    mass_email = db.Column(db.Boolean)
    performance_type = db.Column(db.String(250))
    set_list = db.Column(db.String(250))
    duration_list = db.Column(db.String(250))
    date_price_list = db.Column(db.String(250))
    preferred_day_time_list = db.Column(db.String(250))
    date_feedback_list = db.Column(db.Text)
    date_testimonials_list = db.Column(db.Text)
    comments_list = db.Column(db.Text)
    date_marketing_list = db.Column(db.String(250))

    contact_person = db.relationship('ContactPerson')


class ContactPerson(db.Model):
    __tablename__ = 'contact_person_table'
    id = db.Column(db.Integer, primary_key=True)
    contact_person = db.Column(db.String(250))

    data_base_id = db.Column(db.Integer, db.ForeignKey('database.id'))


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


def admin_only(f):
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
# @admin_only
def home():
    facilities = DataBase.query.all()
    
    facilities = sorted(facilities, key=lambda x: x.facility)

    facility_names = [last_item(split_list(facility.facility)) for facility in facilities]
    length = len(facility_names)

    facility_contacts = [
    check_for_data_return_last(facility.contact_person).contact_person if facility.contact_person else None
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

            facility_contacts = [
                check_for_data_return_last(facility.contact_person).contact_person.lower() for facility in facilities]
            
            print(facility_contacts)
            print(request_name.lower())

            facilities = [facility for facility in facilities if request_name.lower() in facility.facility.lower() 
                          or request_name.lower() in facility.town.lower()
                          or request_name.lower() in facility_contacts]

            facility_names = [last_item(split_list(facility.facility)) for facility in facilities]
            length = len(facility_names)

            facility_contacts = [
                check_for_data_return_last(facility.contact_person).contact_person if facility.contact_person else None
                for facility in facilities
                ]

            facility_id = [facility.id for facility in facilities]

            facility_towns = [facility.town for facility in facilities]

            town_check = None

        elif request.form.get('option_'):
            if request.form.get('option_') == 'Name':
                facilities = DataBase.query.all()
    
                facilities = sorted(facilities, key=lambda x: x.facility)

                facility_names = [last_item(split_list(facility.facility)) for facility in facilities]
                length = len(facility_names)

                facility_contacts = [
                check_for_data_return_last(facility.contact_person).contact_person if facility.contact_person else None
                for facility in facilities
                ]

                facility_id = [facility.id for facility in facilities]

                facility_towns = [facility.town for facility in facilities]

                town_check = None

            
            elif request.form.get('option_') == 'Town':

                facilities = DataBase.query.all()
    
                facilities = sorted(facilities, key=lambda x: x.town)

                facility_names = [last_item(split_list(facility.facility)) for facility in facilities]
                length = len(facility_names)

                facility_contacts = [
                    check_for_data_return_last(facility.contact_person).contact_person if facility.contact_person else None
                    for facility in facilities
                    ]

                facility_id = [facility.id for facility in facilities]

                facility_towns = [facility.town for facility in facilities]

                town_check = True


    return render_template('index.html', facility_names=facility_names, facility_contacts=facility_contacts, 
                           length=length, facility_id=facility_id, facility_towns=facility_towns, bible_verse=bible_verse,
                           town_check=town_check)


@app.route('/form', methods=['GET', 'POST'])
# @admin_only
def form():
    form = AddressBookForm()

    if request.method == 'POST':
        if form.location_img_url.data:
            file = form.location_img_url.data
            file_string = str(form.location_img_url.data.filename)

            if file_string.endswith('.jpg'):
                file_type = '.jpg'
            elif file_string.endswith('.jpeg'):
                file_type = '.jpeg'
            elif file_string.endswith('.png'):
                file_type = '.png'
            else:
                location_img_url = None

            file_string = str(form.facility.data)

            if ' ' in file_string:
                file_string = file_string.replace(' ', '_')

            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   app.config['UPLOAD_FOLDER'],
                                   secure_filename(f'{file_string}{file_type}')))

            location_img_url = f'../static/location_img/{file_string}{file_type}'

        else:
            location_img_url = None

        if form.email.data:
            email = form.email.data
        else:
            email = None

        if form.performance_type.data != 'None':
            performance_type = form.performance_type.data
        else:
            performance_type = None

        
        set_list_string = set_list_form_submit('no_field', 'no_field', form)


        if form.duration_list.data:
            duration_list = form.duration_list.data
        else:
            duration_list = None
        if form.date.data:
            date = form.date.data
        else:
            date = None

        if form.price_list.data:
            if date:
                price_list = f"{date}|{form.price_list.data}"
            else:
                price_list = form.price_list.data
        else:
            price_list = None

        if form.preferred_day.data != 'None':
            preferred_day = form.preferred_day.data
        else:
            preferred_day = None
        if form.preferred_time.data:
            preferred_time = request.form.get('time_')
        else:
            preferred_time = None

        if preferred_day and preferred_time:
            preferred_day_time = f"{preferred_day}|{preferred_time}"
        elif preferred_day:
            preferred_day_time = preferred_day
        elif preferred_time:
            preferred_day_time = preferred_time
        else:
            preferred_day_time = None

        if form.feedback_list.data != 'None':
            if date:
                feedback = f"{date}|{form.feedback_list.data}"
            else:
                feedback = form.feedback_list.data
        else:
            feedback = None

        if form.testimonials_list.data:
            if date:
                testimonials_list = f"{date}|{form.testimonials_list.data}"
            else:
                testimonials_list = form.testimonials_list.data
        else:
            testimonials_list = None

        if form.comments_list:
            comments_list = form.comments_list.data
        else:
            comments_list = None
        
        marketing_list_list = []
        market_list_string = ''
        if form.marketing_list_physical_flyer.data:
            marketing_list_list.append('Physical Flyer')
        if form.marketing_list_electronic_flyer.data:
            marketing_list_list.append('electronic Flyer')
        if form.marketing_list_physical_business_card.data:
            marketing_list_list.append('Physical Business Card')
        if form.marketing_list_epk.data:
            marketing_list_list.append('EPK')
        if form.marketing_list_chocolate.data:
            marketing_list_list.append('Chocolate')
        if form.marketing_list_video_clip.data:
            marketing_list_list.append('Video Clip')

        if len(marketing_list_list) == 0:
            market_list_string = None
        elif len(marketing_list_list) == 1:
            market_list_string += marketing_list_list[0]
        else:
            market_list_string += marketing_list_list[0]
            for material in marketing_list_list[1:]:
                market_list_string += '|'
                market_list_string += material
        if date:
            market_list_string = f"{date}:{market_list_string}"

        if form.date.data:
            date = form.date.data
        else:
            date = None

        phone_string = str(form.phone_number.data)
        if ' ' in phone_string:
            phone_string = phone_string.replace(' ', '')
        if '(' in phone_string:
            phone_string = phone_string.replace('(', '')
        if ')' in phone_string:
            phone_string = phone_string.replace(')', '')

        if form.venue_type.data == 'None':
            venue_type = None
        else:
            venue_type = form.venue_type.data

        new_entry = DataBase(
            facility = form.facility.data,
            state = form.state.data,
            town = form.town.data,
            street = form.street.data,
            zip_code = form.zip_code.data,
            phone_number = phone_string,
            distance_time = form.distance_time.data,
            venue_type = venue_type,
            location_img_url = location_img_url,
            email = email,
            mass_email = form.mass_email.data,
            performance_type = performance_type,
            set_list = set_list_string,
            duration_list = duration_list,
            date_feedback_list = feedback,
            date_price_list = price_list,
            preferred_day_time_list = preferred_day_time,
            date_testimonials_list = testimonials_list,
            comments_list = comments_list,
            date_marketing_list = market_list_string
        )

        db.session.add(new_entry)
        db.session.commit()

        new_contact = ContactPerson(
            contact_person = form.contact_person.data,
            data_base_id = new_entry.id,
        )

        db.session.add(new_contact)
        db.session.commit()



        return redirect(url_for('facility_page', id=new_entry.id))

    return render_template('form.html', form=form)


@app.route('/facility/<int:id>', methods=['GET', 'POST'])
# @admin_only
def facility_page(id):
    facility = DataBase.query.filter_by(id=id).first()

    contact_person = check_for_data_return_last(facility.contact_person)
    if contact_person:
        contact_person = contact_person.contact_person

    phone_number = last_item(split_list(facility.phone_number))
    phone_ext = ext_phone(phone_number)
    phone_string = phone_to_string(phone_number)

    email = last_item(split_list(facility.email))

    venue_type = split_list(facility.venue_type)

    performance_type = split_list(facility.performance_type)

    duration_list = split_list(facility.duration_list)
    duration_time = format_duration(facility.duration_list, duration_list)

    day_time_array = split_list(facility.preferred_day_time_list)
    day_time_list = split_break_day_time(day_time_array)

    date_price_array = split_list(facility.date_price_list)
    date_price_list = split_break_itemOne_itemTwo(date_price_array)  

    comments_list = split_list(facility.comments_list)
    comments_list_length = list_length(comments_list)

    set_list = split_break(facility.set_list)

    market_date_array = split_list(facility.date_marketing_list)
    market_date_list = split_colon_market_date(market_date_array)

    feedback_array = split_list(facility.date_feedback_list)
    feedback_list = split_break_itemOne_itemTwo(feedback_array)
    feedback_list_length = list_length(feedback_array)


    testimonial_array = split_list(facility.date_testimonials_list)
    testimonial_list = split_break_itemOne_itemTwo(testimonial_array)
    testimonial_list_length = list_length(testimonial_array)

    return render_template('facility-page.html', facility=facility, date_price_list=date_price_list, set_list=set_list,
                           market_date_list=market_date_list,contact_person=contact_person, id=id,
                           phone_number=phone_number, email=email, venue_type=venue_type, performance_type=performance_type, 
                           duration_time=duration_time, day_time_list=day_time_list,comments_list=comments_list, 
                           comments_list_length=comments_list_length,feedback_list=feedback_list, feedback_list_length=feedback_list_length ,
                           testimonial_list=testimonial_list, testimonial_list_length=testimonial_list_length , phone_string=phone_string, 
                           phone_ext=phone_ext)


@app.route('/add/<int:id>/<field>', methods=['GET', 'POST'])
# @admin_only
def add_data(id, field):
    facility = DataBase.query.filter_by(id=id).first()
    form = AddressBookForm()
    
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
                           weekdays=weekdays, feedback_list_items=feedback_list_items)


@app.route('/commit-add/<int:id>/<field>', methods=['GET', 'POST'])
# @admin_only
def commit_add_data(id, field):
    facility = DataBase.query.filter_by(id=id).first()
    form = AddressBookForm()
    
    if request.method == 'POST':       
        
        # new_contact = add_data_method('contact_person', field, 
        #                               'contact_person_', facility.contact_person)
        # if new_contact:
        #     facility.contact_person = new_contact

        if field == 'contact_person':
            new_contact = ContactPerson(
                contact_person = request.form.get('contact_person_'),
                data_base_id = id,
            )
            db.session.add(new_contact)
            db.session.commit()
        

        image_file_string_type = image_url('location_img', field, 'location_img_new', facility.location_img_url)
        if image_file_string_type:
            image_file_string_type[0].save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                app.config['UPLOAD_FOLDER'],
                                secure_filename(f'{image_file_string_type[1]}{image_file_string_type[2]}'))) 
            facility.location_img_url = f'../static/location_img/{image_file_string_type[1]}{image_file_string_type[2]}'


        new_phone_number = add_data_method('phone_number', field,
                                           'phone_number_', facility.phone_number)
        if new_phone_number:
            facility.phone_number = new_phone_number


        new_email = add_data_method('email', field, 'email_', facility.email)
        if new_email:
            facility.email = new_email
            

        new_venue = add_data_method('venue_type', field, 
                                    'venue_type_', facility.venue_type)
        new_performance_type = add_data_method('venue_type', field, 
                                               'performance_type_', facility.performance_type) 
        new_duration = add_data_method('venue_type', field,
                                            'duration_', facility.duration_list)
        if new_venue:
            facility.venue_type = new_venue
        if new_performance_type:
            facility.performance_type = new_performance_type
        if new_duration:
            facility.duration_list = new_duration 


        new_preferred_day_time = add_two_data_method('preferred_day_time', field,
                                                     'preferred_day_', 'time_',
                                                     facility.preferred_day_time_list)
        if new_preferred_day_time:
            facility.preferred_day_time_list = new_preferred_day_time
                   

        new_date_price = add_date_item_method('date_price', field,
                                              'date_', 'price_',
                                              facility.date_price_list)
        if new_date_price:
            facility.date_price_list = new_date_price


        new_market_date = market_date_method('market_date', field, 
                                             facility.date_marketing_list)
        if new_market_date:
            facility.date_marketing_list = new_market_date


        new_comment = add_ckeditor_comment_testimonial_method('comments', field, 
                                                  form, facility.comments_list)
        if new_comment:
            facility.comments_list = new_comment


        new_feedback = add_date_item_method('feedback', field,
                                            'date_', 'feedback_',
                                            facility.date_feedback_list)
        if new_feedback:
            facility.date_feedback_list = new_feedback


        new_testimonial = add_ckeditor_comment_testimonial_method('testimonial', field,
                                                                  form, facility.date_testimonials_list)
        if new_testimonial:
            facility.date_testimonials_list = new_testimonial


        db.session.commit()
    return redirect(url_for('facility_page', id=id))


@app.route('/edit-field/<int:id>/<field>', methods=['GET', 'POST'])
# @admin_only
def edit_field(id, field):
    facility = DataBase.query.filter_by(id=id).first()
    form = AddressBookForm()

    venue = last_item(compare_field_return_data('facility', field, facility.facility))
    # contacts = compare_field_return_data('contact_person', field, facility.contact_person)

    if field == 'contact_person':
        contacts = facility.contact_person
    else:
        contacts = None
    distance_time = last_item(compare_field_return_data('distance_time', field, str(facility.distance_time)))
    location_img = compare_field_return_data('location_img', field, facility.location_img_url)
    address = compare_field_address('address', field, facility.street, facility.town,
                                    facility.state, facility.zip_code)
    phone_numbers = compare_field_return_data('phone_number', field, facility.phone_number)
    phone_numbers_len = list_length(phone_numbers)
    emails = compare_field_return_data('email', field, facility.email)
    emails_len = list_length(emails)
    mass_email = facility.mass_email
    preferred_day_time = compare_field_return_data('preferred_day_time', field,
                                                   facility.preferred_day_time_list)
    days_times = split_break_itemOne_itemTwo(preferred_day_time)
    days_times_len = list_length(days_times)
    venue_types = compare_field_return_data('venue_type', field, facility.venue_type)
    venue_types_len = list_length(venue_types)
    performance_types = compare_field_return_data('venue_type', field, facility.performance_type)
    performance_types_len = list_length(performance_types)
    duration_list = compare_field_return_data('venue_type', field, facility.duration_list)
    duration_list_len = list_length(duration_list)
    venue_box = compare_field('venue_type', field)
    date_price_array = compare_field_return_data('date_price', field, facility.date_price_list)
    date_price_list = split_break_date_item(date_price_array)   
    date_price_list_len = list_length(date_price_list)
    set_list = compare_field('set_list', field) 
    set_list_array = split_break(facility.set_list)
    date_market = compare_field_return_data('market_date', field, facility.date_marketing_list)
    if date_market:
        date_market_labels = split_break_dates(date_market)[0]
        date_market_values = split_break_dates(date_market)[1]
    else:
        date_market_labels = None
        date_market_values = None
    date_market_len = list_length(date_market)
    comments = compare_field_return_data('comments', field, facility.comments_list)
    comments_len = list_length(comments)
    feedback = compare_field_return_data('feedback', field, facility.date_feedback_list)
    if feedback:
        feedback_items = feedback_dates_values(feedback)
        feedback_dates = feedback_items[0]
        feedback_values = feedback_items[1]
    else:
        feedback_dates = None
        feedback_values = None
    feedback_len = list_length(feedback)
    testimonials_list = compare_field_return_data('testimonial', field, facility.date_testimonials_list)
    if testimonials_list:
        testimonial_items = feedback_dates_values(testimonials_list)
        testimonial_dates = testimonial_items[0]
        testimonial_values = testimonial_items[1]
    else:
        testimonial_dates = None
        testimonial_values = None
    testimonials_list_len = list_length(testimonials_list)




    return render_template('edit-field.html', id=id, facility=facility, form=form, field=field, venue=venue, contacts=contacts,
                           distance_time=distance_time, venue_types_len=venue_types_len, performance_types_len=performance_types_len, duration_list_len=duration_list_len,
                           phone_numbers=phone_numbers, location_img=location_img, address=address, emails=emails, mass_email=mass_email, days_times=days_times,
                           days_times_len=days_times_len, venue_types=venue_types, venue_type_list=venue_type_list, performance_types=performance_types,
                           performance_type_list=performance_type_list, duration_list=duration_list, venue_box=venue_box, date_price_list=date_price_list,
                           phone_numbers_len=phone_numbers_len, emails_len=emails_len, weekdays=weekdays, date_price_list_len=date_price_list_len,
                           set_list=set_list, set_list_array=set_list_array, date_market=date_market, date_market_len=date_market_len, date_market_labels=date_market_labels,
                           date_market_values=date_market_values, comments=comments, comments_len=comments_len, feedback=feedback, feedback_len=feedback_len,
                           feedback_list_items=feedback_list_items, feedback_dates=feedback_dates, feedback_values=feedback_values, testimonials_list=testimonials_list,
                           testimonial_dates=testimonial_dates, testimonial_values=testimonial_values, testimonials_list_len=testimonials_list_len)


@app.route('/commit-edit/<int:id>/<field>', methods=['GET', 'POST'])
# @admin_only
def commit_edit(id, field):
    facility = DataBase.query.filter_by(id=id).first()
    form = AddressBookForm()

    if request.method == 'POST':

        edit_facility = edit_data_method('facility', field, facility.facility, 'facility_')
        if edit_facility:
            facility.facility = edit_facility

        edit_contact_person = edit_data_method('contact_person', field, 
                                                    facility.contact_person, 'contact_person_')
        if edit_contact_person:
            facility.contact_person = edit_contact_person


        edit_distance_time = edit_data_method('distance_time', field, 
                                              facility.distance_time, 'distance_time_')
        if edit_distance_time:
            facility.distance_time = edit_distance_time


        edit_img_file_string_type = image_url('location_img', field,
                                 'location_img_new', facility)
        if edit_img_file_string_type:
            edit_img_file_string_type[0].save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                app.config['UPLOAD_FOLDER'],
                                secure_filename(f'{edit_img_file_string_type[1]}{edit_img_file_string_type[2]}')))
            facility.location_img_url = f'../static/location_img/{edit_img_file_string_type[1]}{edit_img_file_string_type[2]}'

        
        edit_address = edit_address_method('address', field, facility)
        if edit_address:
            facility.street = edit_address[0]
            facility.town = edit_address[1]
            facility.state = edit_address[2]
            facility.zip_code = edit_address[3]


        edit_phone_number = edit_data_method('phone_number', field, 
                                             facility.phone_number, 'phone_number_')
        if edit_phone_number:
            facility.phone_number = edit_phone_number

        
        edit_email = edit_data_method('email', field, facility.email, 'email_')
        if edit_email:
            facility.email = edit_email

        edit_mass_email = edit_mass_email_method('email', field)
        if edit_mass_email == 'True':
            facility.mass_email = True
        elif edit_mass_email == 'False':
            facility.mass_email = False
            

        edit_preferred_day_time = edit_data_method_break('preferred_day_time', field,
                                                    facility.preferred_day_time_list,
                                                    'day_', 'time_')
        if edit_preferred_day_time:
            facility.preferred_day_time_list = edit_preferred_day_time


        edit_venue_type = edit_data_method('venue_type', field, 
                                           facility.venue_type, 'venue_type_')
        if edit_venue_type:
            facility.venue_type = edit_venue_type

        
        edit_performance_type = edit_data_method('venue_type', field,
                                                 facility.performance_type, 'performance_type_')
        if edit_performance_type:
            facility.performance_type = edit_performance_type

    
        edit_duration_list = edit_data_method('venue_type', field,
                                              facility.duration_list, 'duration_list_')
        if edit_duration_list:
            facility.duration_list = edit_duration_list        


        edit_date_price = edit_data_method_break('date_price', field,
                                                 facility.date_price_list,
                                                 'date_', 'price_')
        if edit_date_price:
            facility.date_price_list = edit_date_price
  

        edit_set_list = set_list_form_submit('set_list', field, form)
        if edit_set_list == 'empty':
            facility.set_list = None
        elif edit_set_list:
            facility.set_list = edit_set_list


        edit_feedback = edit_data_date_method('feedback', field, 
                                              facility.date_feedback_list,
                                              'feedback_')
        if edit_feedback:
            facility.date_feedback_list = edit_feedback 


        db.session.commit()
    return redirect(url_for('facility_page', id=id))


@app.route('/wtformedit/<int:id>/<field>/<data>', methods=['GET', 'POST'])
# @admin_only
def wtform_edit(id, field, data):
    facility = DataBase.query.filter_by(id=id).first()
    form = AddressBookForm()

    date_market_items = wtf_edit_data_market('market_date', field, data,
                                             facility.date_marketing_list)
    if date_market_items:
        date_market = date_market_items[0]
        date_market_label = date_market_items[1]
        date_market_values = date_market_items[2]
    else:
        date_market = None
        date_market_label = None
        date_market_values = None


    comment = wtf_edit_method('comments', field,
                               facility.comments_list, data)
    

    testimonial_item = wtf_edit_method('testimonial', field,
                                       facility.date_testimonials_list,
                                       data)
    if testimonial_item:
        testimonial_items = testimonial_dates_values(testimonial_item)
        testimonial_date = testimonial_items[0]
        testimonial_value = testimonial_items[1]
    else:
        testimonial_items = None
        testimonial_date = None
        testimonial_value = None
    
    return render_template('wtformedit.html', id=id, field=field, data=data, facility=facility, form=form,
                           date_market=date_market, date_market_label=date_market_label, date_market_values=date_market_values,
                           comment=comment, testimonial_item=testimonial_item, testimonial_date=testimonial_date,
                           testimonial_value=testimonial_value)


@app.route('/wtformcommit/<int:id>/<field>/<data>', methods=['GET', 'POST'])
# @admin_only
def wtform_commit(id, field, data):
    facility = DataBase.query.filter_by(id=id).first()
    form = AddressBookForm()


    if request.method == 'POST':

        edit_date_market = marketing_list_form_submit('market_date', field, form,
                                                        facility.date_marketing_list, data)
        if edit_date_market:
            facility.date_marketing_list = edit_date_market
            if facility.date_marketing_list is not None:
                db.session.commit()
                return redirect(url_for('edit_field', id=id, field='market_date'))
              
        edit_comment = wtf_edit_ckeditor('comments', field, facility.comments_list, data, form)
        if edit_comment:
            facility.comments_list = edit_comment
            if facility.comments_list is not None:
                db.session.commit()
                return redirect(url_for('edit_field', id=id, field='comments'))
            
        
        edit_testimonial = wtf_edit_testimonial('testimonial', field,
                                                facility.date_testimonials_list, data, form)
        if edit_testimonial:
            facility.date_testimonials_list = edit_testimonial
            if facility.date_testimonials_list is not None:
                db.session.commit()
                return redirect(url_for('edit_field', id=id, field='testimonial'))

    return redirect(url_for('edit_field', id=id, field=field))


@app.route('/previous-contact-data/<int:id>')
# @admin_only
def previous_contact(id):
    facility = DataBase.query.filter_by(id=id).first()

    contact_list = [contact.contact_person for contact in facility.contact_person]

    phone_list = split_list(facility.phone_number)

    email_list = split_list(facility.email)


    return render_template('previous.html', id=id, contact_list = contact_list, phone_list=phone_list, email_list=email_list)


@app.route('/delete/<int:id>/<field>/<int:data>', methods=['GET', 'POST'])
# @admin_only
def delete_data(id, field, data):
    facility = DataBase.query.filter_by(id=id).first()
    data = data


    # delete_contact = delete_data_method('contact_person', field, 
    #                                     facility.contact_person, data, True)
    # if delete_contact:
    #     if delete_contact == 'redirect':
    #         return redirect(url_for('facility_page', id=id))  
    #     else:
    #         facility.contact_person = delete_contact

    if field == 'contact_person':
        delete_contact = ContactPerson.query.filter_by(id=data).first()
        db.session.delete(delete_contact)
        db.session.commit()



    delete_phone_number = delete_data_method('phone_number', field, 
                                             facility.phone_number, data, True)
    if delete_phone_number:
        if delete_phone_number == 'redirect':
            return redirect(url_for('facility_page', id=id))
        else:
            facility.phone_number = delete_phone_number


    delete_email = delete_data_method('email', field,
                                      facility.email, data, False)
    if delete_email:
        if delete_email == 'None':
            facility.email = None
            db.session.commit()
            return redirect(url_for('facility_page', id=id))
        else:
            facility.email = delete_email


    delete_preferred_day_time = delete_data_method('preferred_day_time', field,
                                                   facility.preferred_day_time_list,
                                                   data, False)
    if delete_preferred_day_time:
        if delete_preferred_day_time == 'None':
            facility.preferred_day_time_list = None
            db.session.commit()
            return redirect(url_for('facility_page', id=id))
        else:
            facility.preferred_day_time_list = delete_preferred_day_time


    delete_venue_type = delete_data_method('venue_type', field,
                                           facility.venue_type,
                                           data, False)
    if delete_venue_type:
        if delete_venue_type == 'None':
            facility.venue_type = None
            db.session.commit()
            if facility.venue_type is None and facility.performance_type is None and facility.duration_list is None:
                return redirect(url_for('facility_page', id=id))
        else:
            facility.venue_type = delete_venue_type

    
    delete_performance_type = delete_data_method('performance_type', field,
                                                 facility.performance_type,
                                                 data, False)
    if delete_performance_type:
        if delete_performance_type == 'None':
            facility.performance_type = None
            db.session.commit()
            field = 'venue_type'
            if facility.venue_type is None and facility.performance_type is None and facility.duration_list is None:
                return redirect(url_for('facility_page', id=id))
        else:
            facility.performance_type = delete_performance_type
            field = 'venue_type'

    
    delete_duration_list = delete_data_method('duration_list', field,
                                              facility.duration_list,
                                              data, False)
    if delete_duration_list:
        if delete_duration_list == 'None':
            facility.duration_list = None
            db.session.commit()
            field = 'venue_type'
            if facility.venue_type is None and facility.performance_type is None and facility.duration_list is None:
                return redirect(url_for('facility_page', id=id))
        else:
            facility.duration_list = delete_duration_list
            field = 'venue_type'


    delete_date_price = delete_data_method('date_price', field,
                                           facility.date_price_list,
                                           data, False)
    if delete_date_price:
        if delete_date_price == 'None':
            facility.date_price_list = None
            db.session.commit()
            return redirect(url_for('facility_page', id=id))
        else:
            facility.date_price_list = delete_date_price


    delete_date_market = delete_data_method('market_date', field,
                                            facility.date_marketing_list,
                                            data, False)
    if delete_date_market:
        if delete_date_market == 'None':
            facility.date_marketing_list = None
            db.session.commit()
            return redirect(url_for('facility_page', id=id))
        else:
            facility.date_marketing_list = delete_date_market


    delete_comment = delete_data_method('comments', field,
                                        facility.comments_list,
                                        data, False)
    if delete_comment:
        if delete_comment == 'None':
            facility.comments_list = None
            db.session.commit()
            return redirect(url_for('facility_page', id=id))
        else:
            facility.comments_list = delete_comment


    delete_feedback = delete_data_method('feedback', field,
                                         facility.date_feedback_list,
                                         data, False)
    if delete_feedback:
        if delete_feedback == 'None':
            facility.date_feedback_list = None
            db.session.commit()
            return redirect(url_for('facility_page', id=id))
        else:
            facility.date_feedback_list = delete_feedback


    delete_testimonial = delete_data_method('testimonial', field, facility.date_testimonials_list,
                                            data, False)
    if delete_testimonial:
        if delete_testimonial == 'None':
            facility.date_testimonials_list = None
            db.session.commit()
            return redirect(url_for('facility_page', id=id))
        else:
            facility.date_testimonials_list = delete_testimonial


    db.session.commit()
    return redirect (url_for('edit_field', id=id, field=field))


@app.route('/delete-contact/<int:id>', methods=['GET', 'POST'])
# @admin_only
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
# @admin_only
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
        facility_email_list = [split_list(facility.email)[-1] for facility in facilities_email_true]
               

        if attachment_path:
            for email in facility_email_list:
                send_email_with_attachment(subject, body, email, attachment=attachment_path)
        else:
            for email in facility_email_list:
                send_email_with_attachment(subject, body, email)

        return redirect(url_for('home'))

    return render_template('mass-email.html', form=mass_email_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page'))


if __name__ == "__main__":
    app.run(port=5001, debug=True)