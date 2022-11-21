import QuestionsApi from '../api/QuestionsApi'

export function fetchElements(config) {
  return function(dispatch) {
    switch (config.resourceType) {
      case 'catalogs':
        dispatch(fetchCatalogs())
        break
    }
  }
}

export function fetchElementsSuccess({ resource, elements }) {
  return {type: 'elements/fetchElementsSuccess', resource, elements }
}

export function fetchElement(config) {
  return {type: 'elements/fetchElement', config}
}

export function fetchElementSuccess(element) {
  return {type: 'elements/fetchElementSuccess', element}
}

export function fetchCatalogs() {
  return function(dispatch) {
    return QuestionsApi.fetchCatalogs().then(elements => {
      dispatch(fetchElementsSuccess({ resourceType: 'catalogs', elements }))
    })
  }
}
