from django.conf.urls import url
#import settings
from . import views

#app_name = 'school_app'
urlpatterns = [
    url(r'^result', views.result, name='result'),
    
    url(r'^$', views.index, name='index'),
    url(r'^choice', views.helper_page1, name="helper_page1")
    #url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    #url(r'^media/(?P<path>.*)', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
];