const elementTypes = {
  'questions.catalog': 'catalogs',
  'questions.section': 'sections',
  'questions.page': 'pages',
  'questions.questionset': 'questionsets',
  'questions.question': 'questions',
  'domain.attribute': 'attributes',
  'options.optionset': 'optionsets',
  'options.option': 'options',
  'conditions.condition': 'conditions',
  'tasks.task': 'tasks',
  'views.view': 'views'
}

const elementModules = {
  'questions.catalog': 'questions',
  'questions.section': 'questions',
  'questions.page': 'questions',
  'questions.questionset': 'questions',
  'questions.question': 'questions',
  'domain.attribute': 'domain',
  'options.optionset': 'options',
  'options.option': 'options',
  'conditions.condition': 'conditions',
  'tasks.task': 'tasks',
  'views.view': 'views'
}

const codeClass = {
  'questions.catalog': 'code-questions',
  'questions.section': 'code-questions',
  'questions.page': 'code-questions',
  'questions.questionset': 'code-questions',
  'questions.question': 'code-questions',
  'domain.attribute': 'code-domain',
  'options.optionset': 'code-options',
  'options.option': 'code-options',
  'conditions.condition': 'code-conditions',
  'tasks.task': 'code-tasks',
  'views.view': 'code-views'
}

const verboseNames = {
  'questions.catalog': gettext('Catalog'),
  'questions.section': gettext('Section'),
  'questions.page': gettext('Page'),
  'questions.questionset': gettext('Question set'),
  'questions.question': gettext('Question'),
  'domain.attribute': gettext('Attribute'),
  'options.optionset': gettext('Option set'),
  'options.option': gettext('Option'),
  'conditions.condition': gettext('Condition'),
  'tasks.task': gettext('Task'),
  'views.view': gettext('View')
}

export { elementTypes, elementModules, codeClass, verboseNames }
