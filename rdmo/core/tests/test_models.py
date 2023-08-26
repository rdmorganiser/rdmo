import pytest

from rdmo.core.models import TranslationMixin

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


@pytest.mark.parametrize('replace_missing_translation', boolean_toggle)
@pytest.mark.parametrize('test_language', test_languages)
def test_translationmixin_trans(settings, replace_missing_translation, test_language):
    settings.REPLACE_MISSING_TRANSLATION = replace_missing_translation

    settings.LANGUAGE_CODE = test_language
    instance = TestTranslationModel()
    # trans should return the correct value
    assert instance.trans('title') == getattr(instance, test_lang_mapper[settings.LANGUAGE_CODE]['title'])
    assert instance.trans('text') == getattr(instance, test_lang_mapper[settings.LANGUAGE_CODE]['text'])
    del instance

@pytest.mark.parametrize('replace_missing_translation', boolean_toggle)
@pytest.mark.parametrize('test_language', test_languages)
def test_translationmixin_trans_empty_field(settings, replace_missing_translation, test_language):
    settings.REPLACE_MISSING_TRANSLATION = replace_missing_translation
    empty_lang = 'en'

    settings.LANGUAGE_CODE = test_language
    instance = TestTranslationModel()
    instance.title_lang1 = ''
    instance.text_lang1 = ''

    other_lang = 'de' if settings.LANGUAGE_CODE == 'en' else 'en'

    if settings.LANGUAGE_CODE == empty_lang and settings.REPLACE_MISSING_TRANSLATION:
        assert instance.trans('title') == getattr(instance, test_lang_mapper[other_lang]['title'])
        assert instance.trans('text') == getattr(instance, test_lang_mapper[other_lang]['text'])
    else:
        assert instance.trans('title') == getattr(instance, test_lang_mapper[settings.LANGUAGE_CODE]['title'])
        assert instance.trans('text') == getattr(instance, test_lang_mapper[settings.LANGUAGE_CODE]['text'])
    del instance
