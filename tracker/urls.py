from django.urls import path
from django.shortcuts import render
from .views import register_user,expense_list_create, expense_update_delete,income_list_create,income_update_delete,download_expenses,download_income,welcome,register_page,login_page,dashboard,expenses_page,income_page,download_page

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    #Register endpoint
    path('api/register/', register_user, name='register'),


    # Login endpoint (JWT)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Refresh token endpoint (optional)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

# Expenses APIs
    path('api/expenses/', expense_list_create, name='expense-list-create'),
    path('api/expenses/<int:pk>/', expense_update_delete, name='expense-update-delete'),
    path('api/download-expenses/', download_expenses, name='download-expenses'),

#Income APIS
    path('api/income/', income_list_create, name='income-list-create'),
    path('api/income/<int:pk>/', income_update_delete, name='income-update-delete'),
    path('api/download-income/',download_income, name='download-income'),
#frontend
    path('', welcome, name='welcome'),
    path('register-page/', register_page, name='register-page'),
    path('login-page/', login_page, name='login-page'),
    path('dashboard-page/', dashboard, name='dashboard-page'),
    path('expenses-page/', expenses_page,name='expense-page'),
    path('income-page/', income_page, name='income-page'),
    path('download-page/', download_page, name='download-page'),

]




"""#frontend
    path('',welcome, name='welcome'),
    path('register/', register_page, name='register'),
    path('login/',login_page, name='login'),
    path('dashboard/',dashboard, name='dashboard'),
    path('expenses/',expenses_page, name='expenses'),
    path('income/',income_page, name='income'),
    path('download/',download_page, name='download'),
"""