# Coding Style

This document outlines the naming conventions and code patterns used in RDMO, as well as guidelines for the user interface. There may be cases where deviating from these conventions is necessary. In such cases, the reasoning should either be documented in a comment or be clear from the surrounding context of the code.

## Naming conventions

Consistent and descriptive naming is one of the key factors for readable and maintainable code. Giving good names to variables, functions, and classes not only makes the code easier to understand and debug, it also helps when reviewing code and onboarding new team members.

In general, we want to follow established naming conventions used in Django, Django Rest Framework (DRF), React, Redux and Bootstrap. In addition, please follow the guidelines below when naming new variables, functions or methods:

* The prefixes `set` and `get` should be used for functions which perform little to none operations.
* If functions access the network (e.g. in the front end) or the database, `fetch` and `store` are good prefixes.
* For more complex functions we use `compute` as prefix. An exception are well established Django/DRF patterns like `get_queryset`.
* The words `list`, `retrieve`, `create`, `update`, `delete` correspond to *actions* in DRF. The boolean `detail` describes whether the API works with one object or a list.
* The Django permission system uses `view`, `add`, `change`, `delete` to describe the operations it checks. The same words are used in the admin interface.
* The data model of RDMO introduces its own vocabulary, which can lead to confusion. Terms like `catalog`, `section`, `page`, `view`, `attribute`, or `value` should only be used when the context is clear.
* For function props, we use names like `onClick` and `onSubmit`. When handling events in the body of a component, we use functions like `handleClick` or `handleSubmit`.
* Custom hooks should be prefixed with `use`.
* In the front end, `location` describes the current URL visible to the user, usually in the form of a JavaScript state object containing the different parameters.

Please note [ARCHITECTURE.md](https://github.com/rdmorganiser/rdmo/blob/main/ARCHITECTURE.md) for the file naming conventions used in RDMO.

## Language-Specific Patterns

### Python and Django

For Python code, we use [ruff](https://github.com/astral-sh/ruff) as linter and formatter (as configured in `pyproject.toml`). Instead of the [black](https://github.com/psf/black)/[ruff format](https://docs.astral.sh/ruff/formatter/) defaults, we use a maximum line length of 120 characters and single quotes for strings. [Magic trailing commas](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html#the-magic-trailing-comma) can be used to enforce line breaks and to format lists and dicts in a consistent way.

Examples:

```python
# use parenthesis and indent nicely
last_changed_subquery = Subquery(
    Value.objects.filter(project=OuterRef('pk'))
    .order_by('-updated')
    .values('updated')[:1]
)

# multi line strings have the space at the end
Error(
    "When ACCOUNT_TERMS_OF_USE is enabled, "
    "The TermsAndConditionsRedirectMiddleware is missing from the middlewares.",
    ...,
)

# magic trailing commas prevent inlining of short dicts or lists
get_kwargs = {
    'attribute': data.get('attribute'),
    'set_prefix': data.get('set_prefix'),
    'set_index': data.get('set_index'),  # <- magic trailing comma
}
```

For constant iterables we use tuples `()` instead of lists `[]`.

In Python classes, we prefer `@property` instead of getter method (e.g. like `get_var(self)`).

RDMO uses [Django settings](https://docs.djangoproject.com/en/6.0/ref/settings/) extensively. All settings have a default value set in `rdmo/core/settings.py`. For readability, settings must not check if they exists (e.g. using `try/except` or `hasattr`).

Complex database requests can have a big impact on the performance of the application. Queries using multiple models / tables need to make use of [select_related](https://docs.djangoproject.com/en/stable/ref/models/querysets/#select-related) and [prefetch_related](https://docs.djangoproject.com/en/stable/ref/models/querysets/#prefetch-related). [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io) can be used to access database performance.

### JavaScript and React

In the JavaScript code, we use [ESlint](https://eslint.org). Like for the Python code, we use a maximum line length of 120 characters and single quotes for strings. Semicolons are omitted. Indentation uses 2 spaces, with switch case bodies indented one level inside the switch and the branches of ternary expressions indented when they wrap. Multiline ternaries must place each arm on its own line whenever the expression spans multiple lines.

In JSX, multiline expressions must be wrapped in parentheses with the opening parenthesis on a new line. Inside JSX curly braces, newlines are required when the expression is multiline, while single-line expressions must be spaced consistently within the same block. JSX attribute quotes use double quotes (e.g., `className="foo"`), as opposed to the single quotes used elsewhere in JS.

Examples:

```javascript
// conditional rendering
{
  attribute.id && (
    <div className="panel-body panel-border">
      {info}
    </div>
  )
}

// multiline ternary operators
{
  page.id ? (
    <>
      <strong>{gettext('Page')}{': '}</strong>
      <code className="code-questions">{page.uri}</code>
    </>
  ) : (
    <strong>{gettext('Create page')}</strong>
  )
}
```

We only use functional components and only one component should be in a single file.

## User interface considerations

All front end logic needs to be implemented with a consistent user experience in mind. Generic components reside in `rdmo/core/assets/js/components` and should be used where ever possible.

The styling should align with Bootstrap and it should be possible to adjust the visual style in a local theme using CSS variables alone and **without re-building the front end**.

Custom CSS code should be kept to a minimum. For CSS classes hyphens `-` should be used instead of underscores (`_`).

In the interactive front end, regular links (using the `a` tag) should only be used to navigate to a frontend location or a backend URL, which actually exists and which users might want to copy or bookmark. In all other cases, a `button` is preferred. The CSS class `link` can be used to make it look like a link. Usually `button` has `type="button"`, unless used as submit button in a form.

Form input fields should apply or save automatically. This save operation needs a visual indicator to communicate success to the user. An exception are fields in models, which are saved when the submit button of the modal is clicked.
