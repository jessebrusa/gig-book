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
    if '-' in date:
        date_object = datetime.strptime(date, '%Y-%m-%d')
        return date_object.strftime('%m/%d/%Y')


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
        marketing_list.append('electronic Flyer')
    if form.marketing_list_physical_business_card.data:
        marketing_list.append('Physical Business Card')
    if form.marketing_list_epk.data:
        marketing_list.append('EPK')
    if form.marketing_list_chocolate.data:
        marketing_list.append('Chocolate')
    if form.marketing_list_video_clip.data:
        marketing_list.append('Video Clip')

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





def split_list(column):
    if column == None:
        return None
    else:
        if '~' in column:
            column_list = column.split('~')
            if column_list[0] == 'None':
                return None
            else:
                return column_list
        elif column is None:
            return None
        else:
            return [column]
    

def split_break(list):
    if list:
        if '|' in list:
            return list.split('|')
        else:
            return [list]
    else:
        return []


def split_break_dates(list):
    if list:
        dates = []
        items = []
        for item in list:
            if ':' in item:
                date = item.split(':')[0]
                dates.append(date)
                if '|' in item:
                    values = item.split(':')[1].split('|')
                    items.append(values)
                else:
                    values = item.split(':')[1]
                    items.append(values)
            else:
                dates.append("No Date")
                if '|' in item:
                    values = item.split('|')
                    items.append(values)
                else:
                    values = [item]
                    items.append(values)
        return [dates, items]
    else:
        return None


def split_break_itemOne_itemTwo(list):
    if list:
        appended_list = []
        for item in list:
            if '|' in item:
                first_item = item.split('|')[0]
                second_item = item.split('|')[1]
                if ':' in second_item:
                    second_item = format_time(second_item)
            elif '-' not in item:
                first_item = None
                second_item = item
                if ':' in second_item:
                    second_item = format_time(second_item)
            appended_list.append([first_item, second_item])
        return appended_list
    else:
        return None


def split_colon_market_date(list):
    if list:
        appended_list = []
        for item in list:
            if ':' in item:
                appended_list.append([item.split(':')[0].replace('-', '/'),
                                      item.split(':')[1].split('|')])
            elif '|' in item:
                appended_list.append([None, item.split('|')])
            else:
                appended_list.append([None, None])
        return appended_list
    else:
        return None


def compare_field(correct_field, field):
    if correct_field == field:
        return True
    else:
        return None


def list_length(list):
    if list:
        return len(list)
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


def add_data_method(correct_field, field, request_name, facility_object):
    if correct_field == field:
        data = request.form.get(request_name)
        if data:
            if facility_object is None:
                return data
            else:
                return f'{facility_object}~{data}'
        else:
            pass
    else:
        pass


def add_two_data_method(correct_field, field,
                        request_name_one, request_name_two,
                        facility_object):
    if correct_field == field:
        item_one = request.form.get(request_name_one)
        item_two = request.form.get(request_name_two)
        if facility_object is not None:
            if item_one and item_two:
                return f'{facility_object}~{item_one}|{item_two}'
            elif item_one:
                return f'{facility_object}~{item_one}'
            elif item_two:
                return f'{facility_object}~{item_two}'
        else:
            if item_one and item_two:
                return f'{item_one}|{item_two}'
            if item_one:
                return item_one
            if item_two:
                return item_two
    else:
        pass


def add_date_item_method(correct_field, field,
                         request_name_one, request_name_two,
                         facility_object):
    if correct_field == field:
        date = request.form.get(request_name_one)
        item = request.form.get(request_name_two)
        if facility_object is not None:
            if date and item:
                return f'{facility_object}~{date}|{item}'
            if item:
                return f'{facility_object}~{item}'
        else:
            if date and item:
                return f'{date}|{item}'
            if item:
                return item
    else:
        pass


