import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    created = "2016-03-14T13:37:00Z"
    updated = "2016-03-14T13:37:00Z"

    help_text = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est. Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est. Lorem ipsum dolor sit amet.'

    options = {
        'a': 'a',
        'b': 'b',
        'c': 'c',
        'd': 'd',
        'e': 'e'
    }

    range_options = {
        'minimum': 0,
        'maximum': 1000,
        'step': 10
    }

    # pk, name, is_collection, parent_pk, value_type
    # pk, name, is_collection, parent_pk
    models = (
        (1001, 'text', 0, None, None, 'text', 'text'),
        (1002, 'textarea', 0, None, None, 'text', 'textarea'),
        (1003, 'yesno', 0, None, None, 'boolean', 'yesno'),
        (1004, 'date', 0, None, None, 'date', 'date'),
        (1005, 'range', 0, None, None, 'float', 'range'),
        (1006, 'radio', 0, None, None, 'options', 'radio'),
        (1007, 'select', 0, None, None, 'options', 'select'),
        (1008, 'checkbox', 0, None, None, 'options', 'checkbox'),

        (1010, 'collection', 0, None, False),

        (1011, 'collection.text', 1, 1010, None, 'text', 'text'),
        (1012, 'collection.textarea', 1, 1010, None, 'text', 'textarea'),
        (1013, 'collection.yesno', 1, 1010, None, 'boolean', 'yesno'),
        (1014, 'collection.date', 1, 1010, None, 'date', 'date'),
        (1015, 'collection.range', 1, 1010, None, 'float', 'range'),
        (1016, 'collection.radio', 1, 1010, None, 'options', 'radio'),
        (1017, 'collection.select', 1, 1010, None, 'options', 'select'),
        (1018, 'collection.checkbox', 1, 1010, None, 'options', 'checkbox'),

        (1100, 'set', 0, None, True),

        (1101, 'set.text', 0, 1100, 1100, 'text', 'text'),
        (1102, 'set.textarea', 0, 1100, 1100, 'text', 'textarea'),
        (1103, 'set.yesno', 0, 1100, 1100, 'boolean', 'yesno'),
        (1104, 'set.date', 0, 1100, 1100, 'date', 'date'),
        (1105, 'set.range', 0, 1100, 1100, 'float', 'range'),
        (1106, 'set.radio', 0, 1100, 1100, 'options', 'radio'),
        (1107, 'set.select', 0, 1100, 1100, 'options', 'select'),
        (1108, 'set.checkbox', 0, 1100, 1100, 'options', 'checkbox'),

        (1110, 'set.collection', 0, 1100, False),

        (1111, 'set.collection.text', 1, 1110, 1100, 'text', 'text'),
        (1112, 'set.collection.textarea', 1, 1110, 1100, 'text', 'textarea'),
        (1113, 'set.collection.yesno', 1, 1110, 1100, 'boolean', 'yesno'),
        (1114, 'set.collection.date', 1, 1110, 1100, 'date', 'date'),
        (1115, 'set.collection.range', 1, 1110, 1100, 'float', 'range'),
        (1116, 'set.collection.radio', 1, 1110, 1100, 'options', 'radio'),
        (1117, 'set.collection.select', 1, 1110, 1100, 'options', 'select'),
        (1118, 'set.collection.checkbox', 1, 1110, 1100, 'options', 'checkbox'),

        (1200, 'collection_set', 1, None, True),

        (1201, 'collection_set.text', 0, 1200, 1200, 'text', 'text'),
        (1202, 'collection_set.textarea', 0, 1200, 1200, 'text', 'textarea'),
        (1203, 'collection_set.yesno', 0, 1200, 1200, 'boolean', 'yesno'),
        (1204, 'collection_set.date', 0, 1200, 1200, 'date', 'date'),
        (1205, 'collection_set.range', 0, 1200, 1200, 'float', 'range'),
        (1206, 'collection_set.radio', 0, 1200, 1200, 'options', 'radio'),
        (1207, 'collection_set.select', 0, 1200, 1200, 'options', 'select'),
        (1208, 'collection_set.checkbox', 0, 1200, 1200, 'options', 'checkbox'),

        (1210, 'collection_set.collection', 0, 1200, False),

        (1211, 'collection_set.collection.text', 1, 1210, 1200, 'text', 'text'),
        (1212, 'collection_set.collection.textarea', 1, 1210, 1200, 'text', 'textarea'),
        (1213, 'collection_set.collection.yesno', 1, 1210, 1200, 'boolean', 'yesno'),
        (1214, 'collection_set.collection.date', 1, 1210, 1200, 'date', 'date'),
        (1215, 'collection_set.collection.range', 1, 1210, 1200, 'float', 'range'),
        (1216, 'collection_set.collection.radio', 1, 1210, 1200, 'options', 'radio'),
        (1217, 'collection_set.collection.select', 1, 1210, 1200, 'options', 'select'),
        (1218, 'collection_set.collection.checkbox', 1, 1210, 1200, 'options', 'checkbox'),
    )

    def handle(self, *args, **options):

        domain = []
        questions = [
            {
                "model": "questions.catalog",
                "pk": 1000,
                "fields": {
                    "order": 1,
                    "title_en": "catalog_en",
                    "title_de": "catalog_de",
                    "created": self.created,
                    "updated": self.updated
                }
            },
            {
                "model": "questions.section",
                "pk": 1000,
                "fields": {
                    "catalog": 1000,
                    "order": 1,
                    "title_en": "section_en",
                    "title_de": "section_de",
                    "created": self.created,
                    "updated": self.updated
                }
            },
            {
                "model": "questions.subsection",
                "pk": 1000,
                "fields": {
                    "section": 1000,
                    "order": 1,
                    "title_en": "subsection_en",
                    "title_de": "subsection_de",
                    "created": self.created,
                    "updated": self.updated
                }
            }
        ]

        for model in self.models:
            try:
                pk, full_title, is_collection, parent_attribute_pk, parent_question_pk, value_type, widget_type = model
                create_question_entity = True
            except ValueError:
                pk, full_title, is_collection, parent_attribute_pk, create_question_entity = model
                parent_question_pk = None
                value_type = False
                widget_type = False

            name = full_title.split('.')[-1]

            domain.append({
                "model": "domain.attributeentity",
                "pk": pk,
                "fields": {
                    'parent_entity': parent_attribute_pk,
                    'title': name,
                    'full_title': full_title,
                    'is_collection': is_collection,
                }
            })

            if value_type:
                domain.append({
                    "model": "domain.attribute",
                    "pk": pk,
                    "fields": {
                        'value_type': value_type,
                        'unit': None
                    }
                })

                if value_type == 'options':
                    for i, key in enumerate(self.options):
                        try:
                            text_en = self.options[key] + '_en'
                            text_de = self.options[key] + '_de'
                        except TypeError:
                            text_en = self.options[key]
                            text_de = self.options[key]

                        domain.append({
                            "model": "domain.option",
                            "pk": i * 10000 + pk,
                            "fields": {
                                "attribute": pk,
                                "order": i,
                                "text_en": text_en,
                                "text_de": text_de,
                                "additional_input": False
                            }
                        })

                    domain.append({
                        "model": "domain.option",
                        "pk": 100000 + pk,
                        "fields": {
                            "attribute": pk,
                            "order": 100,
                            "text_en": 'other_en',
                            "text_de": 'other_de',
                            "additional_input": True
                        }
                    })

                if widget_type and widget_type == 'range':
                    domain.append({
                        "model": "domain.range",
                        "pk": pk,
                        "fields": {
                            'attribute': pk,
                            "minimum": self.range_options['minimum'],
                            "maximum": self.range_options['maximum'],
                            "step": self.range_options['step']
                        }
                    })

            if create_question_entity:
                questions.append({
                    "model": "questions.questionentity",
                    "pk": pk,
                    "fields": {
                        "attribute_entity": pk,
                        "subsection": 1000,
                        "order": pk,
                        "help_en": self.help_text,
                        "help_de": self.help_text,
                        "created": self.created,
                        "updated": self.updated
                        }
                })

                if widget_type:
                    questions.append({
                        "model": "questions.question",
                        "pk": pk,
                        "fields": {
                            "parent_entity": parent_question_pk,
                            "text_en": full_title.capitalize().replace('_', ' ') + ' en?',
                            "text_de": full_title.capitalize().replace('_', ' ') + ' de?',
                            "widget_type": widget_type
                        }
                    })



        domain_file = os.path.join(settings.BASE_DIR, 'apps/domain/fixtures/domain/testing.json')
        questions_file = os.path.join(settings.BASE_DIR, 'apps/questions/fixtures/questions/testing.json')

        open(domain_file, 'w').write(json.dumps(domain))
        open(questions_file, 'w').write(json.dumps(questions))
