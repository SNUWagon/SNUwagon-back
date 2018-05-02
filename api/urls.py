from django.urls import path
from django.conf.urls import url, include
from api.views import auth_views, list_views, posts_views, vote_views

urlpatterns = [
    url(r'^auth/signin$', auth_views.signin),
    url(r'^auth/signup$', auth_views.signup),
    url(r'^auth/userinfo/(?P<id>[0-9]+)$', auth_views.userinfo),
    url(r'posts/index$', posts_views.index),
    url(r'posts/question$', posts_views.question),
    url(r'posts/question/(?P<id>[0-9]+)$', posts_views.question),
    url(r'posts/information$', posts_views.information),
    url(r'posts/information/(?P<id>[0-9]+)$', posts_views.information),
    url(r'list/questions$', list_views.questions),
    url(r'list/questions/tag/(?P<tag>[0-9]+)$', list_views.questions_with_tag),
    url(r'list/questions/type/(?P<type>[0-9]+)$', list_views.questions_with_type),
    url(r'list/questions/title/(?P<title>[0-9]+)$', list_views.questions_with_title),
    url(r'list/informations$', list_views.informations),
    url(r'list/informations/tag/(?P<tag>[0-9]+)$', list_views.informations_with_tag),
    url(r'list/informations/type/(?P<type>[0-9]+)$', list_views.informations_with_type),
    url(r'list/informations/title/(?P<title>[0-9]+)$', list_views.informations_with_title),
    url(r'list/all$', list_views.all),
    url(r'list/all/tag/(?P<tag>[0-9]+)$', list_views.all_with_tag),
    url(r'list/all/type/(?P<type>[0-9]+)$', list_views.all_with_type),
    url(r'list/all/title/(?P<title>[0-9]+)$', list_views.all_with_title),
    url(r'vote$', vote_views.vote),
    url(r'vote/(?P<id>[0-9]+)$', vote_views.vote),
]