def market_date_method(correct_field, field, facility_object):
    if correct_field == field:
        date = request.form.get('date_')
        physical_flyer = request.form.get('physical_flyer_')
        electronic_flyer = request.form.get('electronic_flyer_')
        business_card = request.form.get('business_card_')
        epk = request.form.get('epk_')
        chocolate = request.form.get('chocolate_')
        video = request.form.get('video_')
        marketing_list = []

        if physical_flyer:
            marketing_list.append('Physical Flyer')
        if electronic_flyer:
            marketing_list.append('Electronic Flyer')
        if business_card:
            marketing_list.append('Physical Business Card')
        if epk:
            marketing_list.append('EPK')
        if chocolate:
            marketing_list.append('Chocolate')
        if video:
            marketing_list.append('Video Clip')

        market_date_string = ''
        if date:
            market_date_string += f'{date}:'
            for num in range(len(marketing_list)):
                market_date_string += marketing_list[num]
                if num != len(marketing_list):
                    market_date_string += '|'
        else:
            for num in range(len(marketing_list)):
                market_date_string += marketing_list[num]
                if num != len(marketing_list):
                    market_date_string += '|'

        if marketing_list:
            if facility_object is not None:
                return f"{facility_object}~{market_date_string}"
            else:
                return market_date_string
    else:
        pass


def add_ckeditor_comment_testimonial_method(correct_field, field, form, facility_object):
    if correct_field == field:
        if correct_field == 'comments':
            data = form.comments_list.data
            date = None
        elif correct_field == 'testimonial':
            data = form.testimonials_list.data
            date = request.form.get('date_')
        if data and date:
            if facility_object is not None:
                return f'{facility_object}~{date}|{data}'
            else:
                return f'{date}|{data}'
        elif data:
            if facility_object is not None:
                return f'{facility_object}~{data}'
            else:
                return data
    else:
        pass


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


def edit_data_method_break(correct_field, field, facility_object,
                           request_name_one, request_name_two):
    if correct_field == field:
        item_one_two_list = []
        if '~' in str(facility_object):
            items = str(facility_object).split('~')
            for item in items:
                if '|' in item:
                    item_one = item.split('|')[0]
                    item_two = item.split('|')[1]
                    item_one_two_list.append([item_one, item_two])
                else:
                    item_one_two_list.append([item])
        elif '~' and '|' not in facility_object:
            item_one_two_list.append([facility_object])
        else:
            if '|' in str(facility_object):
                item_one = facility_object.split('|')[0]
                item_two = facility_object.split('|')[1]
                item_one_two_list.append([item_one, item_two])
            else:
                item_one_two_list.append(facility_object)

        item_by_id = []
        for num in range(len(item_one_two_list)):
            temp_list = []
            item_one_id = f'{request_name_one}{num}'
            item_two_id = f'{request_name_two}{num}'
            if request.form.get(item_one_id) == 'None':
                temp_list.append(item_one_two_list[num][0])
            elif request.form.get(item_one_id) is None:
                temp_list.append(item_one_two_list[num][0])
            elif request.form.get(item_one_id) == '':
                temp_list.append(item_one_two_list[num][0])
            else:
                temp_list.append(request.form.get(item_one_id))
            
            if request.form.get(item_two_id):
                if request.form.get(item_two_id) is None:
                    if ':' in item_one_two_list[num][0]:
                        pass
                    else:
                        temp_list.append(item_one_two_list[num][1])
                else:
                    if ':' in item_one_two_list[num][0]:
                        temp_list = [request.form.get(item_two_id)]
                    else:
                        temp_list.append(request.form.get(item_two_id))
            else:
                try:
                    temp_list.append(item_one_two_list[num][1])
                except IndexError:
                    pass
            if '-' in temp_list[0] and len(temp_list) == 1:
                pass
            else:
                item_by_id.append(temp_list)

        string_list = ''
        for num in range(len(item_by_id)):
            if len(item_by_id[num]) == 2:
                string_list += f'{item_by_id[num][0]}|{item_by_id[num][1]}'
            elif item_by_id[num][0] == None:
                pass
            else:
                string_list += item_by_id[num][0]
            if num != len(item_by_id)-1:
                string_list += '~'
        if item_by_id:
            return string_list
    else:
        return None


