from rdmo.domain.models import Attribute


def replace_uri_in_template_string(template: str, source: Attribute, target: Attribute) -> str:
    new_lines = []
    path_changed = source.path != target.path
    for line in template.splitlines():
        new_line = line
        if source.uri in line:
            new_line = new_line.replace(source.uri, target.uri)
        if path_changed:
            if source.path in new_line:
                new_line = new_line.replace(source.path, target.path)
        new_lines.append(new_line)
    new_template = "\n".join(new_lines)
    return new_template
