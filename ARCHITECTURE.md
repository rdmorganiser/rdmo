# Architecture

This document provides an overview over the architecture of RDMO and provides information about the different modules.

## Core dependencies

RDMO is a [Django](https://www.djangoproject.com/) application with an integrated [React](https://react.dev/) frontend.

On the backend, it makes heavy use of:

* [Django Rest Framework](https://www.django-rest-framework.org/) (DRF) for the REST API,
* [rules](https://github.com/dfunckt/django-rules) for object based permissions.

The frontend code relies on:

* [webpack](https://webpack.js.org) for bundling,
* [Redux](https://redux.js.org/) for state management,
* [Redux Thunk](https://github.com/reduxjs/redux-thunk) for asynchronous Redux actions,
* [Bootstrap](https://getbootstrap.com/) as CSS framework,
* [lodash](https://lodash.com/) for various utilities.

Testing is done with:

* [pytest](https://docs.pytest.org) for the backend,
* [Playwright](https://playwright.dev) for the frontend.

## File layout

The main `rdmo` package consists of the following modules:

```
rdmo/
├── core/              ← Core functionality
├── accounts/          ← Authentication & user profiles
├── domain/            ← Domain model
├── questions/         ← Structure of the questionnaire
├── conditions/        ← Conditional display of questions or answers
├── options/           ← Controlled vocabularies for answers
├── tasks/             ← Follow up actions based on answers
├── views/             ← Templating for output and export
├── projects/          ← User projects, snapshots and answers
├── management/        ← Management editing backend
└── services/          ← OAuth / external integrations
```

Each module (an *app* in Django terms) tries to follow the conventional layout and naming conventions:

* `admin.py` → Django admin interface configuration
* `apps.py` → Django app configuration
* `assets/` → Source files for the frontend (JavaScript, CSS, ...)
* `constants.py` → Definition of constant values
* `exports.py` → Export plugin functionality
* `filters.py` → Filters for DRF viewsets
* `forms.py` → Django forms
* `handlers/` or `handlers.py` → Handlers for Django signals
* `imports.py` → Helper functionality for the XML import
* `managers.py` → Managers for Django models
* `migrations/` → Django database migrations
* `mixins.py` → Mixins for different classes
* `models/` or `models.py` → Django database models
* `permissions.py` → DRF permission classes
* `providers.py` → Optionset provider plugins
* `renderers/` or `renderers.py` → Render functionality for the XML export
* `rules.py` → Object based permissions
* `serializers/` or `serializers.py` → DRF serializers
* `signals.py` → Signals for Django signals
* `static/` → Build front end assets, ignored by Git
* `templates/` → Django templates
* `templatetags/` → Django template tags and filters
* `tests/` → Tests
* `urls/` or `urls.py` → Django URL mapping
* `utils.py` → Utility functions
* `validators.py` → Additional validators for DRF
* `views/` or `views.py` → Django views
* `viewsets.py` → DRF viewsets for the REST API

In addition, the `rdmo` repository contains the following notable files or directories:

* `pyproject.toml` → Python package configuration
* `rdmo/locale` → Translation files
* `rdmo/share` → Supplemental files
* `testing` → Test configuration & fixtures
* `conftest.py` → pytest setup
* `webpack.config.js` → Frontend build configuration
* `package.json` and `package-lock.json` → Frontend dependencies

The `assets` directories in the modules use the following structure:

* `assets/js/` → JavaScript front-end code, separated by React app
    * `actions/` → Actions for the Redux store
    * `api/` → API classes with methods mapping the endpoints of the REST API
    * `components/` → React components
    * `factories/` → Factory functions for front end objects
    * `hooks/` → React hooks
    * `reducers/` → Reducers for the Redux store
    * `store/` → Configuration and initialization of the Redux store
    * `utils/` → Utility functions
* `assets/scss/` → Sass files, separated by React app
* `assets/fonts/`, `assets/img/` → Additional, static assets

## Internal dependencies

```plain
┌────────────┐         ┌────────────┐
│ core       │◀───┬────┤ accounts   │
└────────────┘    │    └────────────┘
                  │    ┌────────────┐         ┌────────────┐
                  ├────┤ domain     │◀───┬────┤ projects   │
                  │    └────────────┘    │    └────────────┘
                  │    ┌────────────┐    │    ┌────────────┐
                  ├────┤ conditions │◀───┼────┤ management │
                  │    └────────────┘    │    └────────────┘
                  │    ┌────────────┐    │
                  ├────┤ options    │◀───┤
                  │    └────────────┘    │
                  │    ┌────────────┐    │
                  ├────┤ questions  │◀───┤
                  │    └────────────┘    │
                  │    ┌────────────┐    │
                  ├────┤ tasks      │◀───┤
                  │    └────────────┘    │
                  │    ┌────────────┐    │
                  └────┤ views      │◀───┘
                       └────────────┘
```

The modules depend on each other in the following way:

* `core` does not depend on the other modules.
* `accounts` does only depend on `core`.
* `conditions`, `domain`, `options`, `questions`, `tasks`, `views` depend only on `core` (with the exception that the `options.Optionset` model and the `conditions.Condition` depend on each other).
* `project` and `management` depend on `conditions`, `domain`, `options`, `questions`, `tasks`, `views` and `core`.

Besides those dependencies:

* `utils.py` and `managers.py` must not depend on anything inside the module.
* `models.py` must only depend on `utils.py` and `managers.py`.

If utility functions, which depend on the models are needed, they are put in special files, e.g. `process.py`. Utility functions for tests are placed in `tests/helpers.py`.

Only after careful consideration, functions can use local imports (in the function body) to circumvent the described dependency rules.

## Backend considerations

RDMO tries to follow the conventional style of Django projects. It should work with all database backends and with all common web server setups. The aim is to limit the dependencies and the effort to maintain an instance to a minimum. For the same reason, RDMO does not depend on a caching solution or an infrastructure for asynchronous tasks.

While some parts of RDMO use the common Django MVC-pattern using models, (class-based) views and templates, other parts use the Django Rest Service pattern using viewsets, serializers and renderers. The latter is used by the interactive frontend (see below), but also as scriptable API.

## Frontend considerations

As already mentioned, major parts of RDMO are implemented as separate interactive *single page applications*. In particular:

* the projects table located at `/projects/`,
* the project dashboard located at `/projects/<id>/`,
* the management interface located at `/management/`.

The Django template of these pages contain just an empty element, and the functionality is implemented with JavaScript, React and Redux, and makes heavy use of the REST API.

In order to keep the deployment effort low, no node dependencies need to be handled by the maintainers of the instances. Instead, the frontend is build when creating the release and is then shipped as part of the `rdmo` Python package. Frontend source files reside in `rdmo/<module>/assets/` and the build is stored in `rdmo/<module>/static/`, from where Django handles them as regular static files.
