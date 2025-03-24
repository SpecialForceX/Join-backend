from rest_framework import serializers
from .models import Contact, Task, SubTask, LoginData


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        exclude = ['task']  # 👈 task-Feld wird automatisch gesetzt


class TaskSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False, allow_blank=True)  # <--- HIER!

    sub_tasks = SubTaskSerializer(many=True)
    assigned_to = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Contact.objects.all(),
        required=False,
        allow_empty=True
    )

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        sub_tasks_data = validated_data.pop('sub_tasks', [])
        assigned_contacts = validated_data.pop('assigned_to', [])
        task = Task.objects.create(**validated_data)
        task.assigned_to.set(assigned_contacts)
        for subtask_data in sub_tasks_data:
            SubTask.objects.create(task=task, **subtask_data)
        return task

    def update(self, instance, validated_data):
        sub_tasks_data = validated_data.pop('sub_tasks', [])
        assigned_contacts = validated_data.pop('assigned_to', [])

        # Update Felder des Tasks selbst
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.assigned_to.set(assigned_contacts)
        instance.save()

        # Alte SubTasks löschen
        instance.sub_tasks.all().delete()

        # Neue SubTasks anlegen
        for subtask_data in sub_tasks_data:
            SubTask.objects.create(task=instance, **subtask_data)

        return instance


class LoginDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginData
        fields = '__all__'
