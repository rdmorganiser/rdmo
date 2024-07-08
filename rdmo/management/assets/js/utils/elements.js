import isNil from 'lodash/isNil'
import isUndefined from 'lodash/isUndefined'

import { elementTypes, elementModules } from '../constants/elements'

const compareElements = (element1, element2) => {
  return element1.model == element2.model && element1.id == element2.id
}

const updateElement = (element, actionElement) => {
  if (compareElements(element, actionElement)) {
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

function canMoveElement(dragElement, dropElement) {
  if (compareElements(dragElement, dropElement)) {
    // an element cannot be moved on itself
    return false
  } else if (isUndefined(dragElement.elements)) {
    // if dragElement has no elements, the element can be moved
    return true
  } else {
    // check recursively if one of the descendants of dragElement is dropElement
    return dragElement.elements.reduce((acc, el) => {
      return acc && canMoveElement(el, dropElement)
    }, true)
  }
}

function moveElement(element, dragElement, dropElement, mode) {
  const dragParent = removeElement(element, dragElement)

  let dropParent
  switch (mode) {
    case 'before':
      dropParent = insertBeforeElement(element, dragElement, dropElement)
      break
    case 'after':
      dropParent = insertAfterElement(element, dragElement, dropElement)
      break
    default:
      dropParent = insertInElement(dragElement, dropElement)
      break
  }

  updateElementElements(dragParent)
  if (compareElements(dragParent, dropParent)) {
    dropParent = null
  } else {
    updateElementElements(dropParent)
  }

  return { dragParent, dropParent }
}

function removeElement(element, dragElement) {
  if (isUndefined(element.elements)) return null

  const dragIndex = element.elements.findIndex(el => compareElements(el, dragElement))
  if (dragIndex > -1) {
    // remove the element
    element.elements.splice(dragIndex, 1)
    return element
  } else {
    // call the function recursively and return the first element which is not null
    return element.elements.map(el => removeElement(el, dragElement))
                           .find(el => !isNil(el))
  }
}

function insertBeforeElement(element, dragElement, dropElement) {
  if (isUndefined(element.elements)) return null

  const dropIndex = element.elements.findIndex(el => compareElements(el, dropElement))
  if (dropIndex > -1) {
    // insert the dragElement before the dropElement
    element.elements.splice(dropIndex, 0, dragElement)
    return element
  } else {
    // call the function recursively and return the first element which is not null
    return element.elements.map(el => insertBeforeElement(el, dragElement, dropElement))
                           .find(el => !isNil(el))
  }
}

function insertAfterElement(element, dragElement, dropElement) {
  if (isUndefined(element.elements)) return null

  const dropIndex = element.elements.findIndex(el => compareElements(el, dropElement))
  if (dropIndex > -1) {
    // insert the dragElement after the dropElement
    element.elements.splice(dropIndex + 1, 0, dragElement)
    return element
  } else {
    // call the function recursively and return the first element which is not null
    return element.elements.map(el => insertAfterElement(el, dragElement, dropElement))
                           .find(el => !isNil(el))
  }
}

function insertInElement(dragElement, dropElement) {
  const dropParent = dropElement
  dropParent.elements = [dragElement, ...dropParent.elements]
  return dropParent
}

function updateElementElements(element) {
  switch(element.model) {
    case 'questions.catalog':
      element.sections = element.elements.map((el, index) => ({ section: el.id, order: index }))
      break
    case 'questions.section':
      element.pages = element.elements.map((el, index) => ({ page: el.id, order: index }))
      break
    case 'questions.page':
    case 'questions.questionset':
      element.questions = element.elements.reduce((questions, el, index) => {
        if (el.model == 'questions.question') {
          questions.push({ question: el.id, order: index })
        }
        return questions
      }, [])
      element.questionsets = element.elements.reduce((questionsets, el, index) => {
        if (el.model == 'questions.questionset') {
          questionsets.push({ questionset: el.id, order: index })
        }
        return questionsets
      }, [])
      break
  }
}

function findDescendants(element, elementType) {
  if (elementType == elementTypes[element.model]) {
    return [element]
  } else if (!isUndefined(element.elements)) {
    return element.elements.reduce((agg, cur) => {
      const descendants = findDescendants(cur, elementType)
      if (!isNil(descendants)) {
        agg = agg.concat(descendants)
      }
      return agg
    }, [])
  } else {
    return null
  }
}

const buildUri = (element) => {
  if (isUndefined(element.uri_prefix) || isUndefined(element.model)) {
    return null
  }

  let uri = `${element.uri_prefix}/${elementModules[element.model]}/`

  if (!isUndefined(element.uri_path) && !isNil(element.uri_path)) {
    uri += element.uri_path
  } else if (!isUndefined(element.path) && !isNil(element.path)) {
    uri += element.path
  } else if (!isUndefined(element.key) && !isNil(element.key)) {
    uri += element.key
  } else {
    return null
  }

  return uri
}

const buildPathForAttribute = (key, parentUri) => {
  let path = key
  if (parentUri) {
     if (parentUri.includes('/domain/')) {
      // construct the path using parentUri directly
      const parentPath = parentUri.split('/domain/')[1]
      path = parentPath ? `${parentPath}/${key}` : key
    }
  }

  return path
}



export { compareElements, updateElement, resetElement, canMoveElement, moveElement, findDescendants, buildUri, buildPathForAttribute }
