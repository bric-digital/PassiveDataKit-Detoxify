# pylint: disable=no-member,line-too-long

from __future__ import print_function

import json

import numpy

from django.core.management.base import BaseCommand

from ...annotators.pdk_detoxify_annotator import annotate

class NumPyEncoder(json.JSONEncoder):
    def default(self, o): # pylint: disable=method-hidden
        if isinstance(o, numpy.integer):
            return int(o)

        if isinstance(o, numpy.floating):
            return float(o)

        if isinstance(o, numpy.ndarray):
            return o.tolist()

        return json.JSONEncoder.default(self, o)

class Command(BaseCommand):
    help = 'Generates Detoxify scores for the provided text.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options): # pylint: disable=too-many-locals, too-many-branches, too-many-statements
        content = input('Enter the text to score: ') # nosec

        results = annotate(content)

        print(json.dumps(results, indent=2, cls=NumPyEncoder))
