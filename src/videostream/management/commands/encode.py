# -*- coding: utf-8 -*-

import commands
import os

from django.core.management.base import NoArgsCommand

from videostream.utils import encode_video_set


class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        """ Encode all pending streams """
        encode_video_set()
