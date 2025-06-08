import pytest
from django.urls import reverse
from activity_tracker.views import home_view, sign_up, login_view, logout_view
from django.contrib.auth import get_user_model


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username='testuser', password='uwu2132')
    
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
    
@pytest.mark.django_db
def test_base_view_login_and_register_links_visible_to_unauthenticated_users(client):
    response = client.get(reverse('base'), follow=True)
    assert response.status_code == 200
    assert b'Login' in response.content
    assert b'Create Account' in response.content

@pytest.mark.django_db
def test_base_view_login_and_register_links_hidden_from_authenticated_users(client, user):
    client.force_login(user)
    response = client.get(reverse('base'), follow=True)
    assert response.status_code == 200
    assert b'Login' not in response.content
    assert b'Create Account' not in response.content

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
def test_sign_up_view_get_request(client):
    response = client.get(reverse('register'))
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_sign_up_view_post_request(client):
    response = client.post(reverse('register'),{
        'username': 'newuser11',
        'email': 'wym@gmmail.com',
        'password1': 'Password1231!',
        'password2': 'Password1231!',
        })
    assert response.status_code == 302
    assert response.url == reverse('login')
    assert get_user_model().objects.filter(username='newuser11').exists()
    assert get_user_model().objects.get(username='newuser11').check_password('Password1231!')
    
@pytest.mark.django_db
def test_login_view_get_request(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_login_view_post_request(client, user):
    response = client.post(reverse('login'), {
        'username': user.username,
        'password': 'uwu2132',
    })
    assert response.status_code == 302
    assert response.url == reverse('dashboard')
    assert response.wsgi_request.user.is_authenticated
    
        
@pytest.mark.django_db
def test_logout_view(client, user):
    client.force_login(user)
    response = client.get(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('login')
    assert not response.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_logout_view_redirects_to_login(client, user):
    client.force_login(user)
    response = client.get(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('login')
    assert not response.wsgi_request.user.is_authenticated
    
@pytest.mark.django_db
def test_logout_view_redirects_to_login_if_not_authenticated(client):
    response = client.get(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('login')
    assert not response.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_add_activity_view_get_request(client, user):
    client.force_login(user)
    response = client.get(reverse('add_activity'))
    assert response.status_code == 302
    assert response.url == reverse('dashboard')
    
@pytest.mark.django_db
def test_add_activity_view_post_request(client, user):
    client.force_login(user)
    response = client.post(reverse('add_activity'), {
        'name': 'Test Activity',
        'description': 'This is a test activity',
        'start_time': '2023-10-01T10:00:00Z',
        'end_time': '2023-10-01T11:00:00Z',
        'activity_type': 'work',
    })
    assert response.status_code == 302
    assert response.url == reverse('dashboard')
    assert user.activity_set.filter(name='Test Activity').exists()

@pytest.mark.django_db
def test_dashboard_view(client, user):
    client.force_login(user)
    response = client.get(reverse('dashboard'))
    assert response.status_code == 200
    assert b'Activity Statistics' in response.content
    assert b'Daily Activities' in response.content

@pytest.mark.django_db
def test_dashboard_view_context(client, user):
    client.force_login(user)
    response = client.get(reverse('dashboard'))
    assert response.status_code == 200

    assert 'today_activities' in response.context
    assert 'tag_stats' in response.context
    assert 'expenses_tag_stats' in response.context
    assert 'daily_activities_chart' in response.context
    assert 'activities_by_type_chart' in response.context
    assert 'form' in response.context
    assert 'selected_period' in response.context
    assert response.context['today_activities'] is not None
    assert hasattr(response.context['form'], 'is_valid')

@pytest.mark.django_db
def test_dashboard_view_creates_activity_if_none_exists(client, user):
    client.force_login(user)
    response = client.get(reverse('dashboard'))
    assert response.status_code == 200
    assert user.activity_set.filter(name='Hello', activity_type='Daily visit').exists()
    activity = user.activity_set.get(name='Hello', activity_type='Daily visit')
    assert activity.description == "Thank you for visiting our site today"
   
@pytest.mark.django_db 
def test_dashboard_view_creates_empty_expense_if_none_exists(client, user):
    client.force_login(user)
    response = client.get(reverse('dashboard'))
    assert response.status_code == 200
    assert user.expense_set.filter(category='No data', amount=0).exists()


@pytest.mark.django_db
def test_dashboard_view_requires_login(client):
    response = client.get(reverse('dashboard'))
    assert response.status_code == 302  