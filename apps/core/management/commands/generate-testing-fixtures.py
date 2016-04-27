import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    created = "2016-03-14T13:37:00Z"
    updated = "2016-03-14T13:37:00Z"

    help_text = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est. Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est. Lorem ipsum dolor sit amet.'

    # pk, name, is_collection, attributeset, widget_type, value_type
    # pk, name, is_collection
    models = (
        (1001, 'text', 0, None, 'text', 'text'),
        (1002, 'textarea', 0, None, 'textarea', 'text'),
        (1003, 'yesno', 0, None, 'yesno', 'boolean'),

        (1011, 'text_collection', 1, None, 'text', 'text'),
        (1012, 'textarea_collection', 1, None, 'textarea', 'text'),
        (1013, 'yesno_collection', 1, None, 'yesno', 'boolean'),

        (1100, 'set', 0),

        (1101, 'set_text', 0, 1100, 'text', 'text'),
        (1102, 'set_textarea', 0, 1100, 'textarea', 'text'),
        (1103, 'set_yesno', 0, 1100, 'yesno', 'boolean'),

        (1111, 'set_text_collection', 1, 1100, 'text', 'text'),
        (1112, 'set_textarea_collection', 1, 1100, 'textarea', 'text'),
        (1113, 'set_yesno_collection', 1, 1100, 'yesno', 'boolean'),

        (1200, 'set_collection', 1),

        (1201, 'set_collection_text', 0, 1200, 'text', 'text'),
        (1202, 'set_collection_textarea', 0, 1200, 'textarea', 'text'),
        (1203, 'set_collection_yesno', 0, 1200, 'yesno', 'boolean'),

        (1211, 'set_collection_text_collection', 1, 1200, 'text', 'text'),
        (1212, 'set_collection_textarea_collection', 1, 1200, 'textarea', 'text'),
        (1213, 'set_collection_yesno_collection', 1, 1200, 'yesno', 'boolean'),
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
                pk, name, is_collection, attributeset, widget_type, value_type = model

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

        domain_file = os.path.join(settings.BASE_DIR, 'apps/domain/fixtures/domain/testing.json')
        questions_file = os.path.join(settings.BASE_DIR, 'apps/questions/fixtures/questions/testing.json')

        open(domain_file, 'w').write(json.dumps(domain))
        open(questions_file, 'w').write(json.dumps(questions))
