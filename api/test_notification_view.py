import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate
from .models import Profile, create_user, QuestionPost, InformationPost, User
from .models import Notification


def login(client):
    data = {
        'username': 'testuser',
        'password': 'userpassword'
    }

    path = reverse('sign_in')
    client.post(path=path,
                data=json.dumps(data),
                content_type='application/json')


def create_information(title, content, username='testuser', hidden_exist=True, hidden_content='thisishidden',
                       due='2019-03-03T04:02:32.142923Z', hidden_content_cost=100, sponsor_credit=200):
    client = Client()
    login(client)

    data = {
        'title': title,
        'content': content,
        'username': username,
        'hidden_exist': hidden_exist,
        'hidden_content': hidden_content,
        'due': due,
        'hidden_content_cost': hidden_content_cost,
        'sponsor_credit': sponsor_credit,
        'tags': ['tag4', 'tag6', 'tag3']
    }

    path = reverse('information_posts')
    response = client.post(path=path,
                           data=json.dumps(data),
                           content_type='application/json')
    return response


def create_question(title, content, username='testuser', due='2019-03-03T04:02:32.142923Z',
                    bounty=100, question_type='private'):
    client = Client()
    login(client)
    data = {
        'title': title,
        'content': content,
        'username': username,
        'due': due,
        'bounty': bounty,
        'question_type': question_type,
        'tags': ['tag1', 'tag2', 'tag3']
    }
    path = reverse('question_posts')
    response = client.post(path=path,
                           data=json.dumps(data),
                           content_type='application/json')
    return response


def create_answer(qid, content, username='testuser'):
    client = Client()
    login(client)

    data = {
        'qid': qid,
        'content': content,
        'username': username,
    }
    path = reverse('question_answers')
    response = client.post(path=path,
                           data=json.dumps(data),
                           content_type='application/json')
    return response


class NotificationTests(TestCase):

    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com',
                    verified=True)

        # make question and information
        response1 = create_information(title='testinformation1', content='testcontent1')
        response2 = create_question(title='testquestion1', content='testcontent1')
        iid = response1.data['data']['id']
        qid = response2.data['data']['id']

        client = Client()
        login(client)
        # make answer
        response3 = create_answer(qid, 'testanswer')
        aid = response3.data['data']['id']

        # select answer
        data = {
            'qid': qid,
            'aid': aid,
            'username': 'testuser'
        }
        path = reverse('question_posts')
        client.put(path=path,
                   data=json.dumps(data),
                   content_type='application/json')

        # buy information
        path = reverse('information_post_by_id', kwargs={'id': iid})
        client.put(path=path)

    def test_get_notifications(self):
        client = Client()
        login(client)

        path = reverse('notifications')
        response = client.get(path=path)
        self.assertEqual(response.status_code, 200)

    def test_get_newsfeed(self):
        client = Client()
        login(client)
        path = reverse('newsfeed')
        response = client.get(path=path)
        self.assertEqual(response.status_code, 200)

    def test_read_newsfeed(self):
        client = Client()
        login(client)

        every_notification = Notification.objects.filter(read=False)
        nid = 0
        for notification in every_notification:
            nid = notification.id

        path = reverse('newsfeed')
        data = {'nid': nid}
        response = client.put(path=path,
                              data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)


class WatchTagTests(TestCase):

    def setUp(self):
        create_user(username='testuser',
                    password='userpassword',
                    email='test@test.com',
                    verified=True)

    def test_watch_tags(self):
        client = Client()
        login(client)

        # setup watch tags
        data = {
            'tags': ['tag1', 'tag2', 'tag3']
        }
        path = reverse('watch_tags')
        response = client.post(path=path,
                               data=json.dumps(data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # make question and information
        create_information(title='testinformation1', content='testcontent1')
        create_question(title='testquestion1', content='testcontent1')

        # check created notifications
        path = reverse('notifications')
        response = client.get(path=path)
        self.assertEqual(response.status_code, 200)
