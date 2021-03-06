import math

from flask import render_template, request, redirect, url_for, flash, session, jsonify
from quanlyphongmachtu import app, login
import os
import utils
from quanlyphongmachtu.admin import *
from flask_login import login_user, logout_user, current_user, login_required
import cloudinary.uploader
from datetime import date


@app.context_processor
def common_response():
    return {
        'unit_medicines': utils.load_unitmedicines(),
        'prescription_stats': utils.count_prescription(session.get('prescription'))
    }


@app.route("/medicines-list")
@login_required
def list_medicines():
    unitmedicine_id = request.args.get("unitmedicine_id")
    kw = request.args.get("keyword")
    page = int(request.args.get('page', 1))
    counter = utils.count_medicine()
    medicines = utils.load_medicines(unitmedicine_id, keyword=kw, page=page)

    return render_template("medicines.html", medicines=medicines, pages=math.ceil(counter / app.config['PageSize']))


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
                next = request.args.get('next', 'home')
                return redirect(url_for(next))
            else:
                error_msg = "Username ho???c Password kh??ng ch??nh x??c"

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
            error_msg_user = 'Username ???? c?? ng?????i s??? d???ng'
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
                    error_msg = '???? c?? l???i x???y ra' + str(ex)
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
            if utils.check_quydinh(surgery_schedule).__eq__(True):
                try:
                    utils.dang_ky_kham_benh_nhan(surgery_schedule, userinfo_id=user_id)
                    return redirect(url_for('xemthongtin_khambenh', user_id=user_id))
                except Exception as ex:
                    error_msg = '???? c?? l???i x???y ra' + str(ex)
            else:
                error_msg = "S??? b???nh nh??n ???? ?????t m???c t???i ??a xin vui l??ng ????ng k?? kh??m v??o ng??y kh??c!"
        else:
            error_msg = "?????t L???ch Kh??m Kh??ng Ph?? H???p"
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
            if utils.check_quydinh(surgery_schedule).__eq__(True):
                try:
                    utils.dang_ky_kham_benh_nhan(surgery_schedule, userinfo_id=userinfo_id)
                    return redirect(url_for('xemdanhsach_khambenh'))
                except Exception as ex:
                    error_msg = "???? c?? l???i x???y ra trong qu?? tr??nh th???c hi???n! Chi ti???t l???i: " + str(ex)
            else:
                error_msg = "S??? b???nh nh??n ???? ?????t m???c t???i ??a xin vui l??ng ????ng k?? kh??m v??o ng??y kh??c!"
        else:
            error_msg = "?????t L???ch Kh??m Kh??ng Ph?? H???p"

    return render_template('dangkykhamyta.html', list_user=list_user, error_msg=error_msg)


@app.route("/xemdanhsach", methods=['get', 'post'])
@login_required
def xemdanhsach_khambenh():
    error_msg = None
    list_khambenh = utils.getlist_khambenh()
    ngaykham_homnay = date.today()
    if request.method == 'POST':
        try:
            utils.util_hoantat_danhsachkham()
            message_success = "Ho??n T???t Danh S??ch Kh??m B???nh!"
            return render_template("xemdanhsachkhambenh.html", ngaykham_homnay=date.today(),
                                   message_success=message_success)
        except Exception as ex:
            error_msg = "???? c?? l???i trong qu?? tr??nh ho??n t???t danh s??ch kh??m!\n" \
                        "Chi ti???t l???i: " + str(ex)
    return render_template("xemdanhsachkhambenh.html", khambenh=list_khambenh, error_msg=error_msg,
                           ngaykham_homnay=ngaykham_homnay)


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


@app.route("/xemdanhsachkhambenh_bacsi", methods=['get', 'post'])
@login_required
def xemdanhsach_khambenh_bacsi():
    dateInput = request.args.get("dateInput")
    ngaykham_homnay = date.today()
    listkhambenh = utils.getlist_khambenhbacsi(dateInput=dateInput)
    return render_template("xemdanhsachkhambenhbacsi.html", khambenh=listkhambenh, dateInput=dateInput,
                           ngaykham_homnay=ngaykham_homnay)


@app.route("/add-phone", methods=['post'])
def add_phones():
    phone_number = request.form.get('phone')
    user_id = request.form.get('user_id')
    try:
        utils.add_phone(phone_number=phone_number, user_id=user_id)
        return redirect('/')
    except Exception as ex:
        error_msg = '???? c?? l???i x???y ra' + str(ex)


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
            flash("C???p nh???t th??ng tin b???nh nh??n th??nh c??ng")
            return redirect(url_for('profile_page', user_id=user_id))
        except Exception as ex:
            error_msg = '???? c?? l???i x???y ra' + str(ex)


