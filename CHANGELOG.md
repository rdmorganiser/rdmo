# Changelog

## RDMO 1.5 (Feb 23, 2021)

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

## RDMO 1.4 (Dec 9, 2020)

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

## RDMO 1.3 (Oct 6, 2020)

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

## RDMO 1.2 (Sep 2, 2020)

* Add functionality to import and export single elements (e.g. optionsets, views)
* Add functionality to copy elements directly through the management interface
* Add "project/title", "project/description", "project/created" and "project/upgraded" to be available in views using "render_value"
* Add Italian language files
* Add visual improvements to the interview (buttons, navigation)
* Make the sidebar "sticky" on all pages
* Fix a path related bug on Windows
* Fix missing project or view title when selected language did provide one
* Fix translations

## RDMO 1.1 (Aug 4, 2020)

* Add plugins to implement custom project export and import
* Refactor project import workflow and include overview pages before and after import

## RDMO 1.0.8 (Jul 2, 2020)

* Fix a bug with project pagination.

## RDMO 1.0.7 (Jun 30, 2020)

* Add Multi-Site-Feature which allows to run multiple different RDMO frontpages in a single instance
* Add projects overview page for admins and site managers
* Add functionality to restrict catalogs and views to sites or groups
* Add terms of use page
* Add French language files
* Improve and simplify handling of templates that exist in multiple translations

## RDMO 1.0.6 (Mar 04, 2020)

* Add possibility to do calculations in views using [mathfilters](https://pypi.org/project/django-mathfilters/)

## RDMO 1.0.5 (Mar 30, 2020)

* Fix a bug which prevented the installation of version 1.0.4
* Fix vendor file download

## RDMO 1.0.4 (Mar 30, 2020)

* Fix some issued with ORCID login. New entries were added to local.py to allow for more flexible authentication workflows:
    * `SOCIALACCOUNT_SIGNUP` is set to False by default. Change into True to enable users to create an account via social accounts, e.g. ORCID
    * `SOCIALACCOUNT_AUTO_SIGNUP` is set to False by default. Set it to True to enable automatic creation of an account when using a social account for the first time Otherwise new users need to fill out a signup form even if the provider does provide the email address. This should be False when using the public ORCID API, but can be set to True when you are sure that an email is provided by the OAuth provider.
* Add styled ORCID login button
* Sort question catalogs alphabetically in right side menu
* Fix vendor files update process
* Fix order of sets in views
* Fix minor issues regarding colours and wording

## RDMO 1.0.3 (Jan 30, 2020)

* Refactor all tests to use pytest
* Fix a bug where exported options had wrong tags
* Update vendor files
* Improve API by adding additional filter options

## RDMO 1.0.2 (Dec 6, 2019)

* Pin requirement to compatible versions

## RDMO 1.0.1 (Oct 30, 2019)

* Fix installation procedure

## RDMO 1.0.0 (Oct 30, 2019)

* First major release
