
def replace_uri_in_template_string(template: str, source_uri: str, target_uri: str) -> str:
    replacements = [
        (f"'{source_uri}'", f"'{target_uri}'"),
        (f'"{source_uri}"', f'"{target_uri}"'),
    ]
    for pattern, replacement in replacements:
        template = template.replace(pattern, replacement)
    return template
