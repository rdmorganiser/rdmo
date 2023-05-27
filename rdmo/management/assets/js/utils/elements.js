import isEmpty from 'lodash/isEmpty';
import isNil from 'lodash/isNil';
import isUndefined from 'lodash/isUndefined';

import { elementModules } from '../constants/elements'

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
  if (!compareElements(dragParent, dropParent)) {
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
  console.log(dragElement.uri_path, dropElement.uri_path);
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
    case 'questions.section':
      element.pages = element.elements.map((el, index) => ({ page: el.id, order: index }))
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
  }
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

export { compareElements, updateElement, moveElement, buildUri }
