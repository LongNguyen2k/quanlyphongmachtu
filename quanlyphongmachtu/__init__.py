from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_babelex import Babel
from flask_login import LoginManager
import cloudinary


app = Flask(__name__)
app.secret_key = '%SF%$#SD#E#SDSDJHSJKHK#$*&*&#*&#&*#&#&**&'
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:17102000@localhost:3308/quanlyphongmachtu?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['PAGE_SIZE'] = 4
app.config['ADMIN_ID'] = 1
app.config['PATIENT_ID'] = 2
app.config['QuyDinhKham'] = 1
db = SQLAlchemy(app)

admin = Admin(app, name='QUẢN LÝ PHÒNG MẠCH TƯ', template_mode='bootstrap4')
babel = Babel(app)
login = LoginManager(app)

cloudinary.config(cloud_name='decmhyieh', api_key='413756871999116',
                  api_secret='G34UwtLLRY2hg_PCrmzs5pT9RTo')

app.config['Twillio_account_sid'] = 'ACb95b4679048107af5a60eebb42811191'
app.config['Twillio_auth_token'] = '74cb3b4f0add848815461589b68b0e81'
app.config['DefaultTwillioPhone'] = "+13305258335"


@babel.localeselector
def get_locale():
        return 'vi'
