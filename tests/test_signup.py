"""
Tests for activity signup endpoint (POST /activities/{activity_name}/signup).

Verifies signup success cases, duplicate participant rejection, and
unknown activity handling.
"""

import pytest


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint behavior."""

    def test_signup_new_participant_success(self, client):
        """
        Test successful signup of a new participant to an activity.

        Arrange: Prepare signup request for a new email not yet in activity
        Act: Send POST request to signup endpoint with activity name and email
        Assert: Response status is 200 and confirmation message is returned
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Signed up" in data["message"]
        assert new_email in data["message"]
        assert activity_name in data["message"]

    def test_signup_new_participant_appears_in_activities(self, client):
        """
        Test that newly signed up participant appears in activities list.

        Arrange: Sign up a new participant
        Act: Retrieve activities list to verify participant was added
        Assert: Participant email is in the activity's participants list
        """
        # Arrange
        activity_name = "Programming Class"
        new_email = "alice@mergington.edu"

        # Act - Sign up
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )

        # Act - Retrieve activities
        activities_response = client.get("/activities")
        activities = activities_response.json()

        # Assert
        assert new_email in activities[activity_name]["participants"]

    def test_signup_duplicate_participant_fails(self, client):
        """
        Test that signing up an already-registered participant fails.

        Arrange: Identify an existing participant in an activity
        Act: Attempt to signup the same participant again
        Assert: Response status is 400 with appropriate error message
        """
        # Arrange
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]

    def test_signup_unknown_activity_fails(self, client):
        """
        Test that signup fails when activity does not exist.

        Arrange: Prepare signup request for nonexistent activity
        Act: Send POST request with invalid activity name
        Assert: Response status is 404 with activity not found message
        """
        # Arrange
        unknown_activity = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{unknown_activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_different_activities_independent(self, client):
        """
        Test that signup to one activity does not affect another.

        Arrange: Sign up a participant to one activity
        Act: Verify they can still signup to a different activity
        Assert: Both signups succeed independently
        """
        # Arrange
        email = "versatile@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"

        # Act - Sign up for first activity
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": email}
        )

        # Act - Sign up for second activity
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": email}
        )

        # Assert - Both signups successful
        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify participation in both
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]
