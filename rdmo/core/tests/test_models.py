import pytest

from django.utils.translation import get_language

from rdmo.core.models import TranslationMixin
from rdmo.core.utils import get_languages

boolean_toggle = (True, False)
test_languages = ('en', 'de')

test_lang_mapper = {
    'en': {
        'title': 'title_lang1',
        'text': 'text_lang1'
    },
    'de': {
        'title': 'title_lang2',
        'text': 'text_lang2'
    }
}

class TestTranslationModel(TranslationMixin):
    
    title_lang1 = 'title-1'
    title_lang2 = 'title-2'

    text_lang1 = 'text-1'
    text_lang2 = 'text-2'



@pytest.mark.parametrize('test_setting', boolean_toggle)
@pytest.mark.parametrize('test_lang', test_languages)
def test_translationmixin_trans(settings, test_setting, test_lang):
    settings.REPLACE_MISSING_TRANSLATION = test_setting

    settings.LANGUAGE_CODE = test_lang
    instance = TestTranslationModel()
    # trans should return the correct value
    assert instance.trans('title') == getattr(instance, test_lang_mapper[test_lang]['title'])
    assert instance.trans('text') == getattr(instance, test_lang_mapper[test_lang]['text'])
    del instance

@pytest.mark.parametrize('test_setting', boolean_toggle)
@pytest.mark.parametrize('test_lang', test_languages)
def test_translationmixin_trans_empty_field(settings, test_setting, test_lang):
    settings.REPLACE_MISSING_TRANSLATION = test_setting
    empty_lang = 'en'

    settings.LANGUAGE_CODE = test_lang
    instance = TestTranslationModel()
    instance.title_lang1 = ''
    instance.text_lang1 = ''

    other_lang = 'de' if test_lang == 'en' else 'en'

    if test_lang == empty_lang and settings.REPLACE_MISSING_TRANSLATION:
        assert instance.trans('title') == getattr(instance, test_lang_mapper[other_lang]['title'])
        assert instance.trans('text') == getattr(instance, test_lang_mapper[other_lang]['text'])
    else:
        assert instance.trans('title') == getattr(instance, test_lang_mapper[test_lang]['title'])
        assert instance.trans('text') == getattr(instance, test_lang_mapper[test_lang]['text'])
    del instance
