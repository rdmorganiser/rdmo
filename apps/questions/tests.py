from django.test import TestCase

class QuestionsTestCase(TestCase):
    fixtures = ['accounts/testing.json', 'domain/testing.json', 'questions/testing.json']