def edit_data_date_method(correct_field, field, facility_object, request_name):
    if correct_field == field:
        if '~' in str(facility_object):
            list = facility_object.split('~')
            list_len = len(list)
            data_list = []
            for num in range(list_len):
                date_field = f'date_{num}'
                item_field = f'{request_name}{num}'
                if request.form.get(date_field):
                    date = request.form.get(date_field)
                elif '|' in list[num]:
                    date = list[num].split('|')[0]
                else:
                    date = None

                if request.form.get(item_field):
                    item = request.form.get(item_field)
                else:
                    if '|' in list[num]:
                        item = list[num].split('|')[1]
                    else:
                        item = list[num]
                data_list.append([date, item])

            data_string = ''
            for num in range(len(data_list)):
                if data_list[num][0]:
                    data_string += f'{data_list[num][0]}|{data_list[num][1]}'
                else:
                    data_string += data_list[num][1]
                if num != len(data_list)-1:
                    data_string += '~'
            return data_string
        else:
            date_field = 'date_0'
            item_field = f'{request_name}0'
            if request.form.get(date_field):
                date = request.form.get(date_field)
            else:
                date = None
            if request.form.get(item_field):
                item = request.form.get(item_field)
            else:
                item = list[num]
            if date:
                data_string += f'{date}|{item}'
            else:
                data_string += item
            return data_string
    return None


def delete_data_method(correct_field, field, facility_object, data_num, required):
    if correct_field == field:
        if required:
            if '~' in facility_object:
                items = facility_object.split('~')
                del items[int(data_num)]
                string = ''
                for num in range(len(items)):
                    string += items[num]
                    if num != len(items) - 1:
                        string += '~'
                return string
            else:
                return 'redirect'
        else:
            if '~' in facility_object:
                items = facility_object.split('~')
                del items[int(data_num)]
                string = ''
                for num in range(len(items)):
                    string += items[num]
                    if num != len(items) - 1:
                        string += '~'
                return string
            else:
                return 'None'
    else:
        return None
        

def image_url(correct_field, field, request_name, facility_object):
    if correct_field == field:
        if request.files[request_name]:
            old_file = facility_object.location_img_url

            try:
                os.remove(old_file)
            except:
                pass

            file = request.files[request_name]
            file_string = str(file.filename)

            if file_string.endswith('.jpg'):
                file_type = '.jpg'
            elif file_string.endswith('.jpeg'):
                file_type = '.jpeg'
            elif file_string.endswith('.png'):
                file_type = '.png'

            new_file_string = str(facility_object.facility)

            if ' ' in new_file_string:
                new_file_string = file_string.replace(' ', '_')

            return [file, new_file_string, file_type]
        else:
            pass


def last_item(list):
    if list:
        return list[-1]
    else:
        return None


def split_break_day_time(list):
    if list:
        appended_list = []
        for item in list:
            if '|' in item:
                first_item = item.split('|')[0]
                second_item = format_time(item.split('|')[1])
            elif item in weekdays:
                first_item = item
                second_item = None
            else:
                first_item = None
                second_item = format_time(item)
            appended_list.append([first_item, second_item])
        return appended_list
    else:
        return None


def split_break_date_item(list):
    if list:
        appended_list = []
        for item in list:
            if '|' in item:
                first_item = item.split('|')[0]
                second_item = item.split('|')[1]
            elif '-' in item:
                first_item = item
                second_item = None
            else:
                first_item = None
                second_item = item
            appended_list.append([first_item, second_item])
        return appended_list
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


