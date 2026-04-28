import pytest

from django.utils import translation

from rdmo.core.models import TranslationMixin

test_languages = (
    ('en', 'title_lang1', 'text_lang1'),
    ('de', 'title_lang2', 'text_lang2')
)


class DummyTranslationModel(TranslationMixin):

    title_lang1 = 'title-1'
    title_lang2 = 'title-2'
    title_lang3 = 'title-3'

    text_lang1 = 'text-1'
    text_lang2 = 'text-2'
    text_lang3 = 'text-3'


@pytest.mark.parametrize('replace_missing_translation', [True, False])
@pytest.mark.parametrize('test_language,title_field,text_field', test_languages)
def test_translationmixin_trans(settings, replace_missing_translation, test_language, title_field, text_field):
    settings.REPLACE_MISSING_TRANSLATION = replace_missing_translation
    settings.LANGUAGE_CODE = test_language

    instance = DummyTranslationModel()
    # the active language should map directly to its
    # corresponding translated attribute.
    assert instance.trans('title') == getattr(instance, title_field)
    assert instance.trans('text') == getattr(instance, text_field)

@pytest.mark.parametrize('replace_missing_translation', [True, False])
@pytest.mark.parametrize('test_language,title_field,text_field', test_languages)
def test_translationmixin_trans_empty_field(settings, replace_missing_translation, test_language, title_field, text_field):  # noqa: E501
    settings.REPLACE_MISSING_TRANSLATION = replace_missing_translation
    empty_lang = 'en'

    settings.LANGUAGE_CODE = test_language
    instance = DummyTranslationModel()
    instance.title_lang1 = ''
    instance.text_lang1 = ''

    other_title_field = 'title_lang2' if test_language == 'en' else 'title_lang1'
    other_text_field = 'text_lang2' if test_language == 'en' else 'text_lang1'

    # An empty value in the active language only falls back to another
    # translation when replacement is enabled.
    if test_language == empty_lang and settings.REPLACE_MISSING_TRANSLATION:
        assert instance.trans('title') == getattr(instance, other_title_field)
        assert instance.trans('text') == getattr(instance, other_text_field)
    else:
        assert instance.trans('title') == getattr(instance, title_field)
        assert instance.trans('text') == getattr(instance, text_field)


def test_translationmixin_trans_region_language(settings):
    settings.REPLACE_MISSING_TRANSLATION = False

    instance = DummyTranslationModel()

    # Regional locales should still resolve to the configured base-language translation.
    with translation.override('en-us'):
        assert instance.trans('title') == instance.title_lang1
        assert instance.trans('text') == instance.text_lang1

    with translation.override('de-de'):
        assert instance.trans('title') == instance.title_lang2
        assert instance.trans('text') == instance.text_lang2


def test_translationmixin_trans_exact_locale_match(settings):
    settings.REPLACE_MISSING_TRANSLATION = False
    settings.LANGUAGES = (
        ('en', 'English'),
        ('en-GB', 'English (GB)'),
        ('de', 'German')
    )

    instance = DummyTranslationModel()

    # If a regional locale is configured explicitly,
    # it should have priority over the more general base-language.
    with translation.override('en-gb'):
        assert instance.trans('title') == instance.title_lang2
        assert instance.trans('text') == instance.text_lang2


def test_translationmixin_trans_uses_resolved_base_language(settings):
    settings.REPLACE_MISSING_TRANSLATION = False
    settings.LANGUAGES = (
        ('en', 'English'),
        ('de', 'German')
    )

    instance = DummyTranslationModel()

    # When the exact regional locale is not configured,
    # it falls back to the matching base language.
    with translation.override('de-at'):
        assert instance.trans('title') == instance.title_lang2
        assert instance.trans('text') == instance.text_lang2
