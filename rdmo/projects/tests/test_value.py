import datetime

from ..models import Value


def mocked_trans(self, field):
    return self.text_lang1


def test_value_text(db):
    value = Value.objects.get(id=1)
    assert value.value == value.text
    assert value.value_and_unit == value.text
    assert value.option_text is None
    assert value.option_additional_input is None


def test_value_textarea(db):
    value = Value.objects.get(id=2)
    assert value.value == value.text
    assert value.value_and_unit == value.text
    assert value.option_text is None
    assert value.option_additional_input is None


def test_value_bool(db):
    value = Value.objects.get(id=3)
    assert value.value == 'Yes'
    assert value.value_and_unit == 'Yes'
    assert value.option_text is None
    assert value.option_additional_input is None


def test_value_radio(db, mocker):
    mocker.patch('rdmo.options.models.Option.trans', mocked_trans)

    value = Value.objects.get(id=4)
    assert value.value == 'Other: Lorem ipsum'
    assert value.value_and_unit == 'Other: Lorem ipsum'
    assert value.option_text == 'Other'
    assert value.option_additional_input is True


def test_value_select(db, mocker):
    value = Value.objects.get(id=5)
    mocker.patch('rdmo.options.models.Option.trans', mocked_trans)
    assert value.value == 'One'
    assert value.value_and_unit == 'One'
    assert value.option_text == 'One'
    assert value.option_additional_input is False


def test_value_range(db):
    value = Value.objects.get(id=6)
    assert value.value == value.text
    assert value.value_and_unit == value.text
    assert value.option_text is None
    assert value.option_additional_input is None


def test_value_datetime(db):
    value = Value.objects.get(id=7)
    assert value.value == datetime.date(2018, 1, 1)
    assert value.value_and_unit == datetime.date(2018, 1, 1)
    assert value.option_text is None
    assert value.option_additional_input is None


def test_value_file(db):
    value = Value.objects.get(id=238)
    assert value.value == 'rdmo-logo.svg'
    assert value.value_and_unit == 'rdmo-logo.svg'
    assert value.option_text is None
    assert value.option_additional_input is None
