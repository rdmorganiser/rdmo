import isEmpty from 'lodash/isEmpty';
import isUndefined from 'lodash/isUndefined';

const replaceElement = (elements, element) => {
  const index = elements.findIndex(e => e.uri == element.uri)

  if (index < 0) {
    return elements.map(child => {
      if (!isUndefined(child.elements) && !isEmpty(child.elements)) {
        child.elements = replaceElement(child.elements, element)
      }
      return child
    })
  } else {
    elements[index] = {...elements[index], ...element}
  }
  return elements
}

export { replaceElement }
