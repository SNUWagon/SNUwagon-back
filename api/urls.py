from django.urls import path
from django.conf.urls import url, include
from api.views import auth_views, list_views, question_views, information_views, vote_views

urlpatterns = [
    url(r'^auth/signin$', auth_views.signin, name='sign_in'),
    url(r'^auth/signup$', auth_views.signup, name='sign_up'),
    url(r'^auth/signout$', auth_views.signout, name='sign_out'),
    url(r'^auth/verification/(?P<hashstring>[\s\S]+)$', auth_views.verification, name='verification'),
    url(r'^auth/userinfo$', auth_views.userinfo, name='my_info'),
    url(r'^auth/userinfo/(?P<id>[0-9]+)$', auth_views.userinfo, name='user_info'),

    url(r'posts/question$', question_views.question, name='question_posts'),
    url(r'posts/question/(?P<id>[0-9]+)$', question_views.question, name='question_post_by_id'),
    url(r'posts/answer$', question_views.answer, name='question_answers'),
    url(r'posts/answer/(?P<id>[0-9]+)$', question_views.answer, name='question_answers_by_id'),
    url(r'posts/information$', information_views.information, name='information_posts'),
    url(r'posts/information/(?P<id>[0-9]+)$', information_views.information, name='information_post_by_id'),

    url(r'list/questions$', list_views.questions, name='question_list'),
    url(r'list/questions/tag/(?P<tag>[\s\S]+)$', list_views.questions_with_tag, name='question_list_by_tag'),
    url(r'list/questions/type/(?P<type>[0-9]+)$', list_views.questions_with_type, name='question_list_by_type'),
    url(r'list/questions/title/(?P<title>[\s\S]+)$', list_views.questions_with_title, name='question_list_by_title'),
    url(r'list/informations$', list_views.informations, name='information_list'),
    url(r'list/informations/tag/(?P<tag>[\s\S]+)$', list_views.informations_with_tag, name='information_list_by_tag'),
    url(r'list/informations/type/(?P<type>[0-9]+)$', list_views.informations_with_type,
        name='information_list_by_type'),
    url(r'list/informations/title/(?P<title>[\s\S]+)$', list_views.informations_with_title,
        name='information_list_by_title'),
    url(r'list/tags$', list_views.tags, name='tag_list'),
    url(r'vote$', vote_views.vote, name='vote'),
    url(r'vote/(?P<id>[0-9]+)$', vote_views.vote, name='vote_by_id'),
]
