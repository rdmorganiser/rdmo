import isNil from 'lodash/isNil'

import CoreApi from 'rdmo/core/assets/js/api/CoreApi'

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

import { updateLocation } from '../utils/location'

export function fetchElements(elementType) {
  return function(dispatch, getState) {
    updateLocation(getState().config.baseUrl, elementType)

    dispatch(fetchElementsInit(elementType))

    let action
    switch (elementType) {
      case 'catalogs':
        action = (dispatch, getState) => QuestionsApi.fetchCatalogs(true)
          .then(catalogs => dispatch(fetchElementsSuccess({ catalogs })))
        break

      case 'sections':
        action = (dispatch, getState) => QuestionsApi.fetchSections(true)
          .then(sections => dispatch(fetchElementsSuccess({ sections })))
        break

      case 'pages':
        action = (dispatch, getState) => QuestionsApi.fetchPages(true)
          .then(pages => dispatch(fetchElementsSuccess({ pages })))
        break

      case 'questionsets':
        action = (dispatch, getState) => QuestionsApi.fetchQuestionSets(true)
          .then(questionsets => dispatch(fetchElementsSuccess({ questionsets })))
        break

      case 'questions':
        action = (dispatch, getState) => QuestionsApi.fetchQuestions(true)
          .then(questions => dispatch(fetchElementsSuccess({ questions })))
        break

      case 'attributes':
        action = (dispatch, getState) => DomainApi.fetchAttributes(true)
          .then(attributes => dispatch(fetchElementsSuccess({ attributes })))
        break

      case 'optionsets':
        action = (dispatch, getState) => OptionsApi.fetchOptionSets(true)
          .then(optionsets => dispatch(fetchElementsSuccess({ optionsets })))
        break

      case 'options':
        action = (dispatch, getState) => OptionsApi.fetchOptions(true)
          .then(options => dispatch(fetchElementsSuccess({ options })))
        break

      case 'conditions':
        action = (dispatch, getState) => ConditionsApi.fetchConditions(true)
          .then(conditions => dispatch(fetchElementsSuccess({ conditions })))
        break

      case 'tasks':
        action = (dispatch, getState) => TasksApi.fetchTasks(true)
          .then(tasks => dispatch(fetchElementsSuccess({ tasks })))
        break

      case 'views':
        action = (dispatch, getState) => ViewsApi.fetchViews(true)
          .then(views => dispatch(fetchElementsSuccess({ views })))
        break
    }

    dispatch(action)
      .catch(error => dispatch(fetchElementsError(error)))
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

export function fetchElement(elementType, elementId, elementAction) {
  return function(dispatch, getState) {
    if (isNil(elementAction)) elementAction = null

    updateLocation(getState().config.baseUrl, elementType, elementId, elementAction)

    dispatch(fetchElementInit(elementType, elementId, elementAction))

    let action
    switch (elementType) {
      case 'catalogs':
        if (elementAction == 'nested') {
          action = (dispatch, getState) => QuestionsApi.fetchCatalog(elementId, 'nested')
            .then(element => dispatch(fetchElementSuccess({ element })))
        } else {
          action = (dispatch, getState) => Promise.all([
            QuestionsApi.fetchCatalog(elementId),
            QuestionsApi.fetchSections('index'),
            CoreApi.fetchGroups(),
            CoreApi.fetchSites(),
          ]).then(([element, sections, groups, sites]) => dispatch(fetchElementSuccess({
            element, sections, groups, sites
          })))
        }
        break

      case 'sections':
        if (elementAction == 'nested') {
          action = (dispatch, getState) => QuestionsApi.fetchSection(elementId, 'nested')
            .then(element => dispatch(fetchElementSuccess({ element })))
        } else {
          action = (dispatch, getState) => Promise.all([
            QuestionsApi.fetchSection(elementId),
            QuestionsApi.fetchPages('index'),
          ]).then(([element, pages]) => dispatch(fetchElementSuccess({
            element, pages
          })))
        }
        break

      case 'pages':
        if (elementAction == 'nested') {
          action = (dispatch, getState) => QuestionsApi.fetchPage(elementId, 'nested')
            .then(element => dispatch(fetchElementSuccess({ element })))
        } else {
          action = (dispatch, getState) => Promise.all([
            QuestionsApi.fetchPage(elementId),
            DomainApi.fetchAttributes('index'),
            ConditionsApi.fetchConditions('index'),
            QuestionsApi.fetchQuestionSets('index'),
            QuestionsApi.fetchQuestions('index')
          ]).then(([element, attributes, conditions, questionsets,
                    questions]) => dispatch(fetchElementSuccess({
            element, attributes, conditions, questionsets, questions
          })))
        }
        break

      case 'questionsets':
        if (elementAction == 'nested') {
          action = (dispatch, getState) => QuestionsApi.fetchQuestionSet(elementId, 'nested')
            .then(element => dispatch(fetchElementSuccess({ element })))
        } else {
          action = (dispatch, getState) => Promise.all([
            QuestionsApi.fetchQuestionSet(elementId),
            DomainApi.fetchAttributes('index'),
            ConditionsApi.fetchConditions('index'),
            QuestionsApi.fetchQuestionSets('index'),
            QuestionsApi.fetchQuestions('index')
          ]).then(([element, attributes, conditions, questionsets,
                    questions]) => dispatch(fetchElementSuccess({
            element, attributes, conditions, questionsets, questions
          })))
        }
        break

      case 'questions':
        if (elementAction == 'nested') {
          action = (dispatch, getState) => QuestionsApi.fetchQuestion(elementId, 'nested')
            .then(element => dispatch(fetchElementSuccess({ element })))
        } else {
          action = (dispatch, getState) => Promise.all([
            QuestionsApi.fetchQuestion(elementId),
            DomainApi.fetchAttributes('index'),
            OptionsApi.fetchOptionSets('index'),
            OptionsApi.fetchOptions('index'),
            ConditionsApi.fetchConditions('index'),
            QuestionsApi.fetchWidgetTypes(),
            QuestionsApi.fetchValueTypes()
          ]).then(([element, attributes, optionsets, options, conditions,
                    widgetTypes, valueTypes]) => dispatch(fetchElementSuccess({
            element, attributes, optionsets, options, conditions, widgetTypes, valueTypes
          })))
        }
        break

      case 'attributes':
        if (elementAction == 'nested') {
          action = (dispatch, getState) => DomainApi.fetchAttribute(elementId, 'nested')
            .then(element => dispatch(fetchElementSuccess({ element })))
        } else {
          action = (dispatch, getState) => Promise.all([
            DomainApi.fetchAttribute(elementId),
            DomainApi.fetchAttributes('index'),
          ]).then(([element, attributes]) => dispatch(fetchElementSuccess({
            element, attributes
          })))
        }
        break

      case 'optionsets':
        if (elementAction == 'nested') {
          action = (dispatch, getState) => OptionsApi.fetchOptionSet(elementId, 'nested')
            .then(element => dispatch(fetchElementSuccess({element })))
        } else {
          action = (dispatch, getState) => Promise.all([
            OptionsApi.fetchOptionSet(elementId),
            OptionsApi.fetchOptions('index'),
            OptionsApi.fetchProviders(),
          ]).then(([element, options, providers]) => dispatch(fetchElementSuccess({
            element, options, providers
          })))
        }
        break

      case 'options':
        action = (dispatch, getState) => Promise.all([
          OptionsApi.fetchOption(elementId),
          OptionsApi.fetchOptionSets('index'),
        ]).then(([element, optionsets]) => dispatch(fetchElementSuccess({
          element, optionsets
        })))
        break

      case 'conditions':
        action = (dispatch, getState) => Promise.all([
          ConditionsApi.fetchCondition(elementId),
          ConditionsApi.fetchRelations(),
          DomainApi.fetchAttributes('index'),
          OptionsApi.fetchOptions('index'),
        ]).then(([element, relations, attributes, options]) => dispatch(fetchElementSuccess({
          element, relations, attributes, options
        })))
        break

      case 'tasks':
        action = (dispatch, getState) => Promise.all([
          TasksApi.fetchTask(elementId),
          DomainApi.fetchAttributes('index'),
          ConditionsApi.fetchConditions('index'),
          QuestionsApi.fetchCatalogs('index'),
          CoreApi.fetchSites(),
          CoreApi.fetchGroups()
        ]).then(([element, attributes, conditions, catalogs,
                  sites, groups]) => dispatch(fetchElementSuccess({
          element, attributes, conditions, catalogs, sites, groups
        })))
        break

      case 'views':
        action = (dispatch, getState) => Promise.all([
          ViewsApi.fetchView(elementId),
          QuestionsApi.fetchCatalogs('index'),
          CoreApi.fetchSites(),
          CoreApi.fetchGroups()
        ]).then(([element, catalogs, sites, groups]) => dispatch(fetchElementSuccess({
          element, sites, groups, catalogs
        })))
        break
    }

    dispatch(action)
      .catch(error => dispatch(fetchElementError(error)))
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

export function storeElement(elementType, element) {
  return function(dispatch, getState) {
    dispatch(storeElementInit(element))

    let action
    switch (elementType) {
      case 'catalogs':
        action = (dispatch, getState) => QuestionsApi.storeCatalog(element)
          .then(element => dispatch(storeElementSuccess(element)))
        break

      case 'sections':
        action = (dispatch, getState) => QuestionsApi.storeSection(element)
          .then(element => dispatch(storeElementSuccess(element)))
        break

      case 'pages':
        action = (dispatch, getState) => QuestionsApi.storePage(element)
          .then(element => dispatch(storeElementSuccess(element)))
        break

      case 'questionsets':
        action = (dispatch, getState) => QuestionsApi.storeQuestionSet(element)
          .then(element => dispatch(storeElementSuccess(element)))
        break

      case 'questions':
        action = (dispatch, getState) => QuestionsApi.storeQuestion(element)
          .then(element => dispatch(storeElementSuccess(element)))
        break

      case 'attributes':
        action = (dispatch, getState) => DomainApi.storeAttribute(element)
          .then(element => dispatch(storeElementSuccess(element)))
        break

      case 'optionsets':
        action = (dispatch, getState) => OptionsApi.storeOptionSet(element)
          .then(element => dispatch(storeElementSuccess(element)))
        break

      case 'options':
        action = (dispatch, getState) => OptionsApi.storeOption(element)
          .then(element => dispatch(storeElementSuccess(element)))
        break

      case 'conditions':
        action = (dispatch, getState) => ConditionsApi.storeCondition(element)
          .then(element => dispatch(storeElementSuccess(element)))
        break

      case 'tasks':
        action = (dispatch, getState) => TasksApi.storeTask(element)
          .then(element => dispatch(storeElementSuccess(element)))
        break

      case 'views':
        action = (dispatch, getState) => ViewsApi.storeView(element)
          .then(element => dispatch(storeElementSuccess(element)))
        break
    }

    dispatch(action)
      .catch(error => dispatch(storeElementError(element, error)))
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

export function createElement(elementType) {
  return function(dispatch, getState) {
    updateLocation(getState().config.baseUrl, elementType, null, 'create')

    dispatch(createElementInit(elementType))
    dispatch(startPending())

    switch (elementType) {
      case 'catalogs':
        dispatch(createCatalog())
        break
      case 'sections':
        dispatch(createSection())
        break
      case 'pages':
        dispatch(createPage())
        break
      case 'questionsets':
        dispatch(createQuestionSet())
        break
      case 'questions':
        dispatch(createQuestion())
        break
      case 'attributes':
        dispatch(createAttribute())
        break
      case 'optionsets':
        dispatch(createOptionSet())
        break
      case 'options':
        dispatch(createOption())
        break
      case 'conditions':
        dispatch(createCondition())
        break
      case 'tasks':
        dispatch(createTask())
        break
      case 'views':
        dispatch(createView())
        break
      default:
        dispatch(stopPending())
    }
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

export function createCatalog() {
  return function(dispatch) {
    return Promise.all([
      QuestionsFactory.createCatalog(),
      QuestionsApi.fetchSections('index'),
      CoreApi.fetchGroups(),
      CoreApi.fetchSites(),
    ]).then(([element, sections, groups, sites]) => {
      dispatch(stopPending())
      dispatch(createElementSuccess({
        element, sections, groups, sites
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(createElementError(error))
    })
  }
}

export function createSection() {
  return function(dispatch) {
    return Promise.all([
      QuestionsFactory.createSection(),
      QuestionsApi.fetchPages('index'),
    ]).then(([element, pages]) => {
      dispatch(stopPending())
      dispatch(createElementSuccess({
        element, pages
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(createElementError(error))
    })
  }
}

export function createPage() {
  return function(dispatch) {
    return Promise.all([
      QuestionsFactory.createPage(),
      DomainApi.fetchAttributes('index'),
      ConditionsApi.fetchConditions('index'),
      QuestionsApi.fetchQuestionSets('index'),
      QuestionsApi.fetchQuestions('index')
    ]).then(([element, attributes, conditions, questionsets, questions]) => {
      dispatch(stopPending())
      dispatch(createElementSuccess({
        element, attributes, conditions, questionsets, questions
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(createElementError(error))
    })
  }
}

export function createQuestionSet() {
  return function(dispatch) {
    return Promise.all([
      QuestionsFactory.createQuestionSet(),
      DomainApi.fetchAttributes('index'),
      ConditionsApi.fetchConditions('index'),
      QuestionsApi.fetchQuestionSets('index'),
      QuestionsApi.fetchQuestions('index')
    ]).then(([element, attributes, conditions, questionsets, questions]) => {
      dispatch(stopPending())
      dispatch(createElementSuccess({
        element, attributes, conditions, questionsets, questions
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(createElementError(error))
    })
  }
}

export function createQuestion() {
  return function(dispatch) {
    return Promise.all([
      QuestionsFactory.createQuestion(),
      DomainApi.fetchAttributes('index'),
      OptionsApi.fetchOptionSets('index'),
      OptionsApi.fetchOptions('index'),
      ConditionsApi.fetchConditions('index'),
      QuestionsApi.fetchWidgetTypes(),
      QuestionsApi.fetchValueTypes()
    ]).then(([element, attributes, optionsets, options, conditions, widgetTypes, valueTypes]) => {
      dispatch(stopPending())
      dispatch(createElementSuccess({
        element, attributes, optionsets, options, conditions, widgetTypes, valueTypes
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(createElementError(error))
    })
  }
}

export function createAttribute() {
  return function(dispatch) {
    return Promise.all([
      DomainFactory.createAttribute(),
      DomainApi.fetchAttributes('index'),
    ]).then(([element, attributes]) => {
      dispatch(stopPending())
      dispatch(createElementSuccess({
        element, attributes
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(createElementError(error))
    })
  }
}

export function createOptionSet() {
  return function(dispatch) {
    return Promise.all([
      OptionsFactory.createOptionSet(),
      OptionsApi.fetchOptions('index'),
      OptionsApi.fetchProviders(),
    ]).then(([element, options, providers]) => {
      dispatch(stopPending())
      dispatch(createElementSuccess({
        element, options, providers
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(createElementError(error))
    })
  }
}

export function createOption() {
  return function(dispatch) {
    return Promise.all([
      OptionsFactory.createOption(),
      OptionsApi.fetchOptionSets('index'),
    ]).then(([element, optionsets]) => {
      dispatch(stopPending())
      dispatch(createElementSuccess({
        element, optionsets
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(createElementError(error))
    })
  }
}

export function createCondition() {
  return function(dispatch) {
    return Promise.all([
      ConditionsFactory.createCondition(),
      ConditionsApi.fetchRelations(),
      DomainApi.fetchAttributes('index'),
      OptionsApi.fetchOptions('index'),
    ]).then(([element, relations, attributes, options]) => {
      dispatch(stopPending())
      dispatch(createElementSuccess({
        element, relations, attributes, options
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(createElementError(error))
    })
  }
}

export function createTask() {
  return function(dispatch) {
    return Promise.all([
      TasksFactory.createTask(),
      DomainApi.fetchAttributes('index'),
      ConditionsApi.fetchConditions('index'),
      QuestionsApi.fetchCatalogs('index'),
      CoreApi.fetchSites(),
      CoreApi.fetchGroups()
    ]).then(([element, attributes, conditions, catalogs, sites, groups]) => {
      dispatch(stopPending())
      dispatch(createElementSuccess({
        element, attributes, conditions, catalogs, sites, groups
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(createElementError(error))
    })
  }
}

export function createView() {
  return function(dispatch) {
    return Promise.all([
      ViewsFactory.createView(),
      QuestionsApi.fetchCatalogs('index'),
      CoreApi.fetchSites(),
      CoreApi.fetchGroups()
    ]).then(([element, catalogs, sites, groups]) => {
      dispatch(stopPending())
      dispatch(createElementSuccess({
        element, sites, groups, catalogs
      }))
    }).catch(error => {
      dispatch(stopPending())
      dispatch(createElementError(error))
    })
  }
}

// delete element

export function deleteElement(elementType, element) {
  return function(dispatch, getState) {
    dispatch(deleteElementInit(element))

    let action
    switch (elementType) {
      case 'catalogs':
        action = (dispatch, getState) => QuestionsApi.deleteCatalog(element)
        break

      case 'sections':
        action = (dispatch, getState) => QuestionsApi.deleteSection(element)
        break

      case 'pages':
        action = (dispatch, getState) => QuestionsApi.deletePage(element)
        break

      case 'questionsets':
        action = (dispatch, getState) => QuestionsApi.deleteQuestionSet(element)
        break

      case 'questions':
        action = (dispatch, getState) => QuestionsApi.deleteQuestion(element)
        break

      case 'attributes':
        action = (dispatch, getState) => DomainApi.deleteAttribute(element)
        break

      case 'optionsets':
        action = (dispatch, getState) => OptionsApi.deleteOptionSet(element)
        break

      case 'options':
        action = (dispatch, getState) => OptionsApi.deleteOption(element)
        break

      case 'conditions':
        action = (dispatch, getState) => ConditionsApi.deleteCondition(element)

        break

      case 'tasks':
        action = (dispatch, getState) => TasksApi.deleteTask(element)
        break

      case 'views':
        action = (dispatch, getState) => ViewsApi.deleteView(element)
        break
    }

    dispatch(action)
      .then(() => {
        dispatch(deleteElementSuccess(element))
        dispatch(fetchElements(elementType))
      })
      .catch(error => dispatch(deleteElementError(element, error)))
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

export function updateElement(element, field, value) {
  return {type: 'elements/updateElement', element, field, value}
}
