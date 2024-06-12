from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import Genre, Play
from theatre.serializers import PlayListSerializer, PlayDetailSerializer
from theatre.tests.test_actor_api import sample_actor

LIST_URL = reverse("theatre:play-list")


def detail_url(play_id: int) -> str:
    return reverse("theatre:play-detail", args=[play_id])


def sample_play(**params) -> Play:
    defaults = {
        "title": "Sample play",
        "description": "Sample description",
    }
    defaults.update(params)

    return Play.objects.create(**defaults)


def sample_genre(name="Tragedy") -> Genre:
    return Genre.objects.create(name=name)


class UnauthenticatedPlayViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlayViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test12345"
        )
        self.client.force_authenticate(self.user)

    def test_list_plays(self):
        genre = sample_genre()
        actor = sample_actor()

        play = sample_play()
        play.actors.add(actor.id)
        play.genres.add(genre.id)

        response = self.client.get(LIST_URL)

        plays = Play.objects.all()
        serializer = PlayListSerializer(plays, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_play(self):
        genre = sample_genre()
        actor = sample_actor()

        play = sample_play()
        play.actors.add(actor.id)
        play.genres.add(genre.id)

        url = detail_url(play.id)
        response = self.client.get(url)
        serializer = PlayDetailSerializer(play)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_play_forbidden(self):
        genre = sample_genre()
        actor = sample_actor()

        response = self.client.post(
            LIST_URL,
            {
                "title": "test",
                "description": "text",
                "genres": genre.id,
                "actors": actor.id
            }
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_by_title(self):
        play1 = sample_play()

        play2 = sample_play(
            title="Sample play 2",
            description="Sample play text 2"
        )

        response = self.client.get(LIST_URL, {"title": "Sample play"})

        serializer1 = PlayListSerializer(play1)
        serializer2 = PlayListSerializer(play2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

    def test_filter_by_genre(self):
        play1 = sample_play()

        play2 = sample_play(
            title="sample play 2",
            description="sample play text"
        )
        play3 = sample_play(
            title="sample play 3",
            description="sample play text"
        )

        genre1 = sample_genre()
        genre2 = sample_genre(name="Drama")

        play1.genres.add(genre1)
        play2.genres.add(genre2)

        response = self.client.get(
            LIST_URL,
            {"genres": f"{genre1.id},{genre2.id}"}
        )

        serializer1 = PlayListSerializer(play1)
        serializer2 = PlayListSerializer(play2)
        serializer3 = PlayListSerializer(play3)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, response.data)
        self.assertIn(serializer2.data, response.data)
        self.assertNotIn(serializer3.data, response.data)

    def test_filter_by_actor(self):
        play1 = sample_play()

        play2 = sample_play(
            title="play2",
            description="play2 description"
        )
        play3 = Play.objects.create(
            title="play3",
            description="play3 description"
        )

        actor1 = sample_actor()
        actor2 = sample_actor(
            first_name="Emma", last_name="Stone"
        )

        play1.actors.add(actor1)
        play2.actors.add(actor2)

        response = self.client.get(
            LIST_URL,
            {"actors": f"{actor1.id},{actor2.id}"}
        )

        serializer1 = PlayListSerializer(play1)
        serializer2 = PlayListSerializer(play2)
        serializer3 = PlayListSerializer(play3)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, response.data)
        self.assertIn(serializer2.data, response.data)
        self.assertNotIn(serializer3.data, response.data)


class AdminPlayViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@mail.com",
            password="test12345",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_play(self):
        actor = sample_actor()
        genre = Genre.objects.create(name="Drama")

        response = self.client.post(
            LIST_URL,
            {
                "title": "test",
                "description": "description",
                "actors": actor.id,
                "genres": genre.id
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Play.objects.filter(title="test").exists())
