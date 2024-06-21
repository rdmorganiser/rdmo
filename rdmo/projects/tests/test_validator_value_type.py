import pytest

from rest_framework.exceptions import ValidationError as RestFameworkValidationError

from ..serializers.v1 import ValueSerializer
from ..validators import ValueTypeValidator

data = (
    ('url', 'https://exmaple.com'),
    ('url', 'http://exmaple.com'),
    ('integer', '1'),
    ('integer', '-1'),
    ('integer', '+1'),
    ('integer', '12345'),
    ('float', '1'),
    ('float', '1.0'),
    ('float', '+1.0'),
    ('float', '-1.0'),
    ('float', '1,000,000.12345'),
    ('float', '1,0'),
    ('float', '1.000.000,12345'),
    ('float', '1.0e20'),
    ('float', '1.0E20'),
    ('float', '1.0e-20'),
    ('float', '1.0e+20'),
    ('boolean', '0'),
    ('boolean', '1'),
    ('boolean', 'f'),
    ('boolean', 't'),
    ('boolean', 'TrUe'),
    ('boolean', 'FaLsE'),
    ('date', '01.02.2024'),
    ('date', '1.2.2024'),
    ('date', '13.01.1337'),
    ('date', '2/1/2024'),
    ('date', '2024-01-02'),
    ('date', '1. 2. 2024'),
    ('datetime', '2024-01-02'),
    ('datetime', '2024-01-02T10:00'),
    ('datetime', '2024-01-02T10:00:00'),
    ('datetime', '2024-01-02T10:00:00.123'),
    ('datetime', '2024-01-02T10:00:00+02:00'),
    ('datetime', '2024-01-02T10:00:00Z+02:00'),
    ('email', 'user@example.com'),
    ('email', 'user+test@example.com'),
    ('email', 'user!test@example.com'),
    ('phone', '123456'),
    ('phone', '123 456'),
    ('phone', '362 123456'),
    ('phone', '(362) 123456'),
    ('phone', '+49 (0) 362123456'),
    ('phone', '+49 (0) 362 123456'),
)
data_error = (
    ('url', 'wrong'),
    ('url', 'exmaple.com'),
    ('integer', 'wrong'),
    ('integer', '1.0'),
    ('integer', '1b'),
    ('float', 'wrong'),
    ('float', '1,0000.12456'),
    ('float', '1.0000,12456'),
    ('float', '1.0a20'),
    ('boolean', 'wrong'),
    ('boolean', '2'),
    ('boolean', '-1'),
    ('boolean', 'tr'),
    ('date', 'wrong'),
    ('date', '001.02.2024'),
    ('date', '01.02.20240'),
    ('date', '1,2.2024'),
    ('date', '2-1-2024'),
    ('date', '2024-001-02'),
    ('date', '20240-01-02'),
    ('date', '2024-1-2'),
    ('datetime', 'wrong'),
    ('datetime', '2024-13-02'),
    ('datetime', '2024-13-02Y10:00:00'),
    ('datetime', '2024-01-02T10:00:00ZZ+02:00'),
    ('email', 'wrong'),
    ('email', 'example.com'),
    ('email', 'üser@example.com'),
    ('email', 'user@test@example.com'),
    ('phone', 'wrong'),
    ('phone', '123456a'),
    ('phone', '123 456 a'),
    ('phone', '362s 123456'),
    ('phone', '(3 62) 123456'),
    ('phone', '-49 (0) 362123456'),
    ('phone', '49 (0) 362 123456'),
    ('phone', '1234 (0) 123456'),
)


@pytest.mark.parametrize('value_type,text', data)
def test_serializer(db, value_type, text):
    validator = ValueTypeValidator()
    serializer = ValueSerializer()

    validator({'value_type': value_type, 'text': text}, serializer)


@pytest.mark.parametrize('value_type,text', data_error)
def test_serializer_error(db, value_type, text):
    validator = ValueTypeValidator()
    serializer = ValueSerializer()

    with pytest.raises(RestFameworkValidationError):
        validator({'value_type': value_type, 'text': text}, serializer)
