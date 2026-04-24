"""
Tests for root endpoint (GET /).

Verifies that the root endpoint correctly redirects to the static index page.
"""

import pytest


class TestRootRedirect:
    """Test suite for GET / endpoint behavior."""

    def test_root_returns_redirect_to_index(self, client):
        """
        Test that GET / returns a redirect response to /static/index.html.

        Arrange: Request is prepared by test client
        Act: Send GET request to /
        Assert: Response status is 307 (temporary redirect) with correct Location header
        """
        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["Location"] == "/static/index.html"

    def test_root_redirect_follow(self, client):
        """
        Test that following the redirect from / leads to index.html.

        Arrange: Request is prepared by test client
        Act: Send GET request to / with follow_redirects=True
        Assert: Final response status is 200 and contains HTML content
        """
        # Act
        response = client.get("/", follow_redirects=True)

        # Assert
        assert response.status_code == 200
        assert "html" in response.text.lower()
