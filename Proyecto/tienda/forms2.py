from django.forms import ModelForm
from .models import Queja

class QuejaForm(ModelForm):
    class Meta:
        model = Queja
        fields = ['asunto', 'description_queja', 'resolved_queja', 'positive_queja', 'negative_queja']
