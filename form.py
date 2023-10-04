from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, \
    EmailField, SelectField, IntegerField, FileField, BooleanField, \
    DateField, TimeField, TextAreaField, FloatField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField


states = [ ('AK'), ('AL'), ('AR'), ('AZ'), ('CA'), ('CO'), ('CT'), ('DC'), ('DE'), ('FL'), ('GA'),
           ('HI'), ('IA'), ('ID'), ('IL'), ('IN'), ('KS'), ('KY'), ('LA'), ('MA'), ('MD'), ('ME'),
           ('MI'), ('MN'), ('MO'), ('MS'), ('MT'), ('NC'), ('ND'), ('NE'), ('NH'), ('NJ'), ('NM'),
           ('NV'), ('NY'), ('OH'), ('OK'), ('OR'), ('PA'), ('RI'), ('SC'), ('SD'), ('TN'), ('TX'),
           ('UT'), ('VA'), ('VT'), ('WA'), ('WI'), ('WV'), ('WY')]

venue_type_list = sorted([('Senior Home: Independent'), ('Senior Home: Assisted'), ('Senior Home: Rehabilitation'), 
                   ('Senior Home: Nursing'), ('Senior Home: Memory Care'), ('Senior Center: Independent'),
                   ('Drug Rehabilitation'), ('Church'), ('Outreach'), ('Festival'), ('Restaurant'),
                   ('Funeral Service'), ('Wedding Ceremony'), ('Company Party'), ('Private Party'), ('Other')])


performance_type_list = [('Sing Through'), ('Small Talk'), ('Story'), ('Chair'), ('Keep Distance'),
                         ('Full Contact'), ('Music Therapy')]


setlist_list = sorted([("30's"), ("40's"), ("50's"), ("60's"), ("70's"), ("80's"), ("90's"),
                ("2000's"), ('Present'),("Outreach"), ("Secular"), ("Christian"),
                ("Originals"), ("Worship"), ("Hymns")])

weekdays = [('Monday'), ('Tuesday'), ('Wednesday'), ('Thursday'), ('Friday'),
            ('Saturday'), ('Sunday')]


feedback_list_items = [('Volume Low'), ('Volume High'), ('Less Upbeat'),
                       ('More Upbeat'), ('Less Dance'), ('More Dance'),
                       ('Less Interaction'), ('More Interaction'), ('Too Short'),
                       ('Too Long')]

marketing_list_items = [('Physical Flyer'), ('Electronic Flyer'), ('Physical Business Cards'),
                        ('EPK'), ('Chocolate'), ('Video Clip'), ('Post Card')]


performance_title_list = [('Hope with Heather Rae'), ('Get Happy with Heather Rae'), ('Come Away with Heather Rae'),
                          ('In the Arms of the Angel with Heather Rae'), ('A Christmas Miracle with Heather Rae'),
                          ('God Bless the USA with Heather Rae'), ('Worship with Heather Rae'), ('Hymns with Heather Rae'),
                          ('Give Thanks with Heather Rae')]

class AddressBookForm(FlaskForm):
    facility = StringField('Facility Name', validators=[DataRequired()])
    contact_person = StringField('Contact Person', validators=[DataRequired()])
    state = SelectField('State', choices=states, validators=[DataRequired()])
    town = StringField('Town', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    zip_code = StringField('Zip Code', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    distance_hour = IntegerField('Distance Time Hour')
    distance_min = IntegerField('Distance Time Minute')
    venue_type = SelectField('Venue Type', choices=[('None')] + venue_type_list, default='None', validators=[DataRequired()])

    location_img_url = FileField('Choose File')
    email = EmailField('Email')
    mass_email = BooleanField('Mass Email List')
    performance_type = SelectField('Performance Type', choices=[('None')] + performance_type_list, default='None')

    set_list_30 = BooleanField("30's")
    set_list_40 = BooleanField("40's")
    set_list_50 = BooleanField("50's")
    set_list_60 = BooleanField("60's")
    set_list_70 = BooleanField("70's")
    set_list_80 = BooleanField("80's")
    set_list_90 = BooleanField("90's")
    set_list_2000 = BooleanField("2000's")
    set_list_present = BooleanField("Present")
    set_list_outreach = BooleanField("Outreach")
    set_list_christian = BooleanField("Christian")
    set_list_secular = BooleanField("Secular")
    set_list_originals = BooleanField("Originals")
    set_list_worship = BooleanField("Worship")
    set_list_hymns = BooleanField("Hymns")

    duration_hour = IntegerField("Duration Hour")
    duration_min = IntegerField("Duration Minute")
    price_date = DateField('Date')
    price = IntegerField('Price')
    preferred_day = SelectField('Preferred Day', choices=[('None')] + weekdays, default='None')
    preferred_time = TimeField('Preferred Time')
    feedback_date = DateField('Feedback Date')
    feedback = SelectField('Feedback_list', choices=[('None')] + feedback_list_items, default='None')
    testimonial_date = DateField('Testimonial Date')
    testimonial = CKEditorField('Testimonials')
    comment = CKEditorField('Comments')
    
    marketing_date = DateField('Date')
    marketing_list_physical_flyer = BooleanField('Physical Flyer')
    marketing_list_electronic_flyer = BooleanField('Electronic Flyer')
    marketing_list_physical_business_card = BooleanField('Physical Business Card')
    marketing_list_epk = BooleanField('EPK')
    marketing_list_chocolate = BooleanField('Chocolate')
    marketing_list_video_clip = BooleanField('Video Clip')
    marketing_list_post_card = BooleanField('Post Card')

    contact_person_edit = StringField('Contact Person Edit')

    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    f_name = StringField('First Name', validators=[DataRequired()])
    l_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    register_password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class MassEmailForm(FlaskForm):
    attachment = FileField('Choose File')
    subject = StringField('Subject', validators=[DataRequired()])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')


class InvoiceForm(FlaskForm):
    title = SelectField('Title Choices')
    date = DateField('Date', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddTitleForm(FlaskForm):
    title = StringField('Title')
    submit = SubmitField('Submit')