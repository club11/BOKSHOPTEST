from django.urls import path, include
from . import views as staff_views

app_name = 'staff'

urlpatterns = [
    path('excel_import/',  staff_views.ExcelStaffView.as_view(), name='excel_import'),  

]