from django import template
from django.contrib.contenttypes.models import ContentType

from videostream.models import BasicVideo, EmbedVideo, FlashVideo


register = template.Library()


@register.inclusion_tag('videostream/include/render_video.html')
def render_video(video_instance, width=320, height=240):
    """
    This is a intelligent inclusion tag that will try do determine what kind
    of video ``video_instance`` is, and then render the correct HTML for this
    video.

    ``width`` and ``height`` refers to the width and height of the video.

    Example Usage:
        {% render_video video 640 480 %}

    """
    try:
        if video_instance.basicvideo:
            video_type = 'basicvideo'
    except:
        pass

    try:
        if video_instance.embedvideo:
            video_type = 'embedvideo'
    except:
        pass

    try:
        if video_instance.flashvideo:
            video_type = 'flashvideo'
    except:
        pass

    return locals() 
