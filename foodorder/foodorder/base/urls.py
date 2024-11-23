from django.urls import path
from .views import (
    food_list,
    create_order,
    order_summary,
    admin_dashboard,
    order_details,
    update_order_status,
    delete_order,
    food_management,
    add_food_item,
    update_food_item,
    delete_food_item,
    register,
    login_view,
    logout_view,
)

urlpatterns = [
    path('', food_list, name='food_list'),
    path('order/create/', create_order, name='create_order'),
    path('order/<int:order_id>/', order_summary, name='order_summary'),

    # Admin Dashboard and Management
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/order/<int:order_id>/', order_details, name='order_details'),
    path('admin/order/<int:order_id>/update/', update_order_status, name='update_order_status'),
    path('admin/order/<int:order_id>/delete/', delete_order, name='delete_order'),

    # Food Management
    path('admin/food/', food_management, name='food_management'),
    path('admin/food/add/', add_food_item, name='add_food_item'),
    path('admin/food/<int:food_id>/edit/', update_food_item, name='update_food_item'),
    path('admin/food/<int:food_id>/delete/', delete_food_item, name='delete_food_item'),

    # Authentication
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
