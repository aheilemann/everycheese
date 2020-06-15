import pytest
from pytest_django.asserts import assertContains

from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from everycheese.users.models import User
from ..models import Cheese
from ..views import (
    CheeseCreateView,
    CheeseListView,
    CheeseDetailView
)
from .factories import CheeseFactory

pytestmark = pytest.mark.django_db


def test_cheese_list(rf):
    # Get the request
    request = rf.get(reverse("cheeses:list"))
    # Use the request to get the response
    response = CheeseListView.as_view()(request)
    # Test that the response is valid
    assertContains(response, 'Cheese List')


def test_cheese_list_contains_2_cheese(rf):
    # Create some cheese
    cheese1 = CheeseFactory()
    cheese2 = CheeseFactory()
    # Create a request/response for the list of cheese
    request = rf.get(reverse("cheeses:list"))
    response = CheeseListView.as_view()(request)
    # Assert that the created cheeses appear in the list
    assertContains(response, cheese1.name)
    assertContains(response, cheese2.name)


def test_cheese_detail_view(rf):
    # Order some cheese from the CheeseFactory
    cheese = CheeseFactory()
    # Make a request for our new cheese
    url = reverse("cheeses:detail", kwargs={'slug': cheese.slug})
    # url = cheese.get_absolute_url()
    request = rf.get(url)

    # Use the request to get the response
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    # Test that the response is valid
    assertContains(response, cheese.name)


def test_cheese_detail_contain_data(rf):
    cheese = CheeseFactory()
    # Make request for newly created cheese
    url = reverse("cheeses:detail", kwargs={'slug': cheese.slug})
    request = rf.get(url)

    # Get response
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    # tests
    assertContains(response, cheese.name)
    assertContains(response, cheese.get_firmness_display())
    assertContains(response, cheese.country_of_origin.name)


def test_cheese_create_view(rf, admin_user):
    # Order some cheese from the CheeseFactory
    cheese = CheeseFactory()  # why this?
    # Make a request for our new cheese
    request = rf.get(reverse("cheeses:add"))
    # Add an authenticated user
    request.user = admin_user
    # Use the request to get the response
    response = CheeseCreateView.as_view()(request)
    # Test that the response is valid
    assert response.status_code == 200


def test_cheese_create_form_valid(rf, admin_user):
    # Submit the cheese add form
    form_data = {
        "name": "Paski Sir",
        "description": "A salty hard cheese",
        "firmness": Cheese.Firmness.HARD
    }
    request = rf.post(reverse("cheeses:add"), form_data)
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)

    # Get the cheese based on the name
    cheese = Cheese.objects.get(name="Paski Sir")

    # Test the the cheese matches our form
    assert cheese.description == "A salty hard cheese"
    assert cheese.firmness == Cheese.Firmness.HARD
    assert cheese.creator == admin_user
