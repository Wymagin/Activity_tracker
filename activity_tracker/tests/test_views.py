import pytest
from django.urls import reverse
from activity_tracker.views import home_view, sign_up, login_view, logout_view
from django.contrib.auth import get_user_model


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username='testuser', password='uwu2132')

@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_home_view_rendering(client):
    response = client.get(reverse('home'))
    assert 'form' in response.context
    assert 'demo_bar_chart_div' in response.context
    assert 'demo_pie_chart_div' in response.context
    assert 'demo_tree_chart_div' in response.context
    
@pytest.mark.django_db    
def test_base_view_redirecting_to_home_view(client):
    response = client.get(reverse('base'))
    assert response.status_code == 302  # Should redirect to 'home'
    assert response.url == reverse('home')
    assert response['Location'] == reverse('home')

@pytest.mark.django_db
def test_base_view_dashboard_hidden_from_unauthenticated_users(client):
    response = client.get(reverse('base'), follow=True)
    assert response.status_code == 200
    assert b'Dashboard' not in response.content
    
@pytest.mark.django_db
def test_base_view_dashboard_visible_to_authenticated_users(client, user):
    client.force_login(user)
    response = client.get(reverse('base'), follow=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.content
    