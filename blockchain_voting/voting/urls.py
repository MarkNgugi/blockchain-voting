from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("vote/<int:candidate_id>/", views.vote, name="vote"),
    path("admin-panel/", views.admin_dashboard, name="admin_dashboard"), # Admin Panel (protected)
    path("add/add-candidate/", views.add_candidate, name="add_candidate"),
    path("set-timeframe/", views.set_voting_timeframe, name="set_voting_timeframe"),

      
    path("register/", views.student_register, name="student_register"), 
    path("login/", views.student_login, name="student_login"),  
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
if settings.DEBUG:  # Serve media files during development only
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  