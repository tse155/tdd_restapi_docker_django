# import json

import pytest  # type:ignore

from movies.models import Movie


# test for create views
@pytest.mark.django_db
def test_add_movie(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        "/api/movies/",
        {
            "title": "The Big Lebowski",
            "genre": "comedy",
            "year": "1998",
        },
        content_type="application/json",
    )
    assert resp.status_code == 201
    assert resp.data["title"] == "The Big Lebowski"

    movies = Movie.objects.all()
    assert len(movies) == 1


@pytest.mark.django_db
def test_add_movie_invalid_json(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post("/api/movies/", {}, content_type="application/json")
    assert resp.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_add_movie_invalid_json_keys(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        "/api/movies/",
        {
            "title": "The Big Lebowski",
            "genre": "comedy",
        },
        content_type="application/json",
    )
    assert resp.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0


# Tests for get movies
@pytest.mark.django_db
def test_get_single_movie(client, add_movie):
    # add_movie -> from conftests
    movie = add_movie(title="The Big Short", genre="comedy", year="2014")
    resp = client.get(f"/api/movies/{movie.id}/")
    assert resp.status_code == 200
    assert resp.data["title"] == movie.title


# @pytest.mark.django_db
# def test_get_single_movie(client):
#
#     movie = Movie.objects.create(title="The Big Lebowski", genre="comedy", year="1998")
#     resp = client.get(f"/api/movies/{movie.id}/")  # type: ignore
#     assert resp.status_code == 200
#     assert resp.data["title"] == "The Big Lebowski"


@pytest.mark.django_db
def test_get_all_movies(client, add_movie):
    movie_one = add_movie(title="The Big Short", genre="comedy", year="2014")
    movie_two = add_movie("LOTR", "thriller", "2001")
    resp = client.get("/api/movies/")
    assert resp.status_code == 200
    assert resp.data[0]["title"] == movie_one.title
    assert resp.data[1]["title"] == movie_two.title


@pytest.mark.django_db
def test_get_single_movie_incorrect_id(client):
    resp = client.get("/api/movies/166/")
    assert resp.status_code == 404


# @pytest.mark.django_db
# def test_get_various_movie(client):
#     # tests valid retrieval AND 404 behavior
#     ## TEST FOR RETRIEVING VARIOUS ENTRIES WITHOUT REUSABILITY
#     movie = Movie.objects.create(title="The Big Lebowski", genre="comedy", year="1998")
#     movie2 = Movie.objects.create(
#         title="No Country for Old Men", genre="comedy", year="1998"
#     )
#     resp = client.get("/api/movies/")  # type: ignore
#     assert resp.status_code == 200
#     assert resp.data[0]["title"] == movie.title
#     assert resp.data[1]["title"] == movie2.title
#     resp2 = client.get("/api/movies/166/")  # type: ignore
#     assert resp2.status_code == 404
# Tests for delete
@pytest.mark.django_db
def test_remove_movie(client, add_movie):
    movie = add_movie(title="Sinners", genre="horror", year="2026")

    resp = client.get(f"/api/movies/{movie.id}/")
    assert resp.status_code == 200
    assert resp.data["title"] == "Sinners"

    resp_two = client.delete(f"/api/movies/{movie.id}/")
    assert resp_two.status_code == 204

    resp_three = client.get("/api/movies/")
    assert resp_three.status_code == 200
    assert len(resp_three.data) == 0


@pytest.mark.django_db
def test_remove_movie_incorrect_id(client):
    resp = client.delete("/api/movies/99/")
    assert resp.status_code == 404
