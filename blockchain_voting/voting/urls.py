from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("vote/<int:candidate_id>/", views.vote, name="vote"),
    path("panel/", views.admin_dashboard, name="admin_dashboard"),
    path("add/add-candidate/", views.add_candidate, name="add_candidate"),
    path("set-timeframe/", views.set_voting_timeframe, name="set_voting_timeframe"),
]
if settings.DEBUG:  # Serve media files during development only
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 