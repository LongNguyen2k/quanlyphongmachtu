
from datetime import datetime
from datetime import date
from quanlyphongmachtu import app, db
from quanlyphongmachtu.models import UserInfo, Account, UserRole, AddressStreet, PhoneNumber, KhamBenh, QuyDinhKham
from sqlalchemy.sql import extract, func
import hashlib


def check_admin_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        account = Account.query.filter(Account.username.__eq__(username.strip()),
                                       Account.password.__eq__(password)).first()
        if account:
            user_info_id = account.userinfo_id
            return UserInfo.query.filter(UserInfo.id.__eq__(user_info_id)).first()


def check_user_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        account = Account.query.filter(Account.username.__eq__(username.strip()),
                                       Account.password.__eq__(password), ).first()
        if account:
            # lấy ra id user_info của account phía trên
            user_info_id = int(account.userinfo_id)

            # lấy ra đối tượng User_info từ id phía trên
            userinfo = UserInfo.query.filter(UserInfo.id.__eq__(user_info_id)).first()

            # lấy ra id_role của User_info trên
            id_user_role = userinfo.user_role_id

            # lấy ra user_role từ id_role phía trên
            userrole = UserRole.query.get(id_user_role)

            # kiểm tra user_role.name role có phải là bệnh nhân ko
            # if  userrole.name_role.__eq__("Bệnh Nhân"):
            return userinfo
    return None

    # không cần viết none


def check_username(username):
    user = Account.query.filter(Account.username.__eq__(username)).first()
    return user


def add_phone(phone_number, user_id):
    phone = PhoneNumber(number_phone=phone_number, userinfo_id=user_id)
    db.session.add(phone)
    db.session.commit()


