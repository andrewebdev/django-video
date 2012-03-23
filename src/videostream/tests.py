from datetime import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from videostream.models import VideoCategory, Video


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
        self.assertEquals(2, VideoCategory.objects.all().count())

    def test_absolute_url(self):
        self.assertEqual('/category/category-1/',
            VideoCategory.objects.get(id=1).get_absolute_url())


class VideoTestCase(TestCase):

    fixtures = ['videostream_test_fixtures.json']
    urls = 'videostream.urls'

    def test_model_exists(self):
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
            now.strftime('%Y'), now.strftime('%m'), now.strftime('%d'),
            'video-1')

        self.assertEqual(expected_url, v.get_absolute_url())

