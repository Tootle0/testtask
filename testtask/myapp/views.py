import random

from django.http import Http404
from rest_framework import views, status, response
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Query
from .serializers import QuerySerializer

import time


class QueryView(views.APIView):
    def get(self, request, cadastre_number, *args, **kwargs):
        # Получение параметров запроса

        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')

        if not cadastre_number or not latitude or not longitude:
            raise Http404("Incomplete parameters in the request.")

        # Симуляция обработки запроса внешним сервером
        time.sleep(60)
        # В данном примере просто генерируем случайный ответ
        external_server_response = True if random.choice([True, False]) else False

        # Сохранение query в базу данных
        query = Query.objects.create(
            cadastre_number=cadastre_number,
            latitude=latitude,
            longitude=longitude,
            external_server_response=external_server_response
        )
        # Возвращение сериализированых параметров запроса в ответ
        return Response(QuerySerializer(query).data, status=status.HTTP_201_CREATED)


class ResultView(views.APIView):
    def get(self, request, *args, **kwargs):
        # Обработка GET запроса если требуется
        return Response({'message': 'Метод GET обработан'}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Получение параметров запроса
        query_id = request.data.get('query_id')
        result = request.data.get('result')

        try:
            # Попытка получение Query объекта
            query = Query.objects.get(pk=query_id)
        except Query.DoesNotExist:
            # Если Query не найден, то возвращаем ошибку 404
            return Response({'message': 'Query not found'}, status=status.HTTP_404_NOT_FOUND)

        # Обновление Query объекта и его сохранение
        query.external_server_response = result
        query.save()

        # Возвращение сериализированных параметров
        return Response(QuerySerializer(query).data, status=status.HTTP_200_OK)


class PingView(views.APIView):
    def get(self, request, *args, **kwargs):
        # Возвращение ответа от сервера что сервер запущен
        return Response({'status': 'Сервер запущен'}, status=200)


class HistoryView(views.APIView):
    def get(self, request, *args, **kwargs):
        # Получение всех queries из ДБ
        history = Query.objects.all()
        # Сериализация всех queries и возвращение в ответ
        serializer = QuerySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
