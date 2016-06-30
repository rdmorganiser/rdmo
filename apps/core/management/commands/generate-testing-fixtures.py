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
        'min': 0,
        'max': 1000
    }

    # pk, name, is_collection, attributeset, widget_type, value_type
    # pk, name, is_collection
    models = (
        (1001, 'text', 0, None, 'text', 'text', False),
        (1002, 'textarea', 0, None, 'textarea', 'text', False),
        (1003, 'yesno', 0, None, 'yesno', 'boolean', False),
        (1004, 'date', 0, None, 'date', 'text', False),
        (1005, 'range', 0, None, 'range', 'integer', range_options),
        (1006, 'radio', 0, None, 'radio', 'text', options),
        (1007, 'select', 0, None, 'select', 'text', options),
        (1008, 'checkbox', 0, None, 'checkbox', 'text', options),

        (1011, 'text_collection', 1, None, 'text', 'text', False),
        (1012, 'textarea_collection', 1, None, 'textarea', 'text', False),
        (1013, 'yesno_collection', 1, None, 'yesno', 'boolean', False),
        (1014, 'date_collection', 1, None, 'date', 'text', False),
        (1015, 'range_collection', 1, None, 'range', 'integer', range_options),
        (1016, 'radio_collection', 1, None, 'radio', 'text', options),
        (1017, 'select_collection', 1, None, 'select', 'text', options),
        (1018, 'checkbox_collection', 1, None, 'checkbox', 'text', options),

        (1100, 'set', 0),

        (1101, 'set_text', 0, 1100, 'text', 'text', False),
        (1102, 'set_textarea', 0, 1100, 'textarea', 'text', False),
        (1103, 'set_yesno', 0, 1100, 'yesno', 'boolean', False),
        (1104, 'set_date', 0, 1100, 'date', 'text', False),
        (1105, 'set_range', 0, 1100, 'range', 'integer', range_options),
        (1106, 'set_radio', 0, 1100, 'radio', 'text', options),
        (1107, 'set_select', 0, 1100, 'select', 'text', options),
        (1108, 'set_checkbox', 0, 1100, 'checkbox', 'text', options),

        (1111, 'set_text_collection', 1, 1100, 'text', 'text', False),
        (1112, 'set_textarea_collection', 1, 1100, 'textarea', 'text', False),
        (1113, 'set_yesno_collection', 1, 1100, 'yesno', 'boolean', False),
        (1114, 'set_date_collection', 1, 1100, 'date', 'text', False),
        (1115, 'set_range_collection', 1, 1100, 'range', 'integer', range_options),
        (1116, 'set_radio_collection', 1, 1100, 'radio', 'text', options),
        (1117, 'set_select_collection', 1, 1100, 'select', 'text', options),
        (1118, 'set_checkbox_collection', 1, 1100, 'checkbox', 'text', options),

        (1200, 'set_collection', 1),

        (1201, 'set_collection_text', 0, 1200, 'text', 'text', False),
        (1202, 'set_collection_textarea', 0, 1200, 'textarea', 'text', False),
        (1203, 'set_collection_yesno', 0, 1200, 'yesno', 'boolean', False),
        (1204, 'set_collection_date', 0, 1200, 'date', 'text', False),
        (1205, 'set_collection_range', 0, 1200, 'range', 'integer', range_options),
        (1206, 'set_collection_radio', 0, 1200, 'radio', 'text', options),
        (1207, 'set_collection_select', 0, 1200, 'select', 'text', options),
        (1208, 'set_collection_checkbox', 0, 1200, 'checkbox', 'text', options),

        (1211, 'set_collection_text_collection', 1, 1200, 'text', 'text', False),
        (1212, 'set_collection_textarea_collection', 1, 1200, 'textarea', 'text', False),
        (1213, 'set_collection_yesno_collection', 1, 1200, 'yesno', 'boolean', False),
        (1214, 'set_collection_date_collection', 1, 1200, 'date', 'text', False),
        (1215, 'set_collection_range_collection', 1, 1200, 'range', 'integer', range_options),
        (1216, 'set_collection_radio_collection', 1, 1200, 'radio', 'text', options),
        (1217, 'set_collection_select_collection', 1, 1200, 'select', 'text', options),
        (1218, 'set_collection_checkbox_collection', 1, 1200, 'checkbox', 'text', options),
    )

    def handle(self, *args, **options):

        domain = []
        questions = [
            {
                "model": "questions.catalog",
                "pk": 1000,
                "fields": {
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

            if len(model) == 3:
                pk, name, is_collection = model

                domain.append({
                    "model": "domain.attributeentity",
                    "pk": pk,
                    "fields": {
                        "tag": name,
                        "is_collection": is_collection,
                        "created": self.created,
                        "updated": self.updated
                    }
                })
                domain.append({
                    "model": "domain.attributeset",
                    "pk": pk,
                    "fields": {}
                })
                questions.append({
                    "model": "questions.questionentity",
                    "pk": pk,
                    "fields": {
                        "subsection": 1000,
                        "order": pk,
                        "title_en": name + "_en",
                        "title_de": name + "_de",
                        "help_en": self.help_text,
                        "help_de": self.help_text,
                        "created": self.created,
                        "updated": self.updated
                    }
                })
                questions.append({
                    "model": "questions.questionset",
                    "pk": pk,
                    "fields": {
                        "attributeset": pk
                    }
                })

            else:
                pk, name, is_collection, attributeset, widget_type, value_type, options = model

                domain.append({
                    "model": "domain.attributeentity",
                    "pk": pk,
                    "fields": {
                        "tag": name,
                        "is_collection": is_collection,
                        "created": self.created,
                        "updated": self.updated
                    }
                })
                domain.append({
                    "model": "domain.attribute",
                    "pk": pk,
                    "fields": {
                        "attributeset": attributeset,
                        "value_type": value_type,
                        "unit": None
                    }
                })
                questions.append({
                    "model": "questions.questionentity",
                    "pk": pk,
                    "fields": {
                        "subsection": 1000,
                        "order": pk,
                        "title_en": name + '_en',
                        "title_de": name + '_de',
                        "help_en": self.help_text,
                        "help_de": self.help_text,
                        "created": self.created,
                        "updated": self.updated
                        }
                })
                questions.append({
                    "model": "questions.question",
                    "pk": pk,
                    "fields": {
                        "questionset": attributeset,
                        "attribute": pk,
                        "text_en": name.capitalize().replace('_', ' ') + ' en?',
                        "text_de": name.capitalize().replace('_', ' ') + ' de?',
                        "widget_type": widget_type
                    }
                })

                if options:
                    for i, key in enumerate(options):
                        try:
                            text_en = options[key] + '_en'
                            text_de = options[key] + '_de'
                        except TypeError:
                            text_en = options[key]
                            text_de = options[key]

                        questions.append({
                            "model": "questions.option",
                            "pk": i * 10000 + pk,
                            "fields": {
                                "question": pk,
                                "order": i,
                                "key": key,
                                "text_en": text_en,
                                "text_de": text_de,
                                "input_field": False
                            }
                        })

                    questions.append({
                        "model": "questions.option",
                        "pk": 100000 + pk,
                        "fields": {
                            "question": pk,
                            "order": 100,
                            "key": 'other',
                            "text_en": 'other_en',
                            "text_de": 'other_de',
                            "input_field": True
                        }
                    })

        domain_file = os.path.join(settings.BASE_DIR, 'apps/domain/fixtures/domain/testing.json')
        questions_file = os.path.join(settings.BASE_DIR, 'apps/questions/fixtures/questions/testing.json')

        open(domain_file, 'w').write(json.dumps(domain))
        open(questions_file, 'w').write(json.dumps(questions))
