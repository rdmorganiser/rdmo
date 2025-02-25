# Changelog

## [RDMO 2.3.0](https://github.com/rdmorganiser/rdmo/compare/2.2.2...2.3.0)

* Add new interview interface based on React and Redux (#518)
  * Text and Textarea widgets are now saved automatically
  * Select dropdown widgets are now always searchable
  * Show the unit of a question next to the answer field (#499)
  * Tabs (e.g. Datasets) and single values can be reused in different projects.
  * An "Apply to all" button can be used to paste information into all the tabs.
  * Remove custom widgets feature (remove `QUESTIONS_WIDGETS` from settings)
  * Fix several issues regarding the interface (#501, #224)
  * Display attributes in interview to admins, editors, reviewers (#224)
  * Improve accessibility (#514, #1199)
* Add the possibility to copy a project including all its values.
* Add the option to make a project "visible" to all users (#152).
  * Users interact with visible projects as if they would have the Guest role.
  * With the new review feature, this can be used for templates for projects and datasets.
  * Sites and groups can be used to restrict this behaviour.
  * This feature is enabled by default via the `PROJECT_VISIBILITY` setting
* Add a contact form modal to each question to contact support (#502)
  * `PROJECT_CONTACT = True` and `PROJECT_CONTACT_RECIPIENTS = [list of email strings]`
    enable this feature
* Add signal handlers to automatically sync of project views and tasks (#345, #966, #1198)
  * When `PROJECT_VIEWS_SYNC = True` or `PROJECT_TASKS_SYNC = True` is set, the views or
    tasks for a project are automatically synchronized, depending on the
    catalogs configured for them.
* Add snapshot export plugins (which work like project export plugins)
  * Add `PROJECT_SNAPSHOT_EXPORTS` to settings to register snapshot export plugins
* Refactor the `accept` field for project import plugins
  * The field is now a dict of the form `{'content_type': ['suffix']}`
  * The old form should still work
* Add `rdmo.accounts.middleware.TermsAndConditionsRedirectMiddleware'` (#141, #161)
  * The (optional) middleware checks if a user has already confirmed the Terms of use.
  * If not, users need to confirm to proceed.
  * Optionally, when a confirmation renewal is required, the `ACCOUNT_TERMS_OF_USE_DATE = '2025-02-25'`
    can be set to invalidate previous confirmations.
* Add `rdmo-admin` script
  * `rdmo-admin npm run [build:prod|build|watch]` can be used to build the front end
  * `rdmo-admin build` can be used to build the python package
  * `rdmo-admin messages [make|compile]` can be used create and compile the translations
  * `rdmo-admin clean` can be used remove most files which are not version controlled
* Add the support for custom markdown templates injected into help texts
  * The code `{{ code }}` is replaced by a template specified in the `MARKDOWN_TEMPLATES` setting
  * The `TEMPLATES_EXECUTE_SCRIPT_TAGS' setting controls whether Java script code can be executed.
* Add minimum required version to RDMO XML exports (#1205).
* Use the `uri` instead of `path` for attributes in the Django admin interface.
* Fix a set of bugs where the maximum length of a field was not correctly validated by the API.
* Use `lualatex` when using `Pandoc >= 3.0`.
* Remove the `download_vendor_files` step of the setup
  * Remove `VENDOR` and `VENDOR_CDN` from settings.
* Update Python and JavaScript dependencies.
* Drop support for Python 3.8.

## [RDMO 2.2.2](https://github.com/rdmorganiser/rdmo/compare/2.2.1...2.2.2) (Oct 24, 2024)

* Fix projects interface when using RDMO with a path (#1152)
* Fix missing (unavailable) catalogs projects interface

## [RDMO 2.2.1](https://github.com/rdmorganiser/rdmo/compare/2.2.0...2.2.1) (Sep 13, 2024)

* Fix import error when allauth is not used (#1145)
* Fix a bug with collection pages when optionset refresh is true (#1147)
* Prevent the page to change when a validation error occurs on project_questions (#1134)
* Pin importlib_metadata to 0.8.4 due to an upstream problem

## [RDMO 2.2.0](https://github.com/rdmorganiser/rdmo/compare/2.1.3...2.2.0) (Sep 05, 2024)

* Add new projects overview (#865, #355)
  * Projects are now displayed in an interactive table which can be filtered and ordered
  * The projects API is now paginated (new setting PROJECT_TABLE_PAGE_SIZE)
* Add new import interface to management (#469, #468, #465, )
  * Show detailed information what is new and what changed
  * Show a summary of warnings and errors at the top of the page
* Add validation depending on the `value_type` configured for the question
  * Validation needs to be enabled using `PROJECT_VALUES_VALIDATION = True`
  * Configuration can be adjusted using settings for each value_type
* Enable markdown rendering for titles and texts of elements
* All parent attributes are now added to the full XML export
* Use only available catalogs for project import by users (#455)
* Add workaround for conflict validation for checkboxes (#903)
* Add `merge_attributes` management script to move related items from one attribute to another (#990)
* Add `join_values_inline` tag for views (#964)
* Add `user` and `site` to optionset provider plugins (#430)
* Add short title field for sections and pages for the navigation (#346, #363)
* Add section progress to the navigation
* Add button to add/remove the current site to an element in the management interface for multi site instances (#825)
* Fix a bug with conditions with non-consecutive set_index (when datasets are created and deleted)
* Fix a bug with the progress bar when a section has no pages
* Fix progress action if progress did not change
* Fix bugs with element copy in management (#995, #980)
* Fix typos and missing translations on buttons in management interface (#1020, #944)
* Fix link target for links in management interface (#1007)
* Fix textarea resizing (#1021)
* Fix export links in management (#915)
* Fix typos (#1001)
* Use ACCOUNT_FORMS instead of ACCOUNT_SIGNUP_FORM_CLASS in settings
* Remove local hosts from ALLOWED_HOSTS settings
* Improve admin interface (#942, #918)
* Update default home page

## [RDMO 2.1.3](https://github.com/rdmorganiser/rdmo/compare/2.1.2...2.1.3) (Feb 13, 2024)

* Fix the migration of options with additional_input (#912)
* Fix export urls in management when using BASE_PATH (#915)

## [RDMO 2.1.2](https://github.com/rdmorganiser/rdmo/compare/2.1.1...2.1.2) (Jan 15, 2024)

* Fix a bug with webpack font paths
* Fix a bug with option set provider plugins
* Fix a bug with the autocomplete widget
* Add invite.email to send_invite_email context

## [RDMO 2.1.1](https://github.com/rdmorganiser/rdmo/compare/2.1.0...2.1.1) (Dec 21, 2023)

* Fix translations
* Fix bugs with the new progress bar
* Fix issues with option set provider plugins
* Fix issues with import and export in management
* Fix management when BASE_URL is set

## [RDMO 2.1.0](https://github.com/rdmorganiser/rdmo/compare/2.0.2...2.1.0) (Dec 11, 2023)

* Refactor progress bar and overview
  * Fix the progress bar to consider tabs and conditions correctly
  * Show the project progress in the projects overview and the project hierarchy
  * Show which pages are fully or partially answered in the overview
* Refactor options
  * Allow `textarea` as additional input for options
  * Add `view_text` to options to be used in the interview instead of `text`
  * Add `help` to options to be shown next to the option in the interview
* Fix grammar issues in automatically generated help text in the interview
  * Use generic formulations and a "+" sign
  * Remove `verbose_name_plural` field
* Refactor autocomplete widget
  * Add `freeautocomplete` which can also store arbitrary inputs
  * Fix various issues with autocomplete
* Improve help texts
  * Add a custom {more} markdown tag to create a show more/less interaction
  * Adjust the styling of details/summary html tags
* Add restricted accounts
  * Add `PROJECT_CREATE_RESTRICTED` and `PROJECT_CREATE_GROUPS` to restrict project creation to certain groups
  * Add `ACCOUNT_GROUPS` and `SOCIALACCOUNT_GROUPS` to put new user automatically into groups
* Improve new management interface
  * Initialize filters with current site
  * Show order parameter for ordered many to many fields
  * Add current site to new elements
  * Fix translation bugs in the new management interface
* Prevent conflicts when users edit the same values simultaneously
* Add order parameter to tasks/issues and views and order accordingly in the project overview
* Add `option_text` and `option_additional_input` to values to be used in templates
* `Value.value` now always returns a string (and not `None`)
* Move GitHub and GitLab to separate repositories
* Fix option set refresh in the interview
* Fix `allauth` issues
* Add front-end tests using playwright
* Improve continuous integration

## [RDMO 2.0.2](https://github.com/rdmorganiser/rdmo/compare/2.0.1...2.0.2) (Nov 2, 2023)

* Fix migration to RDMO 2.0 for PostgreSQL
* Fix Shibboleth urls
* Fix issue view
* Fix margins in management interface

## [RDMO 2.0.1](https://github.com/rdmorganiser/rdmo/compare/2.0.0...2.0.1) (Oct 9, 2023)

* Fix question set and questions ordering on page
* Fix removal of question sets in interview
* Add official support for Python 3.12

## [RDMO 2.0.0](https://github.com/rdmorganiser/rdmo/compare/1.11.0...2.0.0) (Sep 22, 2023)

* Refactor data model of questions app:
  * Introduce Pages model, replacing question sets which are not nested
  * Use m2m relations instead of foreign keys, e.g. one catalog has now many sections, but one section can be also part of many catalogs
  * Refactor import and update elements import format, but keep old format working
  * Rename key to uri_path in all element models, but Attribute
* Add new React/Redux-based management interface, which replaces the 6 old interfaces:
  * Add table-like views for all elements, with locking, availability and export buttons
  * Add nested views for catalogs, sections, pages and question sets
  * Improve edit views for elements, remove modals
* Add Site-based permissions for all elements and new editor and reviewer roles
* Add set_collection to Value model to store if this value was part of a set
* Add JSON project export and refactor CSV exports
* Add refresh to option set providers
* Don't open XML exports in browser, except when EXPORT_CONTENT_DISPOSITION = None
* Fix new Shibboleth setup
* Refactor packaging, add pyproject.toml
* Add pre-commit-config
* Overhaul testing and CI
* Update Python dependencies, drop support for EOL Python 3.6 and 3.7
* Update CITATION.cff file

## [RDMO 1.11.0](https://github.com/rdmorganiser/rdmo/compare/1.10.0...1.11.0) (Aug 1, 2023)

* Refactor Shibboleth setup, add LOGIN_FORM, SHIBBOLETH_LOGIN_URL
* Add filter for catalogs to site_projects view
* Add API for project Invites
* Add catalog, site, and rdmo version to views
* Enable PROJECT_QUESTIONS_AUTOSAVE by default
* Remove skip button when PROJECT_QUESTIONS_AUTOSAVE is True, move back button
* Remove automatic replacement of missing translations, unless REPLACE_MISSING_TRANSLATION is True
* Hide html metadata tag in views
* Update django-allauth requirement

## [RDMO 1.10.0](https://github.com/rdmorganiser/rdmo/compare/1.9.2...1.10.0) (Apr 27, 2023)

* Allow users to create API access tokens (if ACCOUNT_ALLOW_USER_TOKEN is set)
* Allow users to remove their account when using Shibboleth
* Fix missing views when creating a project via API
* Fix pagination when filtering projects
* Add counter to projects filtering
* Add an error message if save fails in the interview
* Adjust interview buttons if PROJECT_QUESTIONS_AUTOSAVE is True
* Adjust style for \<summary> tag

## [RDMO 1.9.2](https://github.com/rdmorganiser/rdmo/compare/1.9.1...1.9.2) (Feb 23, 2023)

* Fix URL in invite emails in the multi site setup (#576)
* Check permissions for parent project on project page (#576)
* Fix project invite timeout (#580)
* Restore missing commits from last release

## [RDMO 1.9.1](https://github.com/rdmorganiser/rdmo/compare/1.9.0...1.9.1) (Feb 03, 2023)

* Fix overlays if tasks/views are not available for a project
* Add a last overlay with the invitation to contact local support
* Add find_inactive_users and find_inactive_projects management scripts
* Add delete_projects management script
* Fix cancel button on project import
* Add A4 as default paper size to pandoc args
* Improve continuous integration

## [RDMO 1.9.0](https://github.com/rdmorganiser/rdmo/compare/1.8.2...1.9.0) (Nov 28, 2022)

* Automatically update existing projects on saving of views
  * Remove views from projects if they are not available for this site and group anymore
  * PROJECT_REMOVE_VIEWS = False disables this new behavior
* Improve interview interface
  * Add a "breadcrumb" element with the project and the section
  * Remove "Questionnaire" headline
* Change list separation in views from ","" to ";"
* Add filter for current site to catalog management
* Add checkboxes to hide/show URI in catalog management
* Add owners to Snapshot Admin
* Add additional fields to Api
* Add potential views to project context data
* Fix import with different URI prefixes
* Fix CSV export
* Fix delete profile form
* Fix non-deletable questionsets-in-questionsets
* Fix missing redirect after login when allauth is not used

## [RDMO 1.8.2](https://github.com/rdmorganiser/rdmo/compare/1.8.1...1.8.2) (Aug 01, 2022)

* Add Spanish translation
* Add URI to projects and values API
* Add missing (meta-)migrations (which do not alter the database)
* Fix typos in code and translations
* Update requirements

## [RDMO 1.8.1](https://github.com/rdmorganiser/rdmo/compare/1.8.0...1.8.1) (May 25, 2022)

* Fix a bug on the "show all projects on site" view
* Fix a bug with the slider in the interview
* Fix a when selecting and deselecting a checkbox in the interview
* Fix exception when no user matched filter criteria
* Add keycloak logo to be used with allauth
* Add email and phone to VALUE_TYPE_CHOICES
* Various minor fixes

## [RDMO 1.8.0](https://github.com/rdmorganiser/rdmo/compare/1.7.0...1.8.0) (Mar 07, 2022)

* Add Project Export Provider to perform import and export from and to webservices
* Move GitHub and GitLab providers and rename SERVICE_PROVIDERS -> PROJECT_ISSUE_PROVIDERS
* Add `find_users`, `find_spam_users`, `delete_users` management scripts
* Add `export_projects` management script
* Add search_fields and list_filter to RoleAdmin
* Add a cancel button to the import screen
* Use simpler queryset for index actions
* Fix typos in overlays
* Fix template validation
* Improve performance
* Various fixes

## [RDMO 1.7.0](https://github.com/rdmorganiser/rdmo/compare/1.6.2...1.7.0) (Dec 01, 2021)

* Show questionsets with conditions in navigation
* Change Save and proceed behavior
* Add PROJECT_QUESTIONS_CYCLE_SETS settings to keep old behavior
* Add account deletion for LDAP users
* Fix attribute export
* Fix condition resolution when going backwards
* Prevent overlay errors if custom list is used
* Various fixes

## [RDMO 1.6.2](https://github.com/rdmorganiser/rdmo/compare/1.6.1...1.6.2) (Nov 03, 2021)

* Fix bug with overlays
* Fix bug with set deletion
* Fix problem with conditions
* Replaced Travis-CI automation by GitHub Actions
* Add prune projects management command

## [RDMO 1.6.1](https://github.com/rdmorganiser/rdmo/compare/1.6...1.6.1) (Oct 08, 2021)

* Fix additional values in project_questions

## [RDMO 1.6](https://github.com/rdmorganiser/rdmo/compare/1.5.5...1.6) (Sep 28, 2021)

* Improve management interface, refactor filters and fetch lists on model opening
* Improve interview and save only changed values
* Improve error output for imports
* Add nested questionsets to catalogs and set_prefix to values
* Add default values for questions (as part of the catalog)
* Add optional flag to questions (which excludes them from progress computation)
* Add width to questions to enable table-like input
* Add autocomplete widget incl. server-side search for optionset plugins
* Add conditions for single questions and refactor condition handling
* Add PROJECT_QUESTIONS_AUTOSAVE settings to automatically save on user interaction
* Add tooltips to markdown help texts using the special `[text]{tooltip}` syntax
* Add issues/views block to projects even when empty and add PROJECT_ISSUES and PROJECT_VIEWS settings
* Add autofocus to project title in the create project form
* Add overlay tutorials to projects and project pages
* Add check_condition tag to check conditions in project_answers and views
* Add checkboxed to hide questions, questionsets and options in the management interface
* Add export form to questions sidebar in order to save vertical space
* Add snapshot information to view
* Add is_empty to values and view_tags
* Add manage.py upgrade script to combine migrate, download_vendor_files and collectstatic
* Add GitLab provider and refactor GitHub provider
* Make questionset id attribute explicit and migrate existing questionsets accordingly
* Refactor theme creation
* Remove caching for project questionsets, since the api is now project specific
* Replace package csv by defusedcsv to prevent csv vulnerabilities
* Fix title warning for questions modal
* Fix continuation for catalog switch
* Split project_detail_header template and add catalogs to project page
* Allow for custom user models (in fresh instances)
* Optimize database access and increase overall performance

## [RDMO 1.5.5](https://github.com/rdmorganiser/rdmo/compare/1.5.4...1.5.5) (Mar 25, 2021)

* Fix signup url on home page
* Fix continuation to end of interview
* Fix shibboleth logout
* Fix checkboxes in new set

## [RDMO 1.5.4](https://github.com/rdmorganiser/rdmo/compare/1.5.3...1.5.4) (Mar 17, 2021)

* Fix xml mimetype check for centos
* Fix project_answers_tree.html for sets

## [RDMO 1.5.3](https://github.com/rdmorganiser/rdmo/compare/1.5.2...1.5.3) (Mar 4, 2021)

* Fix migrations

## [RDMO 1.5.2](https://github.com/rdmorganiser/rdmo/compare/1.5.1...1.5.2) ( Mar 4, 2021)

* Fix catalog display in interview

## [RDMO 1.5.1](https://github.com/rdmorganiser/rdmo/compare/1.5...1.5.1) (Feb 25, 2021)

* Update versions and fix requirements pinning

## [RDMO 1.5](https://github.com/rdmorganiser/rdmo/compare/1.4...1.5) (Feb 23, 2021)

* Improve user interface:
  * Add functionality to continue interview at the last edited questionset
  * Change order of options in projects and project sidebars to improve usability
  * Remove user credentials from projects page
  * Add additional help text to project page
  * Add additional interaction elements (e.g. invite user) to project page
* Add file upload fields to questionnaire:
  * Add uploaded files to views (images are displayed inline, other files can be downloaded)
  * Add uploaded files to issues/tasks to be send as attachments
* Add project hierarchy:
  * Add parent field to projects, resulting in a tree structure
  * Add child projects to views
  * Add function to import values from parent project to child projects
  * Inherit memberships of superior projects to child projects
* Refactor project memberships:
  * Add invitation by mail (to existing or external users)
  * Add silent creation of memberships for site managers and admins
  * Add separate "Leave project" function
* Add "Locked" flag to elements to prevent unintended changes
* Add PROJECT_FILE_QUOTA to settings to control file quota of projects
* Add NESTED_PROJECTS to settings to disable nested projects
* Add PROJECT_SEND_INVITE to settings to disable invite mails to external users
* Add PROJECT_INVITE_TIMEOUT to set a timeout on invites
* Refactor view rendering and add ProjectWrapper
* Refactor project import
* Refactor validation
* Refactor test for projects
* Optimize database access and increase overall performance

## [RDMO 1.4](https://github.com/rdmorganiser/rdmo/compare/1.3...1.4) (Dec 9, 2020)

* Validate URI instead of path/key and allow for non-unique path/key
* Add the selection of the parent Attribute when cloning Sections, QuestionSets, Questions, Options or Attributes
* Add an assertion and a new Validator to prevent users from cloning Attributes in a bad way.
* Add reference counts to management interface and references to delete modals
* Add order of a Section, QuestionSet, Question or Option to the management views
* Add function to restrict tasks to catalogs
* Add users to API
* Add specific colors to management interface
* Refactor progress bar to show real progress
* Refactor management export templates
* Use parent uri prefix as default when adding new elements
* Use markdown for catalog, task, and view description
* Fix a bug with the import of option sets
* Fix a bug with RDF exports
* Allow anonymous users to see the terms of use
* Allow project export for managers
* Update Italian translation

## [RDMO 1.3](https://github.com/rdmorganiser/rdmo/compare/1.2...1.3) (Oct 6, 2020)

* Refactor tasks in projects (using a new model `Issue`) to store the status of the task for this project
* Add integrations to projects, the `services` app, and service provider plugins to connect RDMO to external services, such as issue trackers
* Add functionality to send issues via mail or integration including attached answers or views
* Add optionset provider plugins to create dynamic optionsets, e.g. to fetch repositories from re3data.org
* Add possibility to set distinct reference documents for a single view
* Enable footer language by template
* Allow empty questionsets
* Fix order of optionsets in interview
* Fix an issue where weeks in the datepicker start on Sundays
* Fix a bug where catalogs and tasks where not copied correctly

## [RDMO 1.2](https://github.com/rdmorganiser/rdmo/compare/1.1...1.2) (Sep 2, 2020)

* Add functionality to import and export single elements (e.g. optionsets, views)
* Add functionality to copy elements directly through the management interface
* Add "project/title", "project/description", "project/created" and "project/upgraded" to be available in views using "render_value"
* Add Italian language files
* Add visual improvements to the interview (buttons, navigation)
* Make the sidebar "sticky" on all pages
* Fix a path related bug on Windows
* Fix missing project or view title when selected language did provide one
* Fix translations

## [RDMO 1.1](https://github.com/rdmorganiser/rdmo/compare/1.0.8...1.1) (Aug 4, 2020)

* Add plugins to implement custom project export and import
* Refactor project import workflow and include overview pages before and after import

## [RDMO 1.0.8](https://github.com/rdmorganiser/rdmo/compare/1.0.7...1.0.8) (Jul 2, 2020)

* Fix a bug with project pagination.

## [RDMO 1.0.7](https://github.com/rdmorganiser/rdmo/compare/1.0.6...1.0.7) (Jun 30, 2020)

* Add Multi-Site-Feature which allows to run multiple different RDMO frontpages in a single instance
* Add projects overview page for admins and site managers
* Add functionality to restrict catalogs and views to sites or groups
* Add terms of use page
* Add French language files
* Improve and simplify handling of templates that exist in multiple translations

## [RDMO 1.0.6](https://github.com/rdmorganiser/rdmo/compare/1.0.5...1.0.6) (Mar 04, 2020)

* Add possibility to do calculations in views using [mathfilters](https://pypi.org/project/django-mathfilters/)

## [RDMO 1.0.5](https://github.com/rdmorganiser/rdmo/compare/1.0.4...1.0.5) (Mar 30, 2020)

* Fix a bug which prevented the installation of version 1.0.4
* Fix vendor file download

## [RDMO 1.0.4](https://github.com/rdmorganiser/rdmo/compare/1.0.3...1.0.4) (Mar 30, 2020)

* Fix some issued with ORCID login. New entries were added to local.py to allow for more flexible authentication workflows:
  * `SOCIALACCOUNT_SIGNUP` is set to False by default. Change into True to enable users to create an account via social accounts, e.g. ORCID
  * `SOCIALACCOUNT_AUTO_SIGNUP` is set to False by default. Set it to True to enable automatic creation of an account when using a social account for the first time Otherwise new users need to fill out a signup form even if the provider does provide the email address. This should be False when using the public ORCID API, but can be set to True when you are sure that an email is provided by the OAuth provider.
* Add styled ORCID login button
* Sort question catalogs alphabetically in right side menu
* Fix vendor files update process
* Fix order of sets in views
* Fix minor issues regarding colours and wording

## [RDMO 1.0.3](https://github.com/rdmorganiser/rdmo/compare/1.0.2...1.0.3) (Jan 30, 2020)

* Refactor all tests to use pytest
* Fix a bug where exported options had wrong tags
* Update vendor files
* Improve API by adding additional filter options

## [RDMO 1.0.2](https://github.com/rdmorganiser/rdmo/compare/1.0.1...1.0.2) (Dec 6, 2019)

* Pin requirement to compatible versions

## [RDMO 1.0.1](https://github.com/rdmorganiser/rdmo/compare/1.0.0...1.0.1) (Oct 30, 2019)

* Fix installation procedure

## RDMO 1.0.0 (Oct 30, 2019)

* First major release
