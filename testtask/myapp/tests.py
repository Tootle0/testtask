from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Query


class QueryViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_query_view(self):
        # Создание URL для query с кадастровым номером
        url = reverse('query', args=['12345'])
        # Отправка GET запроса в query с заданной широтой и долготой
        response = self.client.get(url, {'latitude': 35.2345, 'longitude': 23.452})

        # Проверка ответа на 201 код ответа
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверка ответа на содержание данных полей
        self.assertTrue('cadastre_number' in response.data)
        self.assertTrue('latitude' in response.data)
        self.assertTrue('longitude' in response.data)
        self.assertTrue('external_server_response' in response.data)


class ResultsViewTests(TestCase):
    def test_results_view(self):
        # Создание Query объекта
        query = Query.objects.create(
            cadastre_number="12345",
            latitude="35.2345",
            longitude="23.452"
        )

        # Создание URL для result с созданным Query ID
        url = reverse('result', args=[query.id])

        # Данные для отправки в POST запросе
        data = {'query_id': query.id, 'result': True}

        # Отправка POST запроса в result view
        response = self.client.post(url, data)

        # Проверка статуса ответа на 200 код
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PingViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_ping_view(self):
        # Создание URL для ping
        url = reverse('ping')
        # Отправка GET запроса в ping
        response = self.client.get(url)
        # Проверка ответа на 200 код
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка ответа на содержание поля status
        self.assertTrue('status' in response.data)


class HistoryViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_history_view(self):
        # Создание Query объектов для запроса
        Query.objects.create(cadastre_number='123', latitude=35.2345, longitude=23.452)
        Query.objects.create(cadastre_number='456', latitude=36.2345, longitude=24.452)

        # Создание URL для history
        url = reverse('history')
        # Отправка GET запроса в history
        response = self.client.get(url)

        # Проверка ответа на 200 код
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка ответа на то что это лист и его длину
        self.assertTrue(isinstance(response.data, list))
        self.assertEqual(len(response.data), 2)
