import isEmpty from 'lodash/isEmpty';
import isUndefined from 'lodash/isUndefined';

import { elementModules } from '../constants/elements'

const updateElement = (element, actionElement) => {
  if (element.uri == actionElement.uri) {
    return {...element, ...actionElement}
  } else if (!isUndefined(element.elements)) {
    return {...element, elements: element.elements.map(e => updateElement(e, actionElement))}
  } else {
    return element
  }
}

const resetElement = (element) => {
  delete element.errors

  if (!isUndefined(element.elements)) {
    element.elements.forEach(e => resetElement(e))
  }

  return element
}

const buildUri = (element) => {
  let uri = element.uri_prefix + '/' + elementModules[element.type] + '/'

  if (!isUndefined(element.uri_path)) {
    uri += element.uri_path
  } else if (!isUndefined(element.path)) {
    uri += element.path
  } else {
    uri += element.key
  }

  return uri
}

export { updateElement, resetElement, buildUri }
