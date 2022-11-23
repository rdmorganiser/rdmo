import QuestionsApi from '../api/QuestionsApi'

export function fetchElements(config) {
  return function(dispatch) {
    dispatch(fetchElementsInit())

    switch (config.resourceType) {
      case 'catalogs':
        dispatch(fetchCatalogs())
        break
      case 'sections':
        dispatch(fetchSections())
        break
      case 'pages':
        dispatch(fetchPages())
        break
      case 'questionsets':
        dispatch(fetchQuestionSets())
        break
      case 'questions':
        dispatch(fetchQuestions())
        break
    }
  }
}

export function fetchElementsInit() {
  return {type: 'elements/fetchElementsSuccess'}
}

export function fetchElementsSuccess({ resourceType, elements }) {
  return {type: 'elements/fetchElementsSuccess', resourceType, elements}
}

export function fetchElementsError({ resourceType, error }) {
  return {type: 'elements/fetchElementsError', resourceType, error}
}

export function fetchElement(config) {
  return {type: 'elements/fetchElement', config}
}

export function fetchElementSuccess(element) {
  return {type: 'elements/fetchElementSuccess', element}
}

export function fetchCatalogs() {
  return function(dispatch) {
    return QuestionsApi.fetchCatalogs(true).then(elements => {
      dispatch(fetchElementsSuccess({ resourceType: 'catalogs', elements }))
    }).catch(error => {
      dispatch(fetchElementsError({ resourceType: 'catalogs', error }))
    })
  }
}

export function fetchSections() {
  return function(dispatch) {
    return QuestionsApi.fetchSections(true).then(elements => {
      dispatch(fetchElementsSuccess({ resourceType: 'sections', elements }))
    }).catch(error => {
      dispatch(fetchElementsError({ resourceType: 'sections', error }))
    })
  }
}

export function fetchPages() {
  return function(dispatch) {
    return QuestionsApi.fetchQuestionSets(true).then(elements => {
      dispatch(fetchElementsSuccess({ resourceType: 'questionsets', elements }))
    }).catch(error => {
      dispatch(fetchElementsError({ resourceType: 'questionsets', error }))
    })
  }
}

export function fetchQuestionSets() {
  return function(dispatch) {
    return QuestionsApi.fetchQuestionSets(true).then(elements => {
      dispatch(fetchElementsSuccess({ resourceType: 'questionsets', elements }))
    }).catch(error => {
      dispatch(fetchElementsError({ resourceType: 'questionsets', error }))
    })
  }
}

export function fetchQuestions() {
  return function(dispatch) {
    return QuestionsApi.fetchQuestions(true).then(elements => {
      dispatch(fetchElementsSuccess({ resourceType: 'questions', elements }))
    }).catch(error => {
      dispatch(fetchElementsError({ resourceType: 'questions', error }))
    })
  }
}
