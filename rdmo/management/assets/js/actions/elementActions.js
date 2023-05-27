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
import { compareElements, moveElement } from '../utils/elements'

export function fetchElements(elementType) {
  return function(dispatch, getState) {
    updateLocation(getState().config.baseUrl, elementType)

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
  return function(dispatch, getState) {
    updateLocation(getState().config.baseUrl, elementType, elementId, elementAction)

    dispatch(fetchElementInit(elementType, elementId, elementAction))

    let action
    switch (elementType) {
      case 'catalogs':
        if (elementAction == 'nested') {
          action = (dispatch) => QuestionsApi.fetchCatalog(elementId, 'nested')
            .then(element => dispatch(fetchElementSuccess({ element })))
        } else {
          action = (dispatch) => Promise.all([
            QuestionsApi.fetchCatalog(elementId),
            QuestionsApi.fetchSections('index')
          ]).then(([element, sections]) => dispatch(fetchElementSuccess({
            element, sections
          })))
        }
        break

      case 'sections':
        if (elementAction == 'nested') {
          action = (dispatch) => QuestionsApi.fetchSection(elementId, 'nested')
            .then(element => dispatch(fetchElementSuccess({ element })))
        } else {
          action = (dispatch) => Promise.all([
            QuestionsApi.fetchSection(elementId),
            QuestionsApi.fetchCatalogs('index'),
            QuestionsApi.fetchPages('index'),
          ]).then(([element, catalogs, pages]) => dispatch(fetchElementSuccess({
            element, catalogs, pages
          })))
        }
        break

      case 'pages':
        if (elementAction == 'nested') {
          action = (dispatch) => QuestionsApi.fetchPage(elementId, 'nested')
            .then(element => dispatch(fetchElementSuccess({ element })))
        } else {
          action = (dispatch) => Promise.all([
            QuestionsApi.fetchPage(elementId),
            DomainApi.fetchAttributes('index'),
            ConditionsApi.fetchConditions('index'),
            QuestionsApi.fetchSections('index'),
            QuestionsApi.fetchQuestionSets('index'),
            QuestionsApi.fetchQuestions('index')
          ]).then(([element, attributes, conditions, sections,
                    questionsets, questions]) => dispatch(fetchElementSuccess({
            element, attributes, conditions, sections, questionsets, questions
          })))
        }
        break

      case 'questionsets':
        if (elementAction == 'nested') {
          action = (dispatch) => QuestionsApi.fetchQuestionSet(elementId, 'nested')
            .then(element => dispatch(fetchElementSuccess({ element })))
        } else {
          action = (dispatch) => Promise.all([
            QuestionsApi.fetchQuestionSet(elementId),
            DomainApi.fetchAttributes('index'),
            ConditionsApi.fetchConditions('index'),
            QuestionsApi.fetchPages('index'),
            QuestionsApi.fetchQuestionSets('index'),
            QuestionsApi.fetchQuestions('index')
          ]).then(([element, attributes, conditions, pages,
                    questionsets, questions]) => dispatch(fetchElementSuccess({
            element, attributes, conditions, pages, questionsets, questions
          })))
        }
        break

      case 'questions':
        if (elementAction == 'nested') {
          action = (dispatch) => QuestionsApi.fetchQuestion(elementId, 'nested')
            .then(element => dispatch(fetchElementSuccess({ element })))
        } else {
          action = (dispatch) => Promise.all([
            QuestionsApi.fetchQuestion(elementId),
            DomainApi.fetchAttributes('index'),
            OptionsApi.fetchOptionSets('index'),
            OptionsApi.fetchOptions('index'),
            ConditionsApi.fetchConditions('index'),
            QuestionsApi.fetchPages('index'),
            QuestionsApi.fetchQuestionSets('index')
          ]).then(([element, attributes, optionsets, options, conditions,
                    pages, questionsets]) => dispatch(fetchElementSuccess({
            element, attributes, optionsets, options, conditions, pages, questionsets,
          })))
        }
        break

      case 'attributes':
        if (elementAction == 'nested') {
          action = (dispatch) => DomainApi.fetchAttribute(elementId, 'nested')
            .then(element => dispatch(fetchElementSuccess({ element })))
        } else {
          action = (dispatch) => Promise.all([
            DomainApi.fetchAttribute(elementId),
            DomainApi.fetchAttributes('index'),
            ConditionsApi.fetchConditions('index'),
            QuestionsApi.fetchPages('index'),
            QuestionsApi.fetchQuestionSets('index'),
            QuestionsApi.fetchQuestions('index'),
            TasksApi.fetchTasks('index'),
          ]).then(([element, attributes, conditions, pages, questionsets,
                    questions, tasks]) => dispatch(fetchElementSuccess({
            element, attributes, conditions, pages, questionsets, questions, tasks
          })))
        }
        break

      case 'optionsets':
        if (elementAction == 'nested') {
          action = (dispatch) => OptionsApi.fetchOptionSet(elementId, 'nested')
            .then(element => dispatch(fetchElementSuccess({ element })))
        } else {
          action = (dispatch) => Promise.all([
            OptionsApi.fetchOptionSet(elementId),
            ConditionsApi.fetchConditions('index'),
            OptionsApi.fetchOptions('index'),
            QuestionsApi.fetchQuestions('index')
          ]).then(([element, conditions, options, questions]) => dispatch(fetchElementSuccess({
            element, conditions, options, questions
          })))
        }
        break

      case 'options':
        action = (dispatch) => Promise.all([
          OptionsApi.fetchOption(elementId),
          OptionsApi.fetchOptionSets('index'),
          ConditionsApi.fetchConditions('index'),
        ]).then(([element, optionsets, conditions]) => dispatch(fetchElementSuccess({
          element, optionsets, conditions
        })))
        break

      case 'conditions':
        action = (dispatch) => Promise.all([
          ConditionsApi.fetchCondition(elementId),
          DomainApi.fetchAttributes('index'),
          OptionsApi.fetchOptionSets('index'),
          OptionsApi.fetchOptions('index'),
          QuestionsApi.fetchPages('index'),
          QuestionsApi.fetchQuestionSets('index'),
          QuestionsApi.fetchQuestions('index'),
          TasksApi.fetchTasks('index'),
        ]).then(([element, attributes, optionsets, options,
                  pages, questionsets, questions, tasks]) => dispatch(fetchElementSuccess({
          element, attributes, optionsets, options, pages, questionsets, questions, tasks
        })))
        break

      case 'tasks':
        action = (dispatch) => Promise.all([
          TasksApi.fetchTask(elementId),
          DomainApi.fetchAttributes('index'),
          ConditionsApi.fetchConditions('index'),
          QuestionsApi.fetchCatalogs('index')
        ]).then(([element, attributes, conditions, catalogs]) => dispatch(fetchElementSuccess({
          element, attributes, conditions, catalogs
        })))
        break

      case 'views':
        action = (dispatch) => Promise.all([
          ViewsApi.fetchView(elementId),
          QuestionsApi.fetchCatalogs('index')
        ]).then(([element, catalogs]) => dispatch(fetchElementSuccess({
          element, catalogs
        })))
        break
    }

    return dispatch(action)
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

export function storeElement(elementType, element, back) {
  return function(dispatch, getState) {
    dispatch(storeElementInit(element))

    let action
    switch (elementType) {
      case 'catalogs':
        action = () => QuestionsApi.storeCatalog(element)
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
        action = () => TasksApi.storeTask(element)
        break

      case 'views':
        action = () => ViewsApi.storeView(element)
        break
    }

    return dispatch(action)
      .then(element => {
        dispatch(storeElementSuccess(element))
        if (back) {
          history.back()
        } else if (getState().elements.elementAction == 'create') {
          dispatch(fetchElement(getState().elements.elementType, element.id))
        }
      })
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

export function createElement(elementType, parent={}) {
  return function(dispatch, getState) {
    updateLocation(getState().config.baseUrl, elementType, null, 'create')

    dispatch(createElementInit(elementType))

    let action
    switch (elementType) {
      case 'catalogs':
        action = (dispatch) => Promise.all([
          QuestionsFactory.createCatalog(getState().config),
          QuestionsApi.fetchSections('index')
        ]).then(([element, sections]) => dispatch(createElementSuccess({
          element, sections
        })))
        break

      case 'sections':
        action = (dispatch) => Promise.all([
          QuestionsFactory.createSection(getState().config, parent),
          QuestionsApi.fetchPages('index'),
        ]).then(([element, pages]) => dispatch(createElementSuccess({
          element, parent, pages
        })))
        break

      case 'pages':
        action = (dispatch) => Promise.all([
          QuestionsFactory.createPage(getState().config, parent),
          DomainApi.fetchAttributes('index'),
          ConditionsApi.fetchConditions('index'),
          QuestionsApi.fetchQuestionSets('index'),
          QuestionsApi.fetchQuestions('index')
        ]).then(([element, attributes, conditions,
                  questionsets, questions]) => dispatch(createElementSuccess({
          element, parent, attributes, conditions, questionsets, questions
        })))
        break

      case 'questionsets':
        action = (dispatch) => Promise.all([
          QuestionsFactory.createQuestionSet(getState().config, parent),
          DomainApi.fetchAttributes('index'),
          ConditionsApi.fetchConditions('index'),
          QuestionsApi.fetchQuestionSets('index'),
          QuestionsApi.fetchQuestions('index')
        ]).then(([element, attributes, conditions,
                  questionsets, questions]) => dispatch(createElementSuccess({
          element, parent, attributes, conditions, questionsets, questions
        })))
        break

      case 'questions':
        action = (dispatch) => Promise.all([
          QuestionsFactory.createQuestion(getState().config, parent),
          DomainApi.fetchAttributes('index'),
          OptionsApi.fetchOptionSets('index'),
          OptionsApi.fetchOptions('index'),
          ConditionsApi.fetchConditions('index'),
          QuestionsApi.fetchWidgetTypes(),
          QuestionsApi.fetchValueTypes()
        ]).then(([element, attributes, optionsets,
                  options, conditions]) => dispatch(createElementSuccess({
            element, parent, attributes, optionsets, options, conditions
          })))
        break

      case 'attributes':
        action = (dispatch) => Promise.all([
          DomainFactory.createAttribute(getState().config, parent),
          DomainApi.fetchAttributes('index'),
        ]).then(([element, attributes]) => dispatch(createElementSuccess({
            element, parent, attributes
          })))
        break

      case 'optionsets':
        action = (dispatch) => Promise.all([
          OptionsFactory.createOptionSet(getState().config, parent),
          OptionsApi.fetchOptions('index'),
        ]).then(([element, options]) => dispatch(createElementSuccess({
            element, parent, options
          })))
        break

      case 'options':
        action = (dispatch) => Promise.all([
          OptionsFactory.createOption(getState().config, parent),
          OptionsApi.fetchOptionSets('index'),
        ]).then(([element, optionsets]) => dispatch(createElementSuccess({
            element, parent, optionsets
          })))
        break

      case 'conditions':
        action = (dispatch) => Promise.all([
          ConditionsFactory.createCondition(getState().config, parent),
          DomainApi.fetchAttributes('index'),
          OptionsApi.fetchOptions('index'),
        ]).then(([element, attributes, options]) => dispatch(createElementSuccess({
            element, parent, attributes, options
          })))
        break

      case 'tasks':
        action = (dispatch) => Promise.all([
          TasksFactory.createTask(getState().config),
          DomainApi.fetchAttributes('index'),
          ConditionsApi.fetchConditions('index'),
          QuestionsApi.fetchCatalogs('index')
        ]).then(([element, attributes, conditions, catalogs]) => dispatch(createElementSuccess({
            element, attributes, conditions, catalogs
          })))
        break

      case 'views':
        action = (dispatch) => Promise.all([
          ViewsFactory.createView(getState().config),
          QuestionsApi.fetchCatalogs('index')
        ]).then(([element, catalogs]) => dispatch(createElementSuccess({
          element, catalogs
        })))
        break
    }

    return dispatch(action)
      .catch(error => dispatch(createElementError(error)))
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
  return function(dispatch) {
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
    if (!compareElements(dragElement, dropElement)) {
      const element = {...getState().elements.element}
      const { dragParent, dropParent } = moveElement(element, dragElement, dropElement, mode)

      dispatch(storeElement(elementTypes[dragParent.model], dragParent))
      if (!compareElements(dragParent, dropParent)) {
        dispatch(storeElement(elementTypes[dropParent.model], dropParent))
      }
    }
  }
}