@app.route("/bacsi/lapphieukham/<int:khambenh_id>", methods=['get'])
def lapphieukham(khambenh_id):
    thongtinbenhnhan = utils.get_khambenhinfo_byid(khambenh_id)
    userinfo = utils.get_user_by_id(thongtinbenhnhan.user_info_id)
    return render_template("/bacsi/lapphieukham.html", thongtinbenhnhan=thongtinbenhnhan, userinfo=userinfo,
                           stats=utils.count_prescription(session.get('prescription')))


@app.route('/api/add-to-prescription', methods=['post'])
@login_required
def api_add_to_prescription():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    unitmedicine_name = data.get('unitmedicine_name')
    usage = data.get('usage')
    unitprice = data.get('unitprice')

    prescription = session.get('prescription')
    # ch??a c?? gi??? th?? t???o gi??? thu???c m???i trong session
    if not prescription:
        prescription = {}
    # thu???c ???? c?? trong gi??? th?? t??ng s??? l?????ng
    if id in prescription:
        prescription[id]['quantity'] = prescription[id]['quantity'] + 1
    else:
        # ch??a c?? th?? t???o ra m???t ?????i t?????ng m???i b??? v??o gi???
        prescription[id] = {
            'id': id,
            'name': name,
            'unitmedicine_name': unitmedicine_name,
            'usage': usage,
            'unitprice': unitprice,
            'quantity': 1
        }

    session['prescription'] = prescription

    return jsonify(utils.count_prescription(prescription))


@app.route('/api/update-to-prescription', methods=['put'])
def update_to_prescription():
    data = request.json
    id = str(data.get("id"))
    quantity = data.get('quantity')
    prescription = session.get('prescription')

    if prescription:
        if id in prescription:
            prescription[id]['quantity'] = quantity
            session['prescription'] = prescription

    return jsonify(utils.count_prescription(prescription))


@app.route('/api/delete-to-prescription/<medicine_id>', methods=['delete'])
def delete_to_prescription(medicine_id):
    prescription = session.get('prescription')
    if prescription:
        if medicine_id in prescription:
            del prescription[medicine_id]
            session['prescription'] = prescription

    return jsonify(utils.count_prescription(prescription))


@app.route('/api/add-prescription', methods=['post'])
@login_required
def add_prescription():
    data = request.json
    trieuchung = data.get('trieuchung')
    dudoanbenh = data.get('dudoanbenh')
    user_dangkykham = data.get('user_dangkykham')
    phieukhambenh = data.get('phieukhambenh')
    cachdungthuoc = data.get('cachdungthuoc')
    total_amount = data.get('total_amount')
    try:
        utils.add_prescription(prescription=session.get('prescription'),
                               phieukhambenh=phieukhambenh,
                               user_dangkykham=user_dangkykham,
                               trieuchung=trieuchung,
                               dudoanbenh=dudoanbenh,
                               cachdungthuoc=cachdungthuoc,
                               total_amount=total_amount)
        utils.complete_prescription(int(phieukhambenh))
        del session['prescription']
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})


@app.route("/bacsi/thanhtoan/<khambenh_id>", methods=['get'])
@login_required
def thanhtoan_hoadon(khambenh_id):
    thongtinphieukham = utils.get_infophieukham(id_phieukham=int(khambenh_id))
    info_benhnhan = utils.get_user_by_id(thongtinphieukham.nguoikham_id)
    tienkham = utils.get_infotienkham()
    tongtienhoadon = utils.tongtienhoadon(tienkham.tien_kham, thongtinphieukham.tongtienthuoc)
    return render_template("bacsi/thanhtoanhoadon.html",
                           thongtinphieukham=thongtinphieukham,
                           info_benhnhan=info_benhnhan,
                           tienkham=tienkham,
                           tongtienhoadon=tongtienhoadon)


@app.route('/api/pay_receipt_patient', methods=["post"])
@login_required
def pay_receipt():
    data = request.json
    id_phieukham = data.get("id_phieukham")
    id_tienkham = data.get("id_tienkham")
    tongtien_hoadon = data.get("tongtien_hoadon")
    try:
        utils.thanhtoanhoadon(idphieukham=id_phieukham, idtienkham=id_tienkham, tongtienhoadon=tongtien_hoadon)
        utils.hoantatthanhtoan(id_phieukham=id_phieukham)
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})


if __name__ == "__main__":
    app.run(debug=True)
