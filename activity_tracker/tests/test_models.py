import pytest
from activity_tracker.models import Activity, User


@pytest.mark.django_db
def test_activity_creation():
    user = User.objects.create(username="testuser")
    activity = Activity.objects.create(
        user=user,
        activity_type="work",
        name = "Test Activity",
        description = "This is a test activity",
        start_time = "2023-10-01 10:00:00",
        end_time = "2023-10-01 11:00:00",

    )

    assert activity.user == user
    assert activity.activity_type == "work"
    assert activity.name == "Test Activity"
    assert activity.description == "This is a test activity"
    assert activity.start_time == "2023-10-01 10:00:00"
    assert activity.end_time == "2023-10-01 11:00:00"
    assert activity.duration == "1:00:00"

