"""
Tests for activities listing endpoint (GET /activities).

Verifies that the activities endpoint returns correct response structure
and contains expected activity data.
"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint behavior."""

    def test_get_activities_returns_dict(self, client):
        """
        Test that GET /activities returns a dictionary of activities.

        Arrange: Request is prepared by test client
        Act: Send GET request to /activities
        Assert: Response status is 200 and response is a dictionary
        """
        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_get_activities_contains_expected_fields(self, client):
        """
        Test that each activity has the expected fields.

        Arrange: Request is prepared by test client
        Act: Send GET request to /activities and extract first activity
        Assert: Activity object contains all required fields
        """
        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert - verify at least one activity exists
        assert len(activities) > 0

        # Get first activity and verify required fields
        first_activity_name = list(activities.keys())[0]
        activity = activities[first_activity_name]

        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity

    def test_get_activities_participants_is_list(self, client):
        """
        Test that participants field is a list in each activity.

        Arrange: Request is prepared by test client
        Act: Send GET request to /activities
        Assert: All activity participants lists contain only strings
        """
        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity in activities.items():
            assert isinstance(activity["participants"], list)
            for participant in activity["participants"]:
                assert isinstance(participant, str)

    def test_get_activities_chess_club_present(self, client):
        """
        Test that Chess Club activity is present with expected data.

        Arrange: Request is prepared by test client
        Act: Send GET request to /activities
        Assert: Chess Club exists and has correct initial participants
        """
        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert "Chess Club" in activities
        chess_club = activities["Chess Club"]
        assert chess_club["max_participants"] == 12
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]
