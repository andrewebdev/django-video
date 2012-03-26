from datetime import datetime

from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from videostream.models import (VideoCategory, Video, BasicVideo, HTML5Video,
    EmbedVideo, FlashVideo)


## Models (including basic urls for permalink lookups)
class VideoCategoryTestCase(TestCase):

    fixtures = ['videostream_test_fixtures.json']
    urls = 'videostream.urls'

    def test_model_exists(self):
        cat = VideoCategory.objects.create(
            title='test', slug='test', description='test category')

    def test_unicode(self):
        self.assertEqual('Category 1',
            VideoCategory.objects.get(id=1).__unicode__())

    def test_verbose_name_plural(self):
        self.assertEqual('Video Categories',
            VideoCategory._meta.verbose_name_plural)

    def test_categories_exist(self):
        self.assertEqual(2, VideoCategory.objects.all().count())

    def test_absolute_url(self):
        self.assertEqual('/category/category-1/',
            VideoCategory.objects.get(id=1).get_absolute_url())


class VideoTestCase(TestCase):

    fixtures = ['videostream_test_fixtures.json']
    urls = 'videostream.urls'

    def test_model(self):
        v = Video.objects.create(
            title='test video 1',
            slug='test-video-1',
            description='test video description',
            tags='tag1 tag2',
            author=User.objects.get(id=1),  # Use our default user
        )

    def test_unicode(self):
        self.assertEqual('Video 1', Video.objects.get(id=1).__unicode__())

    def test_visible_video_has_publish_date(self):
        v = Video.objects.get(id=1)
        self.assertIsNone(v.publish_date)

        v.is_public = True
        v.save()
        self.assertIsNotNone(v.publish_date)

    def test_video_has_categories(self):
        v = Video.objects.get(id=1)
        self.assertEqual(2, v.categories.all().count())

    def test_absolute_url(self):
        v = Video.objects.get(id=1)
        v.is_public = True
        v.save()

        now = datetime.now()
        expected_url = '/%s/%s/%s/%s/' % (
            now.strftime('%Y'), now.strftime('%b'), now.strftime('%d'),
            'video-1')

        self.assertEqual(expected_url, v.get_absolute_url())

    def test_is_parent_class(self):
        # Basically since this is a parent class all other videos that
        # inherrits from this class can also be found through this model
        # Since we have these other videos in the fixtures,
        # this test should pass
        self.assertEqual(3, Video.objects.all().count())


class BasicVideoTestCase(TestCase):

    fixtures = ['videostream_test_fixtures.json']

    def test_model_exists(self):
        v = BasicVideo()  # No need to test other fields since it inherrits

    def test_has_html5videos(self):
        v = BasicVideo.objects.get(id=1)
        self.assertEqual(3, v.html5video_set.all().count())


class HTML5VideoTestCase(TestCase):

    fixtures = ['videostream_test_fixtures.json']

    def test_model(self):
        v = HTML5Video(video_type=1, video_file='test.ogg')

    def test_html5videos_exists(self):
        self.assertEqual(3, HTML5Video.objects.all().count())


class EmbedVideoTestCase(TestCase):

    fixtures = ['videostream_test_fixtures.json']

    def test_model(self):
        v = EmbedVideo.objects.create(
            video_url='http://test.example.com/video/',
            video_code='[video code]'
        )


class FlashVideoTestCase(TestCase):

    fixtures = ['videostream_test_fixtures.json']

    def test_model(self):
        v = FlashVideo(
            original_file='original.mp4',
            flv_file='video.flv',
            thumbnail='thumb.png',
            encode=False
        )

    def test_get_player_size(self):
        self.assertEqual('width: 320px; height: 240px;',
            FlashVideo.objects.get(id=1).get_player_size())


class VideoStreamViewsTestCase(TestCase):

    fixtures = ['videostream_test_fixtures.json']
    urls = 'videostream.urls'

    def setUp(self):
        now = datetime.now()
        self.day = now.strftime('%d')
        self.month = now.strftime('%b')
        self.year = now.strftime('%Y')

        for v in Video.objects.all():
            v.is_public = True
            v.save()

    def test_category_list_view(self):
        c = Client()
        response = c.get('/categories/')
        self.assertEqual(200, response.status_code)
        self.assertIn('object_list', response.context)
        self.assertEqual(2, response.context['object_list'].count())

    def test_category_detail_view(self):
        c = Client()
        response = c.get('/category/category-1/')
        self.assertEqual(200, response.status_code)
        self.assertIn('category', response.context)

    def test_archive_year_view(self):
        c = Client()
        response = c.get('/%s/' % self.year)
        self.assertEqual(200, response.status_code)
        self.assertIn('date_list', response.context)
        self.assertEqual(1, len(response.context['date_list']))

    def test_archive_month_view(self):
        c = Client()
        response = c.get('/%s/%s/' % (self.year, self.month))
        self.assertEqual(200, response.status_code)
        self.assertIn('object_list', response.context)
        self.assertEqual(3, response.context['object_list'].count())

    def test_archive_day_view(self):
        c = Client()
        response = c.get('/%s/%s/%s/' % (self.year, self.month, self.day))
        self.assertEqual(200, response.status_code)
        self.assertIn('object_list', response.context)
        self.assertEqual(3, response.context['object_list'].count())

    def test_video_detail_view(self):
        c = Client()
        response = c.get('/%s/%s/%s/%s/' % (
            self.year, self.month, self.day, 'video-1'))
        self.assertEqual(200, response.status_code)
        self.assertIn('video', response.context)
        self.assertEqual('Video 1', response.context['video'].title)

