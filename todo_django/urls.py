from django.conf.urls import patterns, include, url
from tastypie.api import Api
from todo_django.api_v1 import UserResource, TagResource, TaskResource
from django.contrib import admin
admin.autodiscover()

api_v1 = Api(api_name='v1')
api_v1.register(UserResource())
api_v1.register(TaskResource())
api_v1.register(TagResource())

urlpatterns = patterns('',
    url(r'^$', 'todo_django.views.home'),
    url(r'^api/', include(api_v1.urls)),
    url(r'login/',
        'django.contrib.auth.views.login',
        {'template_name': 'index.html'}
        ),
    url(r'logout/',
        'django.contrib.auth.views.logout',
        {'template_name': 'index.html'}
        ),
    url(r'^profile/tags/$',
        'todo_django.views.filter_by_tag'),
    url(r'^profile/tags/(?P<tag>.+)/$', 
        'todo_django.views.filter_by_tag'),
    url(r'^profile/add-task/$', 
        'todo_django.views.add_task'),
    url(r'^profile/get-task/(?P<task_id>\w+)/$',
        'todo_django.views.get_task'),
    url(r'^profile/delete-task/(?P<task_id>\w+)/$',
        'todo_django.views.delete_task'),
    url(r'^profile/$', 'todo_django.views.profile'),
    url(r'^admin/', include(admin.site.urls)),    
)

