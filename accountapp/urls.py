from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('logout/', views.logout, name="logout"),
    path('people/<str:username>/', views.people, name="people"),
    path('profile_update/',views.profile_update, name="profile_update"),
    path('<int:user_id>/follow/', views.follow, name="follow")
]