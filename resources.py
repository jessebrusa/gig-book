from werkzeug.security import generate_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask import request
from form import weekdays
from datetime import datetime
import math
import os



def check_for_data_return_last(facility_object, table_variable):
    if facility_object:
        return getattr(facility_object[-1], table_variable)
    else:
        return None


def return_list(facility_object, table_variable):
    if facility_object:
        return [getattr(item, table_variable) for item in facility_object]
    else:
        return None


def return_table_list(facility_object):
    if facility_object:
        return [item for item in facility_object]
    else:
        return None


def edit_database(facility_object, request_name, table, table_variable):
    id_list = [data.id for data in facility_object]
    for data_id in id_list:
        request_name_id = f'{request_name}{data_id}'
        request_data = request.form.get(request_name_id)
        if request_data is None:
            pass
        elif len(request_data) == 0:
            pass
        else:
            original_data = table.query.filter_by(id=data_id).first()
            setattr(original_data, table_variable, request_data)

            
def edit_two_database(facility_object, request_name_one, request_name_two,
                      table, table_variation_one, table_variation_two):
    id_list = [data.id for data in facility_object]
    for data_id in id_list:
        request_name_one_id = f'{request_name_one}{data_id}'
        request_name_two_id = f'{request_name_two}{data_id}'

        request_data_one = request.form.get(request_name_one_id)
        request_data_two = request.form.get(request_name_two_id)


        if '-' in str(request_data_two):
            request_data_two = format_date(str(request_data_two))
        elif ':' in str(request_data_two):
            request_data_two = format_time(request_data_two)

        if request_data_one is None:
            pass
        elif len(request_data_one) == 0:
            pass
        elif request_data_one == 'None':
            pass
        else:
            original_data_one = table.query.filter_by(id=data_id).first()
            setattr(original_data_one, table_variation_one, request_data_one)

        if request_data_two is None:
            pass
        elif len(request_data_two) == 0:
            pass
        else:
            original_data_two = table.query.filter_by(id=data_id).first()
            setattr(original_data_two, table_variation_two, request_data_two)


def format_time(time):
    time_object = datetime.strptime(time, '%H:%M')
    return time_object.strftime('%I:%M %p')


def format_date(date):
    date = str(date)
    if '-' in date:
        date_object = datetime.strptime(date, '%Y-%m-%d')
        return date_object.strftime('%m/%d/%Y')


def format_url_date(date):
    date = str(date)
    if '/' in date:
        date_object = datetime.strptime(date, '%m/%d/%Y')
        return date_object.strftime('%Y-%m-%d')


def set_list_form_submit(form):
    set_list_list = []
    if form.set_list_30.data:
        set_list_list.append("30's")
    if form.set_list_40.data:
        set_list_list.append("40's")
    if form.set_list_50.data:
        set_list_list.append("50's")
    if form.set_list_60.data:
        set_list_list.append("60's")
    if form.set_list_70.data:
        set_list_list.append("70's")
    if form.set_list_80.data:
        set_list_list.append("80's")
    if form.set_list_90.data:
        set_list_list.append("90's")
    if form.set_list_2000.data:
        set_list_list.append("2000's")
    if form.set_list_present.data:
        set_list_list.append("Present")
    if form.set_list_outreach.data:
        set_list_list.append("Outreach")
    if form.set_list_christian.data:
        set_list_list.append("Christian")
    if form.set_list_secular.data:
        set_list_list.append("Secular")
    if form.set_list_originals.data:
        set_list_list.append("Originals")
    if form.set_list_worship.data:
        set_list_list.append("Worship")
    if form.set_list_hymns.data:
        set_list_list.append("Hymns")

    return set_list_list


def marketing_form_submit(form):
    date = form.marketing_date.data

    marketing_list = []
    if form.marketing_list_physical_flyer.data:
        marketing_list.append('Physical Flyer')
    if form.marketing_list_electronic_flyer.data:
        marketing_list.append('Electronic Flyer')
    if form.marketing_list_physical_business_card.data:
        marketing_list.append('Physical Business Card')
    if form.marketing_list_epk.data:
        marketing_list.append('EPK')
    if form.marketing_list_chocolate.data:
        marketing_list.append('Chocolate')
    if form.marketing_list_video_clip.data:
        marketing_list.append('Video Clip')
    if form.marketing_list_post_card.data:
        marketing_list.append('Post Card')

    return [marketing_list, date]


def remove_unwanted_char_phone(phone_number):
    phone_string = str(phone_number)
    if ' ' in phone_string:
        phone_string = phone_string.replace(' ', '')
    if '(' in phone_string:
        phone_string = phone_string.replace('(', '')
    if ')' in phone_string:
        phone_string = phone_string.replace(')', '')
    return phone_string


def date_key(date_str):
    return datetime.strptime(date_str, "%m/%d/%Y")


def image_url(form_url, facility_name, **kwargs):
    if kwargs.get('old_file'):
        old_file = kwargs.get('old_file')
        try:
            os.remove(old_file)
        except:
            pass

    file = form_url
    file_string = str(file.filename)

    if file_string.endswith('.jpg'):
        file_type = '.jpg'
    elif file_string.endswith('.jpeg'):
        file_type = '.jpeg'
    elif file_string.endswith('.png'):
        file_type = '.png'

    new_file_string = str(facility_name)

    if ' ' in new_file_string:
        new_file_string = file_string.replace(' ', '_')

    return [file, new_file_string, file_type]