def marketing_list_form_submit(correct_field, field, form, 
                               facility_object, data):
    if correct_field == field:
        marketing_list_list = []
        market_list_string = ''

        if form.marketing_list_physical_flyer.data:
            marketing_list_list.append('Physical Flyer')
        if form.marketing_list_electronic_flyer.data:
            marketing_list_list.append('Electronic Flyer')
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
            for num in range(len(marketing_list_list)):
                market_list_string += marketing_list_list[num]
                if num != len(marketing_list_list)-1:
                    market_list_string += '|'

        if '~' in facility_object:
            facility_list = facility_object.split('~')
        else:
            facility_list = [facility_object]

        date = request.form.get('date_')
        if date:
            market_list_string = f"{date}:{market_list_string}"
        else:
            if ':' in facility_list[int(data)]:
                date = facility_list[int(data)].split(':')[0]
                market_list_string = f"{date}:{market_list_string}"

        return_string = ''
        for num in range(len(facility_list)):
            if num !=  int(data):
                return_string += facility_list[num]
            else:
                return_string += market_list_string
            if num != len(facility_list)-1:
                return_string += '~'
        return return_string


def wtf_edit_data_market(correct_field, field, data,
                  facility_object):
    if correct_field == field:
        if '~' in facility_object:
            date_market = split_list(facility_object)[int(data)]
        else:
            date_market = facility_object
        if ':' in date_market:
            date_market_label = date_market.split(':')[0]
            date_market_values = date_market.split(':')[1]
            if '|' in date_market_values:
                date_market_values = date_market_values.split('|')
            else:
                date_market_values = [date_market_values]
        else:
            date_market_label = 'No Date'
            date_market_values = date_market
            if '|' in date_market_values:
                date_market_values = date_market_values.split('|')
            else:
                date_market_values = [date_market_values]
        return [date_market, date_market_label, date_market_values]
    return None


def wtf_edit_method(correct_field, field, facility_object, data):
    if correct_field == field:
        return split_list(facility_object)[int(data)]
    else:
        return None


def wtf_edit_ckeditor(correct_field, field, facility_object, 
                      data, form):
    if correct_field == field:
        item_list = split_list(facility_object)
        return_string = ''
        for num in range(len(item_list)):
            if num == int(data):
                if form.comments_list.data:
                    new_item = form.comments_list.data
                    return_string += new_item
                else:
                    return_string += item_list[num]
            else:
                return_string += item_list[num]
            if num != len(item_list)-1:
                return_string += '~'
        return return_string
    else:
        return None


def feedback_dates_values(list):
    if list:
        feedback_dates = []
        feedback_values = []
        for item in list:
            if '|' in item:
                feedback_dates.append(item.split('|')[0])
                feedback_values.append(item.split('|')[1])
            else:
                feedback_dates.append(None)
                feedback_values.append(item)
        return [feedback_dates, feedback_values]
    else:
        return None


def testimonial_dates_values(item):
    if item:
        if '|' in item:
            return [item.split('|')[0], item.split('|')[1]]
        else:
            return [None, item]
    else:
        return None
    

def wtf_edit_testimonial(correct_field, field, facility_object,
                         data, form):
    if correct_field == field:
        item_list = split_list(facility_object)
        return_string = ''
        for num in range(len(item_list)):
            if num == int(data):
                date = request.form.get('date_')
                if form.testimonials_list.data:
                    new_item = form.testimonials_list.data
                    if date:
                        new_item = f'{date}|{new_item}'
                        return_string += new_item
                    elif '|' in item_list[num]:
                        date = item_list[num].split('|')[0]
                        new_item = f'{date}|{new_item}'
                        return_string += new_item
                    else:
                        return_string += new_item
                elif date:
                    if '|' in item_list[num]:
                        item = item_list[num].split('|')[1]
                        return_string += f'{date}|{item}'
                    else:
                        return_string += f'{date}|{item_list[num]}'
                else:
                    return_string += item_list[num]
            else:
                return_string += item_list[num]
            if num != len(item_list)-1:
                return_string += '~'
        return return_string
    else:
        return None
    

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

    msg.attach(MIMEText(body, 'plain'))

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