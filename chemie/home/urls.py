from django.conf.urls import url
from .views import index, contact, calendar, request_funds, edit_flatpage, request_office, OfficeAccessApplicationListView

urlpatterns = [
    url(r'^$', index, name="home"),
    url(r'^kontakt/', contact, name="kontakt"),
    url(r'^kalender/', calendar, name="calendar"),
    url(r'^funds/', request_funds, name="fundsapplication"),
    url(r'^kontortilgang/apply', request_office, name='officeaccess'),
    url(r'^flatpage/(?P<url>.*)$', edit_flatpage, name='edit_flatpage'),
    url(r'^kontortilgang/applicants',
        OfficeAccessApplicationListView.as_view(),
        name='office_access_list'),
]