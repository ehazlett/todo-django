from tastypie.resources import ModelResource
from tastypie.authorization import (DjangoAuthorization, Authorization)
from tastypie.authentication import (Authentication, ApiKeyAuthentication,
    SessionAuthentication, MultiAuthentication)
from tastypie import fields
from django.core.urlresolvers import reverse
from django.conf.urls.defaults import *
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_user
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import Q
from todo_django.models import Task
from taggit.models import Tag
from tastypie.constants import ALL, ALL_WITH_RELATIONS
import simplejson as json
import os

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        excludes = ('id', 'password', 'is_staff', 'is_superuser')
        list_allowed_methods = ['get']
        authentication = MultiAuthentication(
            SessionAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        resource_name = 'users'

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<username>[\w\d_.-]+)/$" % \
                self._meta.resource_name, self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail"),
        ]

    def get_object_list(self, request):
        return super(UserResource, self).get_object_list(request).filter(
            username=request.user.username)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(username=request.user.username)

    def dehydrate(self, bundle):
        # add api_key
        bundle.data['api_key'] = bundle.obj.api_key.key
        return bundle

class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()

class TaskResource(ModelResource):
    tags = fields.ToManyField(TagResource, 'tags', full=True)

    class Meta:
        queryset = Task.objects.all()
        excludes = ('id', )
        authentication = MultiAuthentication(
            SessionAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        resource_name = 'tasks'
        filtering = {
            "title": ALL,
            "tags": ALL,
        }

    def get_object_list(self, request):
        return super(TaskResource, self).get_object_list(request).filter(
            user=request.user)
