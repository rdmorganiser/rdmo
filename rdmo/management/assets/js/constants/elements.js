const elementTypes = [
  'catalogs',
  'sections',
  'questionsets',
  'pages',
  'questions',
  'attributes',
  'optionsets',
  'options',
  'conditions',
  'tasks',
  'views'
]

const elementModules = {
  'catalog': 'questions',
  'section': 'questions',
  'questionset': 'questions',
  'page': 'questions',
  'question': 'questions',
  'attribute': 'domain',
  'optionset': 'options',
  'option': 'options',
  'condition': 'conditions',
  'task': 'tasks',
  'view': 'views'
}

const codeClass = {
  'catalog': 'code-questions',
  'section': 'code-questions',
  'questionset': 'code-questions',
  'page': 'code-questions',
  'question': 'code-questions',
  'attribute': 'code-domain',
  'optionset': 'code-options',
  'option': 'code-options',
  'condition': 'code-conditions',
  'task': 'code-tasks',
  'view': 'code-views'
}

export { elementTypes, elementModules, codeClass }
