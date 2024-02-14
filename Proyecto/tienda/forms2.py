from django.forms import ModelForm
from .models import Task
from .models import Queja

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        

class QuejaForm(ModelForm):
    class Meta:
        model = Queja
        fields = ['asunto', 'description_queja', 'resolved_queja', 'positive_queja', 'negative_queja']