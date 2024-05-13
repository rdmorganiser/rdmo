from rdmo.domain.models import Attribute


def replace_uri_in_template_string(template: str, source: Attribute, target: Attribute) -> str:
    result = []
    path_changed = source.path != target.path
    for n, line in enumerate(template.splitlines()):
        new_line = line
        if source.uri in line:
            new_line = new_line.replace(source.uri, target.uri)
        if path_changed:
            if source.path in new_line:
                new_line = new_line.replace(source.path, target.path)
        line_result = {
            'line_no': n,
            'new_line': new_line,
            'original_line': line
            }
        result.append(line_result)
    new_template = "\n".join(i['new_line'] for i in result)
    return new_template
