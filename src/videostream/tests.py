from django.test import TestCase
from videostream.models import *

class BaseTestCase(TestCase):
    def setUp(self):
        self.category1 = VideoCategory.objects.create(
            title="News",
            slug="news",
        )

        self.video1 = EmbedVideo.objects.create(
            title="Test Video",
            slug="test-video",
            tags="test video",
            description="A simple test video",
            is_public=True,
            allow_comments=True,
            video_url="http://videourl/",
            video_code="<embed>test</embed>",
        )
        self.video1.categories.add(self.category1)

        self.video2 = FlashVideo.objects.create(
            title="Flash Video Test",
            slug="flash-video-test",
            tags="flash test video",
            description="A simple flash video test",
            is_public = False,
            allow_comments = True,
        )
        self.video2.categories.add(self.category1)

class VideoCategoryTestCase(BaseTestCase):
    def testCategories(self):
        self.assertEquals(VideoCategory.objects.all().count(), 1)

    def testCategoryVideos(self):
        self.failUnless(
            self.category1.video_set.all().count() > 0,
            "No embedded videos added to %s Category." % self.category1
        )
    
    def testVideoTypes(self):
        # Test the Base Video Model
        self.failUnless(
            Video.objects.all().count() == 2,
            "Incorrect number of Videos",
        )

        # Test the Embedded Video Model
        self.failUnless(
            EmbedVideo.objects.all().count() == 1,
            "Incorrect number of Embedded Videos",
        )

        # Test the Flash Video Model
        self.failUnless(
            FlashVideo.objects.all().count() == 1,
            "Incorrect number of Flash Videos",
        )

    def testVideoURL(self):
        response = self.client.get(self.video1.get_absolute_url())
        self.failUnlessEqual(response.status_code, 200)

        response = self.client.get(self.video2.get_absolute_url())
        self.failUnlessEqual(response.status_code, 200)
