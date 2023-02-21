# pylint: disable=line-too-long, no-member

from __future__ import print_function

from detoxify import Detoxify

from django.utils.text import slugify

SKIP_FIELD_NAMES = (
    'url',
)

DEFAULT_FIELD_PRIORITIES = (
    'text',
    'caption',
    'fullText',
    'full_text',
    'post',
    'comment',
    'description',
    'title',
    'name',
    'place',
    'location',
)

DETOXIFY_MODELS = (
    'original',
    'unbiased',
    'multilingual',
)

def annotate(content, field_name=None): # pylint: disable=too-many-branches, too-many-statements, too-many-locals
    if field_name in SKIP_FIELD_NAMES:
        return {}

    scores = {}

    if content is None:
        content = ''

    content = content.strip()

    for model in DETOXIFY_MODELS:
        model_scores = Detoxify(model).predict(content)

        scores[slugify(model).replace('-', '_')] = model_scores

    annotation_field = 'pdk_detoxify'

    if field_name is not None:
        annotation_field = 'pdk_detoxify_' + field_name

    return {
        annotation_field: scores,
        # 'cleartext': content,
    }


def fetch_annotation_fields():
    labels = []

    for model in DETOXIFY_MODELS:
        labels.append(slugify(model).replace('-', '_'))

    return labels


def fetch_annotations(properties, initial_field=None): # pylint: disable=unused-argument
    #if isinstance(properties, dict) is False:
    #    return None

    #field_priorities = DEFAULT_FIELD_PRIORITIES

    #try:
    #    field_priorities = settings.PDK_CONTENT_ANALYSIS_FIELD_PRIORITIES
    #except AttributeError:
    #    pass

    #if initial_field is None:
    #    for field in field_priorities:
    #        sentiment_key = 'pdk_detoxify_' + field

    #        if sentiment_key in properties:
    #            annotations = {}

    #            for model in properties[sentiment_key]:
    #                for label in properties[sentiment_key][model]:
    #                    annotations[(model + '_' + label).lower()] = properties[sentiment_key][model][label]

    #            return annotations

    #        annotations = fetch_annotations(properties, field)

    #        if annotations is not None:
    #            return annotations
    #else:
    #    sentiment_key = 'pdk_detoxify_' + initial_field

    #    if sentiment_key in properties:
    #        annotations = {}

    #        for model in DETOXIFY_MODELS:
    #            model_key = slugify(model).replace('-', '_')

    #        for model in properties[sentiment_key]:
    #            for label in properties[sentiment_key][model]:
    #                annotations[(model + '_' + label).lower()] = properties[sentiment_key][model][label]

    #        return annotations

    #    for key in properties:
    #        value = properties[key]

    #        if isinstance(value, dict):
    #            annotations = fetch_annotations(value, initial_field)

    #            if annotations is not None:
    #                return annotations

    #        elif isinstance(value, list):
    #            for item in value:
    #                annotations = fetch_annotations(item, initial_field)

    #                if annotations is not None:
    #                    return annotations

    return None
