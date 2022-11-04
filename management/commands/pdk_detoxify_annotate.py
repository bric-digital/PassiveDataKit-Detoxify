# pylint: disable=no-member,line-too-long

from __future__ import print_function

import json

import numpy

from django.core.management.base import BaseCommand

from ...annotators.pdk_detoxify_annotator import annotate

class NumPyEncoder(json.JSONEncoder):
    def default(self, obj): # pylint: disable=arguments-renamed
        if isinstance(obj, numpy.integer):
            return int(obj)
        if isinstance(obj, numpy.floating):
            # 👇️ alternatively use str()
            return float(obj)
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

class Command(BaseCommand):
    help = 'Generates Detoxify scores for the provided text.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options): # pylint: disable=too-many-locals, too-many-branches, too-many-statements
        content = input('Enter the text to score: ')

        results = annotate(content)

        print(json.dumps(results, indent=2, cls=NumPyEncoder))
