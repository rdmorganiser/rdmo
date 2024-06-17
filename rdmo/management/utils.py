
def replace_uri_in_template_string(template: str, source_uri: str, target_uri: str) -> str:
    patterns = [f"'{source_uri}'", f'"{source_uri}"']
    replacements = [f"'{target_uri}'", f'"{target_uri}"']

    new_template = template
    for pattern, replacement in zip(patterns, replacements):
        new_template = new_template.replace(pattern, replacement)
    return new_template
