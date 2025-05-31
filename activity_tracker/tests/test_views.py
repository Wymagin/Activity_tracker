import pytest
from django.urls import reverse
from activity_tracker.views import home_view, sign_up, login_view, logout_view


def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    

def test_home_view_rendering(client):
    response = client.get(reverse('home'))
    assert 'form' in response.context
    assert 'demo_bar_chart_div' in response.context
    assert 'demo_pie_chart_div' in response.context
    assert 'demo_tree_chart_div' in response.context