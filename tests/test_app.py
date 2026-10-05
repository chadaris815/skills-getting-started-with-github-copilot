from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "student@mergington.edu"

    activities[activity_name]["participants"].append(email)

    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }


def test_unregister_participant_returns_404_when_activity_does_not_exist():
    response = client.delete(
        "/activities/Unknown Activity/participants/student@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
