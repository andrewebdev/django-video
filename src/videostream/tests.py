from django.test import TestCase
from videostream.models import VideoCategory

class BaseTestCase(TestCase):
    def setUp(self):
        self.category1 = VideoCategory(
            title="News",
            slug="news",
        )
        self.category1.save()

class VideoCategoryTestCase(BaseTestCase):
    def testCategories(self):
        self.assertEquals(
            len(VideoCategory.objects.all()),
            1
        )
