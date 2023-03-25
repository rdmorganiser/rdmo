import isEmpty from 'lodash/isEmpty';
import isUndefined from 'lodash/isUndefined';

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

export { updateElement, resetElement }
