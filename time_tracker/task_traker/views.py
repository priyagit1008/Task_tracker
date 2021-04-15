from __future__ import unicode_literals
import functools
import time

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import GenericViewSet
from .models import Task_tracker
from .serializers import TaskAddSerializer, TaskListSerializer,TaskGetallSerializer
from libs.constants import BAD_REQUEST, BAD_ACTION, ALREADY_EXIST
from libs.error_messages import ERROR_MESSAGE
from libs.exceptions import ParseException

# Create your views here.
class TaskViewSet(GenericViewSet):

	queryset = Task_tracker.objects.all().order_by('-created_at')

	services = TaskServices()
	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'task_add': TaskAddSerializer,
		'task_list': TaskListSerializer,
		'task_get': TaskGetallSerializer,
		}


	def get_queryset(self, filterdata=None):
		if filterdata:
			self.queryset = Task_tracker.objects.filter(**filterdata)
		return self.queryset

	def get_serializer_class(self):
		"""
		Returns serializer class
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)
	

	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated,], )
	def task_add(self, request):

		serializer = self.get_serializer(data=request.data)
		if not serializer.is_valid():
			return Response({"status":"Invalid input"},status=status.HTTP_400_BAD_REQUEST)
		task = serializer.create(serializer.validated_data)

		if task:
			return Response({'status': 'Successfully added'}, status.HTTP_201_CREATED)

		return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)
	

	@action(methods=['get', 'patch'], detail=False, permission_classes=[IsAuthenticated, ], )
	def task_get(self, request):
		"""
		task get
		"""
		id = request.GET.get('id', None)
		if not id:
			return Response({"status": False, "message": "id is required"})
		try:
			serializer = self.get_serializer(self.services.get_task(id))
		except Task_tracker.DoesNotExist:

			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)
		return Response(serializer.data, status.HTTP_200_OK)
	

	@action(
		methods=['get'],
		detail=False,
		permission_classes=[],
	)
	def task_list(self, request, **dict):
		"""
		Return task list data and groups
		"""
		data = self.get_serializer(self.get_queryset(), many=True).data
		return Response(data, status.HTTP_200_OK)


	@action(
		methods=['get'],
		detail=False,
		permission_classes=[],
	)
	def timer(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			start_time = time.perf_counter()
			value = func(*args, **kwargs)
			end_time = time.perf_counter()
			run_time = end_time - start_time
			return Response(run_time,status.HTTP_200_OK)