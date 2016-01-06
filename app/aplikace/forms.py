from flask_wtf import Form
from flask.ext.babel import gettext
from wtforms import TextField, PasswordField, BooleanField,FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length
import re


class FileUploadForm(Form):
    #fileName = FieldList(FileField())
    filename        = FileField(u'Soubor xml')
    #, [validators.regexp(u'^[^/\\]\.xml$')])
    #image        = FileField(u'Image File', [validators.regexp(u'^[^/\\]\.jpg$')])
    def validate_image(form, field):
        if field.data:
            field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)
class EditPromForm(Form):
    promena = TextField(gettext('Promena'))
    hodnota = TextField(gettext('Hodnota'))