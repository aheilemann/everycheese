from django.views.generic import ListView
from .models import Cheese


class CheeseListView(ListView):
    model = Cheese
