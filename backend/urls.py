"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
# from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    url(r'^api/', include('api.urls'))
]

if settings.DEBUG:
    schema_view = get_schema_view(
        openapi.Info(
            title='SNUwagon API',
            default_version='v1',
        ),
    )
    urlpatterns.append(url(r'^swagger(?P<format>\.json|\.yaml)$',
                           schema_view.without_ui(cache_timeout=None), name='schema-json'))
    urlpatterns.append(url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=None),
                           name='schema-swagger-ui'))
    urlpatterns.append(url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=None),
                           name='schema-redoc'))

    # schema_view = get_swagger_view(title='SNUwagon API')
    # urlpatterns.append(
    #     url(r'^swagger$', schema_view)
    # )
    urlpatterns.append(
        path('admin/', admin.site.urls)
    )
