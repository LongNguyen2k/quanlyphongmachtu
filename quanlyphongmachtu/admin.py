from quanlyphongmachtu import admin, db, app
from quanlyphongmachtu.models import Medicine, UnitMedicine, TienKham, QuyDinhKham, UserInfo, Account, UserRole, PhoneNumber, AddressStreet
from flask_admin.contrib.sqla import ModelView
from flask_admin import  BaseView, expose
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


class UnitMedicineView(ModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    column_searchable_list = ['name']
    column_labels = {
        'name':'Tên Đơn Vị'
    }


class TienKhamView(ModelView):
    column_labels = {
        'tien_kham':'Tiền Khám'
    }


class QuyDinhKhamView(ModelView):
    column_labels = {
        'so_benhnhan_kham_trongngay':'Quy Định Số Bệnh Nhân Đăng Ký Khám Trong Ngày'
    }


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


admin.add_view(AuthenticatedUserModelView(UnitMedicine, db.session, name='Đơn Vị Thuốc'))
admin.add_view(MedicineView(Medicine, db.session, 'Thuốc'))
admin.add_view(AuthenticatedUserModelView(TienKham, db.session, 'Tiền Khám'))
admin.add_view(AuthenticatedUserModelView(QuyDinhKham, db.session, 'Quy Định Khám'))
# admin.add_view(AuthenticatedUserModelView(UserInfo, db.session))
# admin.add_view(AuthenticatedUserModelView(Account, db.session))
# admin.add_view(AuthenticatedUserModelView(UserRole, db.session))
# admin.add_view(AuthenticatedUserModelView(PhoneNumber, db.session))
# admin.add_view(AuthenticatedUserModelView(AddressStreet, db.session))
admin.add_view(LogOutView(name='Đăng Xuất'))
admin.add_view(StatsView(name='Thống Kê Báo Cáo'))