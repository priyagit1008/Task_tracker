from rest_framework import serializers
from rest_framework.validators import UniqueValidator 
from django.core.validators import validate_email

from django.contrib.postgres.fields import ArrayField

from libs.helpers import time_it
from .models import Task_tracker


class TaskAddSerializer(serializers.ModelSerializer):
    task_name = serializers.EmailField(required=True)
    project_name = serializers.CharField(required=True, min_length=5)
    start_time = serializers.DateTimeField(required=True)
    end_time = serializers.DateTimeField(required=True)
    discription = serializers.IntegerField(required=True)

    def validate(self, data):
        task_obj = self.Meta.model(**data)
        task_obj.full_clean()
        return data
    
   
    class Meta:
        model = Task_tracker
        fields = '__all__'
        # read_only_fields = ('id',)
    


    @time_it
    def create(self, validated_data):
        task = Task_tracker.objects.create(**validated_data)
        return task





class TaskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task_tracker
        fields = '__all__'


class TaskGetallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_tracker
        fields = '__all__'