from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('good/<int:good_id>', views.good, name='good'),
    path('delelte/<int:del_id>', views.delete, name='delete'),
    path('share/<int:share_id>', views.share, name='share'),
    path('user/<username>', views.user, name='user'),
    path('follow/<follow_user>', views.follow, name='follow'),
    path('follower/<follow_user>', views.follower, name='follower'),
    path('following/<owner>', views.following, name='following'),
    path('following_content', views.following_content, name='following_content'),
    path('notification', views.show_notification, name='notification'),
    path('tsubuyaki', auth_views.LogoutView.as_view(), name='logout'),
    path('signup', views.signup, name='signup'),
]