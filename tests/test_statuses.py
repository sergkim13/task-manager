from http import HTTPStatus

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.constants import REVERSE_LOGIN
from task_manager.statuses.constants import (
    DELETE_STATUS,
    REVERSE_CREATE,
    REVERSE_STATUSES,
    STATUS_USED_IN_TASK,
    TEMPLATE_CREATE,
    TEMPLATE_DELETE,
    TEMPLATE_LIST,
    TEMPLATE_UPDATE,
    UPDATE_STATUS,
)
from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.utils import disable_rollbar


@disable_rollbar()
class TestStatus(TestCase):
    '''`Status` CRUD test cases.'''
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        '''Fixtures setup for tests.'''
        self.fixture_user = User.objects.get(id=1)
        self.fixture_status_1 = Status.objects.get(id=1)
        self.fixture_status_2 = Status.objects.get(id=2)
        self.fixture_status_3 = Status.objects.get(id=3)
        self.valid_status_data = {'name': 'Pending'}
        self.invalid_status_data = {'name': ''}  # empty name
        self.update_status_data = {'name': 'Delayed'}

    def test_status_list(self):
        '''Tests for getting statuses's list.'''
        # GET response check without login
        response = self.client.get(REVERSE_STATUSES)
        self.assertRedirects(response, REVERSE_LOGIN, HTTPStatus.FOUND)

        # GET response check with login
        self.client.force_login(self.fixture_user)
        response = self.client.get(REVERSE_STATUSES)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.fixture_status_1)
        self.assertContains(response, self.fixture_status_1)
        self.assertContains(response, self.fixture_status_1)
        self.assertTemplateUsed(response, TEMPLATE_LIST)

    def test_status_create(self):
        '''Tests for statuses's creation.'''
        # GET response check without login
        response = self.client.get(REVERSE_CREATE)
        self.assertRedirects(response, REVERSE_LOGIN, HTTPStatus.FOUND)

        # GET response check with login
        self.client.force_login(self.fixture_user)
        response = self.client.get(REVERSE_CREATE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, TEMPLATE_CREATE)

        # Valid POST response check
        response = self.client.post(REVERSE_CREATE, data=self.valid_status_data)
        self.assertRedirects(response, REVERSE_STATUSES, HTTPStatus.FOUND)
        self.assertTrue(Status.objects.filter(name='Pending').exists())

        # Invalid POST reponse check: name is empty
        response = self.client.post(REVERSE_CREATE, data=self.invalid_status_data)
        self.assertIn('name', response.context['form'].errors)
        self.assertContains(response, 'Обязательное поле.')

    def test_status_update(self):
        '''Tests for status's update.'''
        URL_PATH = reverse_lazy(UPDATE_STATUS, kwargs={'pk': self.fixture_status_1.id})

        # GET response check without login
        response = self.client.get(URL_PATH)
        self.assertRedirects(response, REVERSE_LOGIN, HTTPStatus.FOUND)

        # GET response check with login
        self.client.force_login(self.fixture_user)
        response = self.client.get(URL_PATH)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, TEMPLATE_UPDATE)

        # POST response check
        response = self.client.post(URL_PATH, data=self.update_status_data)
        updated_status = Status.objects.get(id=1)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_STATUSES)
        self.assertEqual(updated_status.name, self.update_status_data['name'])

    def test_status_delete(self):
        '''Tests for status's delete.'''
        URL_PATH = reverse_lazy(DELETE_STATUS, kwargs={'pk': self.fixture_status_1.id})

        # GET response check without login
        response = self.client.get(URL_PATH)
        self.assertRedirects(response, REVERSE_LOGIN, HTTPStatus.FOUND)

        # GET response check with login
        self.client.force_login(self.fixture_user)
        response = self.client.get(URL_PATH)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, TEMPLATE_DELETE)

        # POST response check
        response = self.client.post(URL_PATH)
        self.assertRedirects(response, REVERSE_STATUSES, HTTPStatus.FOUND)
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(id=self.fixture_status_1.id)


@disable_rollbar()
class TestStatusRelations(TestCase):
    '''`Status` test cases with related `Task`'''
    fixtures = ['users.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        '''Fixtures setup for tests.'''
        self.fixture_user = User.objects.get(id=1)
        self.fixture_status_1 = Status.objects.get(id=1)

    def test_status_with_task_delete(self):
        '''Tests for status's delete which used in task.'''
        URL_PATH = reverse_lazy(DELETE_STATUS, kwargs={'pk': self.fixture_status_1.id})
        self.client.force_login(self.fixture_user)
        response = self.client.post(URL_PATH)
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, REVERSE_STATUSES, HTTPStatus.FOUND)
        self.assertEqual(str(messages[0]), STATUS_USED_IN_TASK)
