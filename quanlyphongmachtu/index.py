from flask import render_template, request, redirect, url_for, flash
from quanlyphongmachtu import app, login
import os
import utils
from quanlyphongmachtu.admin import *
from flask_login import login_user, logout_user, current_user, login_required
import cloudinary.uploader
from datetime import date


@app.route("/")
def home():
    phones = None
    if current_user.is_authenticated:
        phones = utils.phone_info(current_user.id)
    return render_template("index.html", phones=phones)


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id)


@app.route('/admin-login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = utils.check_admin_login(username=username, password=password)
    if user:
        # ghi nhan trang thai dang nhap
        login_user(user=user)
    return redirect('/admin')


@app.route('/login', methods=['get', 'post'])
def user_signin():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            username = request.form['username']
            password = request.form['password']

            user = utils.check_user_login(username=username, password=password)
            if user:
                login_user(user=user)
                return redirect(url_for('home'))
            else:
                error_msg = "Username hoặc Password không chính xác"

        except Exception as ex:
            error_msg = str(ex)

    return render_template('login.html', error_msg=error_msg)


@app.route("/register", methods=['get', 'post'])
def register():
    error_msg = ''
    error_msg_user = ''
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        gender = request.form['gender']
        birthday = request.form['birthday']
        address = request.form['address_street']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        user = utils.check_username(username)
        user_role = request.form['user_role']
        phone = request.form['phone']
        if user:
            error_msg_user = 'Username đã có người sử dụng'
        else:
            if password.strip().__eq__(confirm_password.strip()):
                file = request.files.get('avatar')
                avatar = None
                if file:
                    res = cloudinary.uploader.upload(file)
                    avatar = res['secure_url']
                try:
                    new_user = utils.add_user(firstname=firstname, lastname=lastname,
                                   username=username, password=password,
                                   gender=gender,
                                   birthday=birthday,
                                   address=address,
                                   avatar=avatar,
                                   user_role=user_role)
                    utils.add_phone(phone, new_user.id)

                    return redirect(url_for("user_signin"))
                except Exception as ex:
                    error_msg = 'Đã có lỗi xảy ra' + str(ex)
            else:
                error_msg = "Mat khau khong khop!"

    return render_template('register.html', error_msg=error_msg, error_msg_user=error_msg_user)


@app.route('/logout')
def signout():
    logout_user()
    return redirect(url_for('user_signin'))


@app.route("/profile/<int:user_id>")
@login_required
def profile_page(user_id):
    user_info = utils.get_user_by_id(user_id)
    account = utils.account_info(user_id)
    phones = utils.phone_info(user_id)
    address = utils.address_info(user_info.address_id)
    return render_template('profile.html', account=account, phones=phones, address=address)


@app.route("/dangkykham/<int:user_id>", methods=['get', 'post'])
@login_required
def dang_ky_kham(user_id):
    error_msg = None
    user_info = utils.get_user_by_id(user_id)
    account = utils.account_info(user_id)
    phones = utils.phone_info(user_id)
    address = utils.address_info(user_info.address_id)
    if request.method == 'POST':
        surgery_schedule = request.form.get("lichkham")
        if utils.check_schedule(surgery_schedule):
            try:
                utils.dang_ky_kham_benh_nhan(surgery_schedule, userinfo_id=user_id)
                return redirect(url_for('xemthongtin_khambenh', user_id=user_id))
            except Exception as ex:
                error_msg = 'Đã có lỗi xảy ra' + str(ex)
        else:
            error_msg = "Đặt Lịch Khám Không Phù Hợp"
    return render_template('dangkykham.html',
                           error_msg=error_msg, account=account, phones=phones, address=address)


@app.route("/ytadangkykham/", methods=['get', 'post'])
@login_required
def dangkykham_yta():
    list_user = utils.getlist_patient()
    error_msg = None
    if request.method == 'POST':
        userinfo_id = request.form.get("benhnhan")
        surgery_schedule = request.form.get("lichkham")
        if utils.check_schedule(surgery_schedule):
            try:
                utils.dang_ky_kham_benh_nhan(surgery_schedule, userinfo_id=userinfo_id)
                return redirect(url_for('xemdanhsach_khambenh'))
            except Exception as ex:
                error_msg = "Đã có lỗi xảy ra trong quá trình thực hiện! Chi tiết lỗi: "+ str(ex)
        else:
            error_msg = "Đặt Lịch Khám Không Phù Hợp"
    return render_template('dangkykhamyta.html', list_user=list_user, error_msg=error_msg)


@app.route("/xemdanhsach", methods=['get'])
def xemdanhsach_khambenh():
    list_khambenh = utils.getlist_khambenh()
    ngaykham_homnay = date.today()
    return render_template("xemdanhsachkhambenh.html", list_khambenh=list_khambenh, ngaykham_homnay=ngaykham_homnay)


@app.route("/xemthongtinkham/<int:user_id>", methods=['get'])
@login_required
def xemthongtin_khambenh(user_id):
    thongtin_khambenh = utils.xemthongtin_khambenh(user_id=user_id)
    user_info = utils.get_user_by_id(user_id)
    phones = utils.phone_info(user_id)
    address = utils.address_info(user_info.address_id)
    return render_template("xemthongtinkhambenh.html",
                           user_info=user_info,
                           phones=phones,
                           address=address,
                           thongtin_khambenh=thongtin_khambenh)


@app.route("/add-phone", methods=['post'])
def add_phones():
    phone_number = request.form.get('phone')
    user_id = request.form.get('user_id')
    try:
        utils.add_phone(phone_number=phone_number, user_id=user_id)
        return redirect('/')
    except Exception as ex:
        error_msg = 'Đã có lỗi xảy ra' + str(ex)


@app.route("/profile/update/", methods=["post"])
@login_required
def update_profile():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user_info = utils.get_user_by_id(user_id)
        user_info.first_name = request.form.get("first_name")
        user_info.last_name = request.form.get("last_name")
        user_info.gender = request.form.get("gender")
        user_info.birthday = request.form.get("birthday")
        phone_number = request.form.get("phone")
        address_street = request.form.get("address_street")
        address_country = request.form.get("address_country")
        address_city = request.form.get("address_city")
        try:
            utils.update_profile(user_info=user_info,
                                 user_id=user_id,
                                 phone_number=phone_number,
                                 address_street=address_street,
                                 address_city=address_city,
                                 address_country=address_country)
            flash("Cập nhật thông tin bệnh nhân thành công")
            return redirect(url_for('profile_page', user_id=user_id))
        except Exception as ex:
            error_msg = 'Đã có lỗi xảy ra' + str(ex)


if __name__ == "__main__":
    app.run(debug=True)
