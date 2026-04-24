"""
Tests for participant removal endpoint (DELETE /activities/{activity_name}/participants).

Verifies successful removal of participants, handling of missing participants,
and unknown activity cases.
"""

import pytest


class TestUnregisterParticipant:
    """Test suite for DELETE /activities/{activity_name}/participants endpoint behavior."""

    def test_unregister_existing_participant_success(self, client):
        """
        Test successful removal of an existing participant from an activity.

        Arrange: Identify an existing participant in an activity
        Act: Send DELETE request to unregister them
        Assert: Response status is 200 with confirmation message
        """
        # Arrange
        activity_name = "Chess Club"
        participant_email = "michael@mergington.edu"  # Exists in Chess Club

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": participant_email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]
        assert participant_email in data["message"]

    def test_unregister_removes_from_activities_list(self, client):
        """
        Test that unregistered participant no longer appears in activities.

        Arrange: Note initial participant count
        Act: Unregister a participant and verify activity list
        Assert: Participant is removed from the activity's participants list
        """
        # Arrange
        activity_name = "Gym Class"
        participant_email = "john@mergington.edu"

        # Act - Unregister
        client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": participant_email}
        )

        # Act - Retrieve activities
        activities_response = client.get("/activities")
        activities = activities_response.json()

        # Assert
        assert participant_email not in activities[activity_name]["participants"]

    def test_unregister_nonexistent_participant_fails(self, client):
        """
        Test that unregistering a non-participant fails.

        Arrange: Prepare unregister request for someone not in activity
        Act: Send DELETE request with email not in participants
        Assert: Response status is 404 with participant not found message
        """
        # Arrange
        activity_name = "Chess Club"
        nonexistent_email = "notasignup@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": nonexistent_email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Participant not found" in data["detail"]

    def test_unregister_unknown_activity_fails(self, client):
        """
        Test that unregister fails when activity does not exist.

        Arrange: Prepare unregister request for nonexistent activity
        Act: Send DELETE request with invalid activity name
        Assert: Response status is 404 with activity not found message
        """
        # Arrange
        unknown_activity = "Fictional Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{unknown_activity}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_then_unregister_lifecycle(self, client):
        """
        Test full lifecycle: signup then unregister in sequence.

        Arrange: Prepare new email for signup
        Act: Sign up, verify presence, unregister, verify absence
        Assert: All operations succeed and participant state changes correctly
        """
        # Arrange
        activity_name = "Basketball"
        new_email = "lifecycle@mergington.edu"

        # Act - Sign up
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )

        # Assert signup successful
        assert signup_response.status_code == 200

        # Act - Verify in activities
        check_response = client.get("/activities")
        activities = check_response.json()
        assert new_email in activities[activity_name]["participants"]

        # Act - Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": new_email}
        )

        # Assert unregister successful
        assert unregister_response.status_code == 200

        # Act - Verify no longer in activities
        final_check = client.get("/activities")
        final_activities = final_check.json()
        assert new_email not in final_activities[activity_name]["participants"]

    def test_unregister_one_participant_leaves_others(self, client):
        """
        Test that removing one participant doesn't affect others in same activity.

        Arrange: Identify activity with multiple participants
        Act: Unregister one participant and check others remain
        Assert: Unregistered participant is gone but others still present
        """
        # Arrange
        activity_name = "Chess Club"
        participant_to_remove = "michael@mergington.edu"
        participant_to_keep = "daniel@mergington.edu"

        # Act
        client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": participant_to_remove}
        )

        # Assert
        activities_response = client.get("/activities")
        activities = activities_response.json()
        participants = activities[activity_name]["participants"]

        assert participant_to_remove not in participants
        assert participant_to_keep in participants
