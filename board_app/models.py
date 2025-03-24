from django.db import models

class Contact(models.Model):
    color = models.CharField(max_length=20)
    email = models.EmailField()
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('urgent', 'Urgent'),
    )

    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('awaiting_feedback', 'Awaiting Feedback'),
        ('done', 'Done'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    prio = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    category = models.BooleanField(default=False)
    assigned_to = models.ManyToManyField(Contact, related_name='tasks')

    def __str__(self):
        return self.title

class SubTask(models.Model):
    task = models.ForeignKey(Task, related_name='sub_tasks', on_delete=models.CASCADE)
    subtitle = models.CharField(max_length=200)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.subtitle

class LoginData(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Besser später mit Hashing!

    def __str__(self):
        return self.email
