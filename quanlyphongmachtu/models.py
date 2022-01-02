from quanlyphongmachtu import db
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship, backref
from datetime import datetime, date
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UnitMedicine(BaseModel):
    name = Column(String(50), nullable=False)
    medicines = relationship('Medicine', backref='unitmedicine', lazy=True)

    def __str__(self):
        return self.name


class Medicine(BaseModel):
    name = Column(String(50), nullable=False)
    image = Column(String(255))
    active = Column(Boolean, default=True)
    price = Column(Float, default=0)
    usage = Column(String(255))
    created_date = Column(DateTime, default=datetime.now())
    unitmedicine_id = Column(Integer, ForeignKey(UnitMedicine.id), nullable=False)
    details = relationship('PhieuKhamBenhDetail', backref='medicine_detail', lazy=True)

    def __str__(self):
        return self.name


class TienKham(BaseModel):
    tien_kham = Column(Float, nullable=False)


class UserRole(BaseModel):
    __tablename__ = 'user_role'
    name_role = Column(String(20), nullable=False)
    note_role = Column(String(50))
    userinfos = relationship('UserInfo', backref='userinfo_role', lazy=True)

    def __str__(self):
        return self.name_role


class UserInfo(BaseModel, UserMixin):
    __tablename__ = 'userinfo'
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    avatar = Column(String(255))
    gender = Column(String(10), default='male')
    birthday = Column(Date, nullable=False)
    active = Column(Boolean, default=False)
    phones = relationship('PhoneNumber', backref='phonennumber', lazy='joined')
    account = relationship('Account', backref='userinfo_account', uselist=False, lazy=False)
    address_id = Column(Integer, ForeignKey('address_street.id'), nullable=False)
    user_role_id = Column(Integer, ForeignKey('user_role.id'), nullable=False)
    khambenhs = relationship('KhamBenh', backref='userinfo_khambenh', lazy=True)

    # bacsis = relationship('PhieuKhamBenh', backref='userinfobacsi_khambenh', lazy=True, )
    # benhnhans = relationship('PhieuKhamBenh', backref='userinfobenhnhan_khambenh', lazy=True)

    def __str__(self):
        return str.format("{} {}", self.first_name, self.last_name)


class PhoneNumber(BaseModel):
    number_phone = Column(String(50), nullable=False)
    phone_type = Column(String(20), default='def_phone')
    userinfo_id = Column(Integer, ForeignKey(UserInfo.id), nullable=False)


class AddressStreet(BaseModel):
    __tablename__ = 'address_street'
    city = Column(String(50))
    country = Column(String(50))
    address_street = Column(String(100), nullable=False)
    userinfos = relationship('UserInfo', backref='userinfo_address', lazy=True)

    def __str__(self):
        return str.format("{} Street, City {}, Country {}", self.address_street, self.city, self.country)


class Account(BaseModel):
    userinfo_id = Column(Integer, ForeignKey(UserInfo.id), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    created_date = Column(DateTime, default=datetime.now())


class QuyDinhKham(BaseModel):
    so_benhnhan_kham_trongngay = Column(Integer, nullable=False)
    khambenhs = relationship('KhamBenh', backref='quydinhkham_khambenh', lazy=True)


class KhamBenh(BaseModel):
    lich_khambenh = Column(Date, default=date.today())
    trangthai_khambenh = Column(Boolean, default=False)
    trangthai_hoantatthutuc = Column(Boolean, default=False)
    quydinhkham_id = Column(Integer, ForeignKey(QuyDinhKham.id), nullable=False)
    user_info_id = Column(Integer, ForeignKey(UserInfo.id), nullable=False)
    phieukhambenh = relationship('PhieuKhamBenh', backref='khambenh_phieukhambenh', uselist=False, lazy=False)


class PhieuKhamBenh(BaseModel):
    khambenh_id = Column(Integer, ForeignKey(KhamBenh.id), nullable=False, unique=True)
    bacsi_id = Column(Integer, ForeignKey(UserInfo.id), nullable=False)
    nguoikham_id = Column(Integer, ForeignKey(UserInfo.id), nullable=False)
    ngaytao_phieukham = Column(DateTime, default=datetime.now())
    trieuchung = Column(String(200))
    dudoan_loaibenh = Column(String(200))
    cachdung = Column(String(200))
    trangthaithanhtoan = Column(Boolean, default=False)
    tongtienthuoc = Column(Float, default=0)
    details = relationship('PhieuKhamBenhDetail', backref='phieukhambenh_detail', lazy=True)
    phieukhambenh_bacsi = relationship("UserInfo", foreign_keys=[bacsi_id], backref='userinfobacsi_khambenh', lazy=True)
    phieukhambenh_nguoikham = relationship("UserInfo", foreign_keys=[nguoikham_id], backref='userinfobenhnhan_khambenh',
                                           lazy=True)


class PhieuKhamBenhDetail(db.Model):
    phieukhambenh_id = Column(Integer, ForeignKey(PhieuKhamBenh.id), nullable=False, primary_key=True)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)





#     donvithuocs = relationship('DonViThuoc', secondary='thuoc_donvithuoc', lazy='subquery',
#                                backref=backref('thuocs', lazy=True))
#
#
# thuoc_donvithuoc = db.Table('thuoc_donvithuoc',
#                             Column('id_thuoc', Integer, ForeignKey('thuoc.id'), primary_key=True),
#                             Column('donvithuoc_id', Integer, ForeignKey('donvithuoc.id'), primary_key=True))


if __name__ == '__main__':
    db.create_all()
