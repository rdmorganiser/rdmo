# Coding Style

This document outlines the naming conventions and code patterns used in RDMO, as well as guidelines for the user interface. There may be cases where deviating from these conventions is necessary. In such cases, the reasoning should either be documented in a comment or be clear from the surrounding context of the code.

## Naming conventions

Consistent and descriptive naming is one of the key factors for readable and maintainable code. Giving good names to variables, functions, and classes not only makes the code easier to understand and debug, it also helps when reviewing code and onboarding new team members.

In general, we want to follow established naming conventions used in [Django](https://www.djangoproject.com), [Django Rest Framework](https://www.django-rest-framework.org) (DRF), [React](https://react.dev) and [Bootstrap](https://getbootstrap.com). In addition, please follow the guidelines below when naming new variables, functions or methods:

* The prefixes `set` and `get` should be used for functions which perform little to none operations. In Python classes, we prefer `@property` instead of `get_egg(self)`. For more complex functions we use `compute` as prefix. An exception are well established Django/DRF patterns like `get_queryset`.
* If functions access the network (e.g. in the front end) or the database, `fetch` and `store` are good prefixes.
* The words `list`, `retrieve`, `create`, `update`, `delete` correspond to *actions* in DRF. The boolean `detail` describes whether the API works with one object or a list.
* The Django permission system uses `view`, `add`, `change`, `delete` to describe the operations it checks. The same words are used in the admin interface.
* The data model of RDMO introduces its own vocabulary, which can lead to confusion. Terms like `catalog`, `section`, `page`, `view`, `attribute`, or `value` should only be used when the context is clear.
* For function props, we use names like `onClick` and `onSubmit`. When handling events in the body of a component, we use functions like `handleClick` or `handleSubmit`.
* Custom hooks should be prefixed with `use`.
* In the front end, `location` describes the current URL visible to the user, usually in the form of a JavaScript state object containing the different parameters.

Please note [ARCHITECTURE.md](https://github.com/rdmorganiser/rdmo/blob/main/ARCHITECTURE.md) for the file naming conventions used in RDMO.

## Language-Specific Patterns

### Python and Django

For Python code, we use [ruff](https://github.com/astral-sh/ruff) as linter (as configured in `pyproject.toml`) and follow its suggestions. Unlike many Python projects, we do not enforce [black](https://github.com/psf/black) or [ruff format](https://github.com/astral-sh/ruff). Contributors are trusted to follow the style guidelines without automated formatting.

The maximum line length is 120 characters. When breaking longer statements, we avoid `\`. We use **single quotes for strings**. Double-quotes are used in favor of escaping quotes in strings or when using dicts in f-strings. For constant iterables we use tuples `()` instead of lists `[]`.

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
    ...
)

# we prefer line breaks after { or [
get_kwargs = {
    'attribute': data.get('attribute'),
    'set_prefix': data.get('set_prefix'),
    'set_index': data.get('set_index')
}
```

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

// multiline tertiary operators
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

## UI/UI considerations

All front end logic needs to be implemented with a consistent user experience in mind. Generic components reside in `rdmo/core/assets/js/components` and should be used where ever possible.

The styling should align with Bootstrap and it should be possible to adjust the visual style in a local theme using CSS variables alone and **without re-building the front end**.

Custom CSS code should be kept to a minimum. For CSS classes hyphens `-` should be used instead of underscores (`_`).

In the interactive front end, `a` should be used when there is a front end route or a backend URL which users might want to copy or bookmark. In all other cases, a `button` is preferred. The CSS class `link` can be used to make it look like a link. Usually `button` has `type="button"`, unless used as submit button in a form.

Form input fields should should apply or save automatically. This save operation needs a visual indicator to communicate success to the user. An exception are fields in models modals are only saved on the submit button of the modal.
