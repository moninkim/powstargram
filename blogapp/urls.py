from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('explore/', views.explore, name='explore'),
    path('new/', views.new_post, name = 'new_post'),
    path('<int:post_id>/update', views.edit_post, name='edit'),
    path('<int:post_id>/delete', views.delete, name='delete'),
    path('like/', views.post_like, name='post_like'),
    path('<int:post_id>/comment/create/', views.comment_create, name='comment_create'),
    path('<int:post_id>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete')
] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)