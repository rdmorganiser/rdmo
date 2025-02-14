import { get, isNil } from 'lodash'

import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

import ConditionsApi from '../api/ConditionsApi'
import DomainApi from '../api/DomainApi'
import OptionsApi from '../api/OptionsApi'
import QuestionsApi from '../api/QuestionsApi'
import TasksApi from '../api/TasksApi'
import ViewsApi from '../api/ViewsApi'

import ConditionsFactory from '../factories/ConditionsFactory'
import DomainFactory from '../factories/DomainFactory'
import OptionsFactory from '../factories/OptionsFactory'
import QuestionsFactory from '../factories/QuestionsFactory'
import TasksFactory from '../factories/TasksFactory'
import ViewsFactory from '../factories/ViewsFactory'

import { elementTypes } from '../constants/elements'
import { updateLocation } from '../utils/location'
import { canMoveElement, findDescendants, moveElement } from '../utils/elements'

export function fetchElements(elementType) {
  const pendingId = `fetchElements/${elementType}`

  return function(dispatch) {
    updateLocation(elementType)

    dispatch(addToPending(pendingId))
    dispatch(fetchElementsInit(elementType))

    let action
    switch (elementType) {
      case 'catalogs':
        action = (dispatch) => QuestionsApi.fetchCatalogs(true)
          .then(catalogs => dispatch(fetchElementsSuccess({ catalogs })))
        break

      case 'sections':
        action = (dispatch) => QuestionsApi.fetchSections(true)
          .then(sections => dispatch(fetchElementsSuccess({ sections })))
        break

      case 'pages':
        action = (dispatch) => QuestionsApi.fetchPages(true)
          .then(pages => dispatch(fetchElementsSuccess({ pages })))
        break

      case 'questionsets':
        action = (dispatch) => QuestionsApi.fetchQuestionSets(true)
          .then(questionsets => dispatch(fetchElementsSuccess({ questionsets })))
        break

      case 'questions':
        action = (dispatch) => QuestionsApi.fetchQuestions(true)
          .then(questions => dispatch(fetchElementsSuccess({ questions })))
        break

      case 'attributes':
        action = (dispatch) => DomainApi.fetchAttributes(true)
          .then(attributes => dispatch(fetchElementsSuccess({ attributes })))
        break

      case 'optionsets':
        action = (dispatch) => OptionsApi.fetchOptionSets(true)
          .then(optionsets => dispatch(fetchElementsSuccess({ optionsets })))
        break

      case 'options':
        action = (dispatch) => OptionsApi.fetchOptions(true)
          .then(options => dispatch(fetchElementsSuccess({ options })))
        break

      case 'conditions':
        action = (dispatch) => ConditionsApi.fetchConditions(true)
          .then(conditions => dispatch(fetchElementsSuccess({ conditions })))
        break

      case 'tasks':
        action = (dispatch) => TasksApi.fetchTasks(true)
          .then(tasks => dispatch(fetchElementsSuccess({ tasks })))
        break

      case 'views':
        action = (dispatch) => ViewsApi.fetchViews(true)
          .then(views => dispatch(fetchElementsSuccess({ views })))
        break
    }

    return dispatch(action)
      .catch(error => dispatch(fetchElementsError(error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function fetchElementsInit(elementType) {
  return {type: 'elements/fetchElementsInit', elementType}
}

export function fetchElementsSuccess(elements) {
  return {type: 'elements/fetchElementsSuccess', elements}
}

export function fetchElementsError(error) {
  return {type: 'elements/fetchElementsError', error}
}

// fetch element

export function fetchElement(elementType, elementId, elementAction=null) {
  const pendingId = `fetchElement/${elementType}/${elementId}` + (isNil(elementAction) ? '' : `/${elementAction}`)

  return function(dispatch, getState) {
    updateLocation(elementType, elementId, elementAction)

    dispatch(addToPending(pendingId))
    dispatch(fetchElementInit(elementType, elementId, elementAction))

    let action
    switch (elementType) {
      case 'catalogs':
        if (elementAction == 'nested') {
          action = () => QuestionsApi.fetchCatalog(elementId, 'nested')
            .then(element => ({ element }))
        } else {
          action = () => Promise.all([
            QuestionsApi.fetchCatalog(elementId),
            QuestionsApi.fetchSections('index')
          ]).then(([element, sections]) => ({
            element, sections
          }))
        }
        break

      case 'sections':
        if (elementAction == 'nested') {
          action = () => QuestionsApi.fetchSection(elementId, 'nested')
            .then(element => ({ element }))
        } else {
          action = () => Promise.all([
            QuestionsApi.fetchSection(elementId),
            QuestionsApi.fetchCatalogs('index'),
            QuestionsApi.fetchPages('index'),
          ]).then(([element, catalogs, pages]) => {
            if (elementAction == 'copy') {
              delete element.catalogs
            }
            return {
              element, catalogs, pages
            }
          })
        }
        break

      case 'pages':
        if (elementAction == 'nested') {
          action = () => QuestionsApi.fetchPage(elementId, 'nested')
            .then(element => ({ element }))
        } else {
          action = () => Promise.all([
            QuestionsApi.fetchPage(elementId),
            DomainApi.fetchAttributes('index'),
            ConditionsApi.fetchConditions('index'),
            QuestionsApi.fetchSections('index'),
            QuestionsApi.fetchQuestionSets('index'),
            QuestionsApi.fetchQuestions('index')
          ]).then(([element, attributes, conditions, sections,
                    questionsets, questions]) => {
            if (elementAction == 'copy') {
              delete element.sections
            }

            return {
              element, attributes, conditions, sections, questionsets, questions
            }
          })
        }
        break

      case 'questionsets':
        if (elementAction == 'nested') {
          action = () => QuestionsApi.fetchQuestionSet(elementId, 'nested')
            .then(element => ({ element }))
        } else {
          action = () => Promise.all([
            QuestionsApi.fetchQuestionSet(elementId),
            DomainApi.fetchAttributes('index'),
            ConditionsApi.fetchConditions('index'),
            QuestionsApi.fetchPages('index'),
            QuestionsApi.fetchQuestionSets('index'),
            QuestionsApi.fetchQuestions('index')
          ]).then(([element, attributes, conditions, pages,
                    questionsets, questions]) => {
            if (elementAction == 'copy') {
              delete element.pages
              delete element.parents
            }

            return {
             element, attributes, conditions, pages, questionsets, questions
            }
          })
        }
        break

      case 'questions':
        if (elementAction == 'nested') {
          action = () => QuestionsApi.fetchQuestion(elementId, 'nested')
            .then(element => ({ element }))
        } else {
          action = () => Promise.all([
            QuestionsApi.fetchQuestion(elementId),
            DomainApi.fetchAttributes('index'),
            OptionsApi.fetchOptionSets('index'),
            OptionsApi.fetchOptions('index'),
            ConditionsApi.fetchConditions('index'),
            QuestionsApi.fetchPages('index'),
            QuestionsApi.fetchQuestionSets('index')
          ]).then(([element, attributes, optionsets, options, conditions,
                    pages, questionsets]) => {
            if (elementAction == 'copy') {
              delete element.pages
              delete element.questionsets
            }

            return {
              element, attributes, optionsets, options, conditions, pages, questionsets
            }
          })
        }
        break

      case 'attributes':
        if (elementAction == 'nested') {
          action = () => DomainApi.fetchAttribute(elementId, 'nested')
            .then(element => ({ element }))
        } else {
          action = () => Promise.all([
            DomainApi.fetchAttribute(elementId),
            DomainApi.fetchAttributes('index'),
            ConditionsApi.fetchConditions('index'),
            QuestionsApi.fetchPages('index'),
            QuestionsApi.fetchQuestionSets('index'),
            QuestionsApi.fetchQuestions('index'),
            TasksApi.fetchTasks('index'),
          ]).then(([element, attributes, conditions, pages, questionsets,
                    questions, tasks]) => {
              if (elementAction == 'copy') {
                delete element.conditions
                delete element.pages
                delete element.questionsets
                delete element.questions
                delete element.tasks
              }

            return {
            element, attributes, conditions, pages, questionsets, questions, tasks
            }
          })
        }
        break

      case 'optionsets':
        if (elementAction == 'nested') {
          action = () => OptionsApi.fetchOptionSet(elementId, 'nested')
            .then(element => ({ element }))
        } else {
          action = () => Promise.all([
            OptionsApi.fetchOptionSet(elementId),
            ConditionsApi.fetchConditions('index'),
            OptionsApi.fetchOptions('index'),
            QuestionsApi.fetchQuestions('index')
          ]).then(([element, conditions, options, questions]) => {
            if (elementAction == 'copy') {
              delete element.questions
            }
            return {
              element, conditions, options, questions
            }
          })
        }
        break

      case 'options':
        action = () => Promise.all([
          OptionsApi.fetchOption(elementId),
          OptionsApi.fetchOptionSets('index'),
          ConditionsApi.fetchConditions('index'),
        ]).then(([element, optionsets, conditions]) => {
          if (elementAction == 'copy') {
            delete element.optionsets
            delete element.conditions
          }
          return {
            element, optionsets, conditions
          }
        })
        break

      case 'conditions':
        action = () => Promise.all([
          ConditionsApi.fetchCondition(elementId),
          DomainApi.fetchAttributes('index'),
          OptionsApi.fetchOptionSets('index'),
          OptionsApi.fetchOptions('index'),
          QuestionsApi.fetchPages('index'),
          QuestionsApi.fetchQuestionSets('index'),
          QuestionsApi.fetchQuestions('index'),
          TasksApi.fetchTasks('index'),
        ]).then(([element, attributes, optionsets, options,
                  pages, questionsets, questions, tasks]) => {
           if (elementAction == 'copy') {
            delete element.optionsets
            delete element.pages
            delete element.questionsets
            delete element.questions
            delete element.tasks
          }
           return {
             element, attributes, optionsets, options, pages, questionsets, questions, tasks
           }
        })
        break

      case 'tasks':
        action = () => Promise.all([
          TasksApi.fetchTask(elementId),
          DomainApi.fetchAttributes('index'),
          ConditionsApi.fetchConditions('index'),
          QuestionsApi.fetchCatalogs('index')
        ]).then(([element, attributes, conditions, catalogs]) => ({
          element, attributes, conditions, catalogs
        }))
        break

      case 'views':
        action = () => Promise.all([
          ViewsApi.fetchView(elementId),
          QuestionsApi.fetchCatalogs('index')
        ]).then(([element, catalogs]) => ({
          element, catalogs
        }))
        break
    }

    return dispatch(action)
      .then(elements => {
        if (elementAction == 'copy') {
          const { settings, currentSite } = getState().config

          elements.element.id = null
          elements.element.read_only = false

          if (settings.multisite) {
            elements.element.sites = [currentSite.id]
            elements.element.editors = [currentSite.id]
          }
        }
        return dispatch(fetchElementSuccess({ ...elements }))
      })
      .catch(error => dispatch(fetchElementError(error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function fetchElementInit(elementType, elementId, elementAction) {
  return {type: 'elements/fetchElementInit', elementType, elementId, elementAction}
}

export function fetchElementSuccess(elements) {
  return {type: 'elements/fetchElementSuccess', elements}
}

export function fetchElementError(error) {
  return {type: 'elements/fetchElementError', error}
}

// store element

export function storeElement(elementType, element, elementAction = null, back = false) {
  const pendingId = `storeElement/${elementType}` + (isNil(element.id) ? '' : `/${element.id}`)
                                                  + (isNil(elementAction) ? '' : `/${elementAction}`)

  return function(dispatch, getState) {

    dispatch(addToPending(pendingId))
    dispatch(storeElementInit(element))

    let action
    switch (elementType) {
      case 'catalogs':
        action = () => QuestionsApi.storeCatalog(element, elementAction)
        break

      case 'sections':
        action = () => QuestionsApi.storeSection(element)
        break

      case 'pages':
        action = () => QuestionsApi.storePage(element)
        break

      case 'questionsets':
        action = () => QuestionsApi.storeQuestionSet(element)
        break

      case 'questions':
        action = () => QuestionsApi.storeQuestion(element)
        break

      case 'attributes':
        action = () => DomainApi.storeAttribute(element)
        break

      case 'optionsets':
        action = () => OptionsApi.storeOptionSet(element)
        break

      case 'options':
        action = () => OptionsApi.storeOption(element)
        break

      case 'conditions':
        action = () => ConditionsApi.storeCondition(element)
        break

      case 'tasks':
        action = () => TasksApi.storeTask(element, elementAction)
        break

      case 'views':
        action = () => ViewsApi.storeView(element, elementAction)
        break
    }

    return dispatch(action)
      .then(element => {
        dispatch(storeElementSuccess(element))
        if (back) {
          history.back()
        } else if (['create', 'copy'].includes(getState().elements.elementAction)) {
          dispatch(fetchElement(getState().elements.elementType, element.id))
        }
      })
      .catch(error => dispatch(storeElementError(element, error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function storeElementInit(element) {
  return {type: 'elements/storeElementInit', element}
}

export function storeElementSuccess(element) {
  return {type: 'elements/storeElementSuccess', element}
}

export function storeElementError(element, error) {
  return {type: 'elements/storeElementError', element, error}
}

// createElement

export function createElement(elementType, parent={}) {
  const pendingId = `createElement/${elementType}`

  return function(dispatch, getState) {
    updateLocation(elementType, null, 'create')

    dispatch(addToPending(pendingId))
    dispatch(createElementInit(elementType))

    let action
    switch (elementType) {
      case 'catalogs':
        action = () => Promise.all([
          QuestionsFactory.createCatalog(getState().config),
          QuestionsApi.fetchSections('index')
        ]).then(([element, sections]) => ({
          element, sections
        }))
        break

      case 'sections':
        action = () => Promise.all([
          QuestionsFactory.createSection(getState().config, parent),
          QuestionsApi.fetchPages('index'),
        ]).then(([element, pages]) => ({
          element, parent, pages
        }))
        break

      case 'pages':
        action = () => Promise.all([
          QuestionsFactory.createPage(getState().config, parent),
          DomainApi.fetchAttributes('index'),
          ConditionsApi.fetchConditions('index'),
          QuestionsApi.fetchQuestionSets('index'),
          QuestionsApi.fetchQuestions('index')
        ]).then(([element, attributes, conditions,
                  questionsets, questions]) => ({
          element, parent, attributes, conditions, questionsets, questions
        }))
        break

      case 'questionsets':
        action = () => Promise.all([
          QuestionsFactory.createQuestionSet(getState().config, parent),
          DomainApi.fetchAttributes('index'),
          ConditionsApi.fetchConditions('index'),
          QuestionsApi.fetchQuestionSets('index'),
          QuestionsApi.fetchQuestions('index')
        ]).then(([element, attributes, conditions,
                  questionsets, questions]) => ({
          element, parent, attributes, conditions, questionsets, questions
        }))
        break

      case 'questions':
        action = () => Promise.all([
          QuestionsFactory.createQuestion(getState().config, parent),
          DomainApi.fetchAttributes('index'),
          OptionsApi.fetchOptionSets('index'),
          OptionsApi.fetchOptions('index'),
          ConditionsApi.fetchConditions('index'),
          QuestionsApi.fetchWidgetTypes(),
          QuestionsApi.fetchValueTypes()
        ]).then(([element, attributes, optionsets,
                  options, conditions]) => ({
            element, parent, attributes, optionsets, options, conditions
          }))
        break

      case 'attributes':
        action = () => Promise.all([
          DomainFactory.createAttribute(getState().config, parent),
          DomainApi.fetchAttributes('index'),
        ]).then(([element, attributes]) => ({
            element, parent, attributes
          }))
        break

      case 'optionsets':
        action = () => Promise.all([
          OptionsFactory.createOptionSet(getState().config, parent),
          OptionsApi.fetchOptions('index'),
        ]).then(([element, options]) => ({
            element, parent, options
          }))
        break

      case 'options':
        action = () => Promise.all([
          OptionsFactory.createOption(getState().config, parent),
          OptionsApi.fetchOptionSets('index'),
        ]).then(([element, optionsets]) => ({
            element, parent, optionsets
          }))
        break

      case 'conditions':
        action = () => Promise.all([
          ConditionsFactory.createCondition(getState().config, parent),
          DomainApi.fetchAttributes('index'),
          OptionsApi.fetchOptions('index'),
        ]).then(([element, attributes, options]) => ({
            element, parent, attributes, options
          }))
        break

      case 'tasks':
        action = () => Promise.all([
          TasksFactory.createTask(getState().config),
          DomainApi.fetchAttributes('index'),
          ConditionsApi.fetchConditions('index'),
          QuestionsApi.fetchCatalogs('index')
        ]).then(([element, attributes, conditions, catalogs]) => ({
            element, attributes, conditions, catalogs
          }))
        break

      case 'views':
        action = () => Promise.all([
          ViewsFactory.createView(getState().config),
          QuestionsApi.fetchCatalogs('index')
        ]).then(([element, catalogs]) => ({
          element, catalogs
        }))
        break
    }

    return dispatch(action)
      .then(elements => dispatch(createElementSuccess({...elements})))
      .catch(error => dispatch(createElementError(error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function createElementInit(elementType) {
  return {type: 'elements/createElementInit', elementType}
}

export function createElementSuccess(elements) {
  return {type: 'elements/createElementSuccess', elements}
}

export function createElementError(error) {
  return {type: 'elements/createElementError', error}
}

// delete element

export function deleteElement(elementType, element) {
  const pendingId = `deleteElement/${elementType}/${element.id}`

  return function(dispatch) {
    dispatch(addToPending(pendingId))
    dispatch(deleteElementInit(element))

    let action
    switch (elementType) {
      case 'catalogs':
        action = () => QuestionsApi.deleteCatalog(element)
        break
      case 'sections':
        action = () => QuestionsApi.deleteSection(element)
        break

      case 'pages':
        action = () => QuestionsApi.deletePage(element)
        break

      case 'questionsets':
        action = () => QuestionsApi.deleteQuestionSet(element)
        break

      case 'questions':
        action = () => QuestionsApi.deleteQuestion(element)
        break

      case 'attributes':
        action = () => DomainApi.deleteAttribute(element)
        break

      case 'optionsets':
        action = () => OptionsApi.deleteOptionSet(element)
        break

      case 'options':
        action = () => OptionsApi.deleteOption(element)
        break

      case 'conditions':
        action = () => ConditionsApi.deleteCondition(element)

        break

      case 'tasks':
        action = () => TasksApi.deleteTask(element)
        break

      case 'views':
        action = () => ViewsApi.deleteView(element)
        break
    }

    return dispatch(action)
      .then(() => {
        dispatch(deleteElementSuccess(element))
        history.back()
      })
      .catch(error => dispatch(deleteElementError(element, error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function deleteElementInit(element) {
  return {type: 'elements/deleteElementInit', element}
}

export function deleteElementSuccess(element) {
  return {type: 'elements/deleteElementSuccess', element}
}

export function deleteElementError(element, error) {
  return {type: 'elements/deleteElementError', element, error}
}

// update elements

export function updateElement(element, values) {
  return {type: 'elements/updateElement', element, values}
}

// move elements

export function dropElement(dragElement, dropElement, mode) {
  return function(dispatch, getState) {
    // an element cannot be dropped on itself or on one of its descendants
    if (canMoveElement(dragElement, dropElement)) {
      const element = {...getState().elements.element}
      const { dragParent, dropParent } = moveElement(element, dragElement, dropElement, mode)

    dispatch(storeElement(elementTypes[dragParent.model], dragParent))
    if (!isNil(dropParent)) {
      dispatch(storeElement(elementTypes[dropParent.model], dropParent))
      }
    }
  }
}

// toggle elements

export function toggleElements(element) {
  return (dispatch, getState) => {
    const path = `display.elements.${elementTypes[element.model]}.${element.id}`
    const value = !get(getState().config, path, true)
    dispatch(updateConfig(path, value))
  }
}

export function toggleDescendants(element, elementType) {
  return (dispatch) => {
    findDescendants(element, elementType).forEach(e => dispatch(toggleElements(e)))
  }
}
