import json

from django.urls import reverse


def test_hello_world():
    assert "hello_world" == "hello_world"
    assert "foo" != "bar"


def test_ping(client):
    # Given
    # Client

    # When
    url = reverse("ping")
    response = client.get(url)
    # print(response.content)
    content = json.loads(response.content)
    # print("status:", response.status_code)
    # print("content:", content)
    # print("headers:", response.headers)

    # Then
    assert response.status_code == 200
    assert content["ping"] == "pong!"
