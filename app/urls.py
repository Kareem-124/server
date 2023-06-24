from django.urls import path     
from . import views

app_name = 'app'
urlpatterns = [
    # Page Section:
    path('', views.index),
    path('home',views.success, name = 'home'),
    path('table',views.table, name = 'table'),
    path('form',views.form, name = 'form'),
    path('team/new',views.new_team, name = 'new_team'),
    path('team/<int:id>',views.team_details, name = 'team_details'),
    path('team/<int:team_id>/edit',views.team_edit, name = 'team_edit'),

    # Process Section
    path('reg_process', views.reg_process, name='reg_process'),   # Registration Process                                    
    path('login_process', views.login_process, name='login_process'),   # Login Process                                    
    path('success_redirect_process', views.success_redirect_process, name='success_redirect_process'),   # Login Process                                    
    path('logout_process', views.logout_process, name='logout_process'),   # Login Process                                    
    path('create_new_team_process', views.create_new_team_process, name='create_new_team_process'),   # Create New Team Process                                    
    path('new_team_redirect_process', views.new_team_redirect_process, name='new_team_redirect_process'),   # Login Process                                    
    path('edit_new_team_process/<int:team_id>', views.edit_new_team_process, name='edit_new_team_process'),   # Login Process  
    path('delete_team/<int:team_id>/', views.delete_team, name='delete_team'),                                   
    path('add_player/<int:team_id>/', views.add_player_process, name='add_player_process'),                                   

]