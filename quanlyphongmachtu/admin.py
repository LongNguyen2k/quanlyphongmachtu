from quanlyphongmachtu import admin, db, app
from quanlyphongmachtu.models import Medicine, UnitMedicine, TienKham, QuyDinhKham, UserInfo, Account, UserRole, \
    PhoneNumber, AddressStreet
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect


class AuthenticatedUserModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role_id == app.config['ADMIN_ID']


class MedicineView(AuthenticatedUserModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    column_exclude_list = _list = ('image')
    column_filters = ['usage', 'price']
    column_searchable_list = ['name']
    column_labels = {
        'name': 'Tên Thuốc',
        'active': 'Trạng Thái Kinh Doanh',
        'price': 'Giá Tiền',
        'usage': 'Cách Dùng',
        'created_date': 'Ngày Tạo',
        'unitmedicine': 'Đơn Vị Thuốc',
        'image': 'Ảnh minh họa'
    }
    form_excluded_columns = ['active', 'image']


class UnitMedicineView(AuthenticatedUserModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    column_searchable_list = ['name']
    column_labels = {
        'name': 'Tên Đơn Vị'
    }
    form_excluded_columns = ['medicines']


# quản trị viên có thể kiểm duyệt tài khoản bác sĩ, y tá
class UserInfoView(AuthenticatedUserModelView):
    can_view_details = True
    edit_modal = True
    details_modal = True
    can_edit = True
    can_create = False
    can_delete = False
    column_exclude_list = ['birthday', 'avatar', 'gender', 'userinfo_address']
    form_excluded_columns = ['first_name',
                             'last_name',
                             'birthday',
                             'avatar',
                             'gender',
                             'userinfo_role',
                             'userinfo_address', 'account', 'khambenhs', 'phones']


class TienKhamView(AuthenticatedUserModelView):
    can_create = False
    can_edit = True
    can_delete = False
    column_labels = {
        'tien_kham': 'Tiền Khám'
    }


class QuyDinhKhamView(AuthenticatedUserModelView):
    can_create = False
    can_edit = True
    can_delete = False
    column_labels = {
        'so_benhnhan_kham_trongngay': 'Quy Định Số Bệnh Nhân Đăng Ký Khám Trong Ngày'
    }
    form_excluded_columns = ['khambenhs']


class CheckLogIndUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class CheckUserAuthenticatedAdmin(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role_id == app.config['ADMIN_ID']


class LogOutView(CheckLogIndUser):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class StatsView(CheckUserAuthenticatedAdmin):
    @expose('/')
    def index(self):
        return self.render('/admin/stats.html')


admin.add_view(MedicineView(Medicine, db.session, 'Thuốc'))
admin.add_view(UnitMedicineView(UnitMedicine, db.session, name="Đơn vị thuốc"))
admin.add_view(TienKhamView(TienKham, db.session, name="Tiền Khám Bệnh Nhân"))
admin.add_view(QuyDinhKhamView(QuyDinhKham, db.session, name="Quy Định Khám"))
admin.add_view(UserInfoView(UserInfo, db.session, "Thông tin tài khoản"))
# admin.add_view(AuthenticatedUserModelView(TienKham, db.session, 'Tiền Khám'))
# admin.add_view(AuthenticatedUserModelView(QuyDinhKham, db.session, 'Quy Định Khám'))
# admin.add_view(AuthenticatedUserModelView(UnitMedicine, db.session, name='Đơn Vị Thuốc'))
# admin.add_view(AuthenticatedUserModelView(Account, db.session))
# admin.add_view(AuthenticatedUserModelView(UserRole, db.session))
# admin.add_view(AuthenticatedUserModelView(PhoneNumber, db.session))
# admin.add_view(AuthenticatedUserModelView(AddressStreet, db.session))
admin.add_view(LogOutView(name='Đăng Xuất'))
admin.add_view(StatsView(name='Thống Kê Báo Cáo'))