def add_user(firstname, lastname, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    address_user = AddressStreet(address_street=kwargs.get('address'))
    db.session.add(address_user)
    db.session.commit()
    user_role = int(kwargs.get('user_role'))
    if user_role == 2:
        user_info = UserInfo(first_name=firstname.strip(),
                             last_name=lastname.strip(),
                             gender=kwargs.get('gender'),
                             avatar=kwargs.get('avatar'),
                             birthday=kwargs.get('birthday'),
                             active=True,
                             address_id=address_user.id,
                             user_role_id=user_role,
                             )
    else:
        if user_role == 3 or user_role == 4:
            user_info = UserInfo(first_name=firstname.strip(),
                                 last_name=lastname.strip(),
                                 gender=kwargs.get('gender'),
                                 avatar=kwargs.get('avatar'),
                                 birthday=kwargs.get('birthday'),
                                 address_id=address_user.id,
                                 user_role_id=user_role,
                                 )

    db.session.add(user_info)
    db.session.commit()
    user_account = Account(userinfo_id=user_info.id,
                           username=username.strip(),
                           password=password,
                           )
    db.session.add(user_account)
    db.session.commit()
    return user_info


def get_listuser():
    return UserInfo.query.all()


def get_user_by_id(user_id):
    return UserInfo.query.get(user_id)


def account_info(user_id):
    return Account.query.filter(Account.userinfo_id.__eq__(user_id)).first()


def phone_info(user_id):
    return PhoneNumber.query.filter(PhoneNumber.userinfo_id.__eq__(user_id))


def address_info(address_id):
    return AddressStreet.query.get(address_id)


def update_profile(user_info, user_id, phone_number, address_street, address_city, address_country):
    phone = phone_info(user_id)
    phone[0].number_phone = phone_number
    address = address_info(user_info.address_id)
    address.address_street = address_street
    address.city = address_city
    address.country = address_country
    db.session.commit()


def check_schedule(surgery_schedule):
    surgery_schedule = datetime.strptime(surgery_schedule, "%Y-%m-%d")
    # kiểm tra ngày đặt lịch khám có phải ngày hôm nay không
    if surgery_schedule.day == datetime.now().day \
            and surgery_schedule.month == datetime.now().month and \
            surgery_schedule.year == datetime.now().year:
        return True
    else:
        # kiểm tra ngày đặt lịch khám nhỏ hơn ngày hôm nay thì không hợp lệ còn lớn thì hợp lệ
        if surgery_schedule > datetime.now():
            return True
        else:
            return False


def dang_ky_kham_benh_nhan(lichkham, userinfo_id):
    kham_benh = KhamBenh(lich_khambenh=lichkham, user_info_id=userinfo_id, quydinhkham_id=app.config['QuyDinhKham'])
    db.session.add(kham_benh)
    db.session.commit()


def getlist_patient():
    list = UserInfo.query.filter(UserInfo.user_role_id.__eq__(int(app.config['PATIENT_ID'])))
    return list


def xemthongtin_khambenh(user_id):
    thongtin_khambenh = KhamBenh.query.filter(KhamBenh.user_info_id.__eq__(user_id))
    return thongtin_khambenh


def getlist_khambenh():
    current_date = datetime.now()
    # list_khambenh = KhamBenh.query.filter(KhamBenh.lich_khambenh.day.__eq__(current_date.day),
    #                                       KhamBenh.lich_khambenh.month.__eq__(current_date.month),
    #                                       KhamBenh.lich_khambenh.year.__eq__(current_date.year))
    # list_query = db.session.query(UserInfo, AddressStreet, KhamBenh.user_info_id == UserInfo.id,
    #                                  AddressStreet.id == UserInfo.address_id)\
    #                            .filter(extract('day', KhamBenh.lich_khambenh).__eq__(current_date.day),
    #                                    extract('month', KhamBenh.lich_khambenh).__eq__(current_date.month),
    #                                    extract('year', KhamBenh.lich_khambenh).__eq__(current_date.year),
    #                                    KhamBenh.trangthai_hoantatthutuc.__eq__(False))\
    #                            .add_columns(KhamBenh.id, UserInfo.first_name, UserInfo.last_name, UserInfo.gender,
    #                                         UserInfo.birthday, UserInfo.phones, AddressStreet.address_street,
    #                                         AddressStreet.city, AddressStreet.country).all()
    # list_query = db.session.query(KhamBenh.id, UserInfo.first_name, UserInfo.last_name, UserInfo.gender,
    #                               UserInfo.birthday, UserInfo.phones, AddressStreet.address_street,
    #                               AddressStreet.city, AddressStreet.country) \
    #     .join(KhamBenh, KhamBenh.user_info_id == UserInfo.id) \
    #     .join(UserInfo, UserInfo.address_id == AddressStreet.id) \
    #     .filter(extract('day', KhamBenh.lich_khambenh).__eq__(current_date.day),
    #             extract('month', KhamBenh.lich_khambenh).__eq__(current_date.month),
    #             extract('year', KhamBenh.lich_khambenh).__eq__(current_date.year),
    #             KhamBenh.trangthai_hoantatthutuc.__eq__(False)).all()
    # .join(UserInfo, UserInfo.id == KhamBenh.user_info_id, isouter=False) \
    #     .join(UserInfo, UserInfo.address_id == AddressStreet.id) \
    list_query = db.session.query(KhamBenh.id, UserInfo.first_name, UserInfo.last_name, UserInfo.gender,
                                   UserInfo.birthday, AddressStreet.address_street, AddressStreet.city, AddressStreet.country, PhoneNumber.number_phone)\
                            .select_from(UserInfo)\
                            .join(KhamBenh)\
                           .join(AddressStreet)\
                            .join(PhoneNumber)\
                            .filter(extract('day', KhamBenh.lich_khambenh).__eq__(current_date.day),
                                   extract('month', KhamBenh.lich_khambenh).__eq__(current_date.month),
                                   extract('year', KhamBenh.lich_khambenh).__eq__(current_date.year),
                                   KhamBenh.trangthai_hoantatthutuc.__eq__(False)).all()
    return list_query
