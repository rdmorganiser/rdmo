from ..models import Option, OptionSet, OptionSetOption

URI_PREFIX = 'https://example.com/terms'


def create_options(count, uri_path):
    paths = [f'{uri_path}-{index:04d}' for index in range(count)]
    Option.objects.bulk_create([
        Option(uri=Option.build_uri(URI_PREFIX, path), uri_prefix=URI_PREFIX, uri_path=path,
               text_lang1=f'Option {path}')
        for path in paths
    ])
    # Re-fetch primary keys because bulk_create does not populate them on every database backend.
    options = list(Option.objects.filter(
        uri_prefix=URI_PREFIX, uri_path__startswith=f'{uri_path}-'
    ).order_by('uri_path'))
    assert len(options) == count
    return options


def create_optionset(uri_path, options):
    optionset = OptionSet.objects.create(uri_prefix=URI_PREFIX, uri_path=uri_path)
    OptionSetOption.objects.bulk_create([
        OptionSetOption(optionset=optionset, option=option, order=order)
        for order, option in enumerate(options)
    ])
    return optionset