def compare_field(correct_field, field):
    if correct_field == field:
        return True
    else:
        return None


def compare_field_return_data(correct_field, field, facility_object):
    if correct_field == field:
        if facility_object is None:
            return None
        elif '~' in facility_object:
            return facility_object.split('~')
        else:
            return [facility_object]
    else:
        return None


def compare_field_address(correct_field, field, street, town,
                          state, zip_code):
    if correct_field == field:
        return [street, town, state, zip_code]
    else:
        return None


def edit_data_method(correct_field, field, facility_object, request_name):
    if correct_field == field:
        if '~' in str(facility_object):
            list = facility_object.split('~')
            list_len = len(list)
            data_list = []
            for num in range(list_len):
                field_id = f'{request_name}{num}'
                if request.form.get(field_id):
                    data_list.append(request.form.get(field_id))
                else:
                    data_list.append(list[num])
            data_string = ''
            for num in range(len(data_list)):
                data_string += data_list[num]
                if num != len(data_list)-1:
                    data_string += '~'
            if data_list:
                return data_string
        elif request.form.get(f'{request_name}0'):
            return request.form.get(f'{request_name}0')
        else:
            return request.form.get(request_name)


def last_item(list):
    if list:
        return list[-1]
    else:
        return None


def ext_phone(phone_number):
    if phone_number:
        if 'EXT:' in phone_number:
            return phone_number.split('EXT:')[-1]
        else:
            return None
    else:
        return None
    

def phone_to_string(phone_number):
    if phone_number:
        if len(phone_number) == 11:
            pn = phone_number
            return f'+{pn[0]} ({pn[1]}{pn[2]}{pn[3]}) {pn[4]}{pn[5]}{pn[6]} - {pn[7]}{pn[8]}{pn[9]}{pn[10]}'
        elif len(phone_number) == 12:
            pn = phone_number
            return f'+{pn[0]}{pn[1]} ({pn[2]}{pn[3]}{pn[4]}) {pn[5]}{pn[6]}{pn[7]} - {pn[8]}{pn[9]}{pn[10]}{pn[11]}'
        else:
            pn = phone_number
            return f'({pn[0]}{pn[1]}{pn[2]}) {pn[3]}{pn[4]}{pn[5]} - {pn[6]}{pn[7]}{pn[8]}{pn[9]}'
    else:
        return None
 

def format_duration(time):
    if isinstance(time, list):
        duration_time = []
        for i in time:
            hour = math.floor(int(i) / 60)
            min = int(i) % 60
            if hour < 1:
                hour = None
            if min == 0:
                min = None
            duration_time.append([hour, min])
        return duration_time
    else:
        hour = math.floor(int(time) / 60)
        min = int(time) % 60
        if hour < 1:
            hour = None
        if min == 0:
            min = None
        return [hour, min]
    

def edit_address_method(correct_field, field, facility):
    '''Returns a list of street, town, state, and zip_code'''
    if correct_field == field:
        old_street = facility.street
        old_town = facility.town
        old_state = facility.state
        old_zip_code = facility.zip_code

        address_list = []
        if request.form.get(old_street):
            address_list.append(request.form.get(old_street))
        else:
            address_list.append(old_street)
        if request.form.get(old_town):
            address_list.append(request.form.get(old_town))
        else:
            address_list.append(old_town)
        if request.form.get(old_state):
            address_list.append(request.form.get(old_state))
        else:
            address_list.append(old_state)
        if request.form.get(old_zip_code):
            address_list.append(request.form.get(old_zip_code))
        else:
            address_list.append(old_zip_code)
        
        return address_list


def edit_mass_email_method(correct_field, field):
    if correct_field == field:
        if request.form.get('mass_email') == 'on':
            return 'True'
        else:
            return 'False'


def generate_hash_salt(password):
    hash_password = generate_password_hash(
        password,
        method='pbkdf2:sha256:600000',
        salt_length=8)
    return hash_password


def send_email_with_attachment(subject, body, recipient, **kwargs):
    sender = 'book.heatherrae@gmail.com'
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    msg.attach(MIMEText(body, 'html'))

    if kwargs.get('attachment'):
        attachment_filename = kwargs.get('attachment')

        with open(attachment_filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
    
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {attachment_filename}')
        msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, 'gwar syjc svqr cern')
        smtp_server.sendmail(sender, recipient, msg.as_string())
    

def attachment_url(form):
    if form.attachment.data:
        file = form.attachment.data
        file_string = str(file.filename)

        if ' ' in file_string:
            file_string = file_string.replace(' ', '_')

        return [file, file_string]
    else:
        pass


bible_url = 'http://labs.bible.org/api/?'

params = {
    'passage': 'random' 
}

MAPS_DIRECTIONS_API_KEY = 'AIzaSyB7zXC0t9VFRd2DpOBCGqwT8Zk9PjQIDdI'
ORIGIN = '256 Millbury Street, Auburn, Ma, 01501' 