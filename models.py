# pylint: disable=line-too-long
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import requests

from django.conf import settings
from django.core.checks import Error, Warning, register # pylint: disable=redefined-builtin

@register()
def check_remote_endpoint(app_configs, **kwargs): # pylint: disable=unused-argument
    errors = []

    if hasattr(settings, 'SIMPLE_DETOXIFY_URL'):
        url = settings.SIMPLE_DETOXIFY_URL

        if url is None:
            error = Error('SIMPLE_DETOXIFY_URL parameter set to None', hint='Update SIMPLE_DETOXIFY_URL to point to Detoxify endpoint.', obj=None, id='passive_data_kit_detoxify.E001')
            errors.append(error)
        else:
            try:
                response = requests.post(url, data={'s': 'Testing the Detoxify endpoint...'}, timeout=120)

                scores = response.json()

                if ('to_score' in scores) is False:
                    error = Error('SIMPLE_DETOXIFY_URL (%s) endpoint provided unexpected result' % url, hint='Check that the Detoxify endpoint server is functioning as intended.', obj=None, id='passive_data_kit_detoxify.E004')
                    errors.append(error)
            except requests.exceptions.ConnectionError:
                error = Error('Unable to connect to SIMPLE_DETOXIFY_URL (%s)' % url, hint='Check that the Detoxify endpoint is online.', obj=None, id='passive_data_kit_detoxify.E002')
                errors.append(error)
            except requests.exceptions.ReadTimeout:
                error = Error('SIMPLE_DETOXIFY_URL (%s) took too long to respond' % url, hint='Check that the Detoxify endpoint server is not overloaded.', obj=None, id='passive_data_kit_detoxify.E003')
                errors.append(error)
            except requests.exceptions.JSONDecodeError:
                error = Error('SIMPLE_DETOXIFY_URL (%s) returned an invalid result' % url, hint='Check that the Detoxify endpoint server is functioning properly.', obj=None, id='passive_data_kit_detoxify.E005')
                errors.append(error)
    else:
        error = Error('SIMPLE_DETOXIFY_URL not defined', hint='Update SIMPLE_DETOXIFY_URL to point to Detoxify endpoint.', obj=None, id='passive_data_kit_detoxify.E999')
        errors.append(error)

    return errors

@register()
def check_retain_text(app_configs, **kwargs): # pylint: disable=unused-argument
    errors = []

    if hasattr(settings, 'SIMPLE_DETOXIFY_RETAIN_SCORED_TEXT') is False:
        error = Warning('Please explicitly specify whether to retain scored text by setting SIMPLE_DETOXIFY_RETAIN_SCORED_TEXT to True or False.', hint='Update SIMPLE_DETOXIFY_RETAIN_SCORED_TEXT to be True or False.', obj=None, id='passive_data_kit_detoxify.W001')
        errors.append(error)

    return errors
