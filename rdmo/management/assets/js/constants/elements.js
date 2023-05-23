const elementTypes = {
  'questions.catalog': 'catalogs',
  'questions.section': 'sections',
  'questions.page': 'pages',
  'questions.questionset': 'questionsets',
  'questions.question': 'questions',
  'domain.attribute':'attributes',
  'options.optionset': 'optionsets',
  'options.option': 'options',
  'condition.condition': 'conditions',
  'tasks.task': 'tasks',
  'tasks.view': 'views'
}

const elementModules = {
  'catalogs': 'questions',
  'sections': 'questions',
  'pages': 'questions',
  'questionsets': 'questions',
  'questions': 'questions',
  'attributes': 'domain',
  'optionsets': 'options',
  'options': 'options',
  'conditions': 'conditions',
  'tasks': 'tasks',
  'views': 'views'
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
  'condition.condition': 'code-conditions',
  'tasks.task': 'code-tasks',
  'tasks.view': 'code-views'
}

const verboseNames = {
  'questions.catalog': gettext('Catalogs'),
  'questions.section': gettext('Section'),
  'questions.page': gettext('Page'),
  'questions.questionset': gettext('Question set'),
  'questions.question': gettext('Question'),
  'domain.attribute': gettext('Attribute'),
  'options.optionset': gettext('Option set'),
  'options.option': gettext('Option'),
  'condition.condition': gettext('Condition'),
  'tasks.task': gettext('Task'),
  'tasks.view': gettext('View')
}

export { elementTypes, elementModules, codeClass, verboseNames }
