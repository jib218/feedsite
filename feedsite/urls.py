from django.urls import path

from . import views

app_name = 'feedsite'
urlpatterns = [
    path('', views.UnreadView.as_view(), name = 'unread'),
    path('markread/<int:item_id>/', views.markread, name = "markread"),
    path('markreadlist/<int:first>/<int:next>/', views.markreadlist, name = "markreadlist"),
    path('markreadrest/<int:first>/', views.markreadrest, name = 'markreadrest'),
    path('markunread/<int:item_id>/', views.markunread, name = "markunread"),
    path('history/', views.HistoryView.as_view(), name = 'history'),
    path('feeds/', views.FeedsView.as_view(), name = "feeds"),
    path('feeds/create/', views.FeedCreateView.as_view(), name='feed-create'),
    path('feeds/<int:pk>/', views.FeedUpdateView.as_view(), name='feed-update'),
    path('feeds/<int:pk>/delete', views.FeedDeleteView.as_view(), name='feed-delete'),
    path('settings/', views.SettingsView.as_view(), name = 'settings')   
]