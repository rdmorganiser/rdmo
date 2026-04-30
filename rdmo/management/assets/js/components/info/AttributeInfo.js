import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'

import { fetchElement } from '../../actions/elementActions'
import useBool from '../../hooks/useBool'

import { CodeLink, ExtendLink } from '../common/Links'

const AttributeInfo = ({ attribute }) => {
  const dispatch = useDispatch()

  const elements = useSelector((state) => state.elements)

  const [extendAttributes, toggleAttributes] = useBool(false)
  const [extendConditions, toggleConditions] = useBool(false)
  const [extendPages, togglePages] = useBool(false)
  const [extendQuestionSets, toggleQuestionSets] = useBool(false)
  const [extendQuestions, toggleQuestions] = useBool(false)
  const [extendTasks, toggleTasks] = useBool(false)

  const attributes = elements.attributes.filter(e => attribute.attributes.includes(e.id))
  const conditions = elements.conditions.filter(e => attribute.conditions.includes(e.id))
  const pages = elements.pages.filter(e => attribute.pages.includes(e.id))
  const questionsets = elements.questionsets.filter(e => attribute.questionsets.includes(e.id))
  const questions = elements.questions.filter(e => attribute.questions.includes(e.id))
  const tasks = elements.tasks.filter(e => attribute.tasks.includes(e.id))

  const fetchAttribute = (attribute) => dispatch(fetchElement('attributes', attribute.id))
  const fetchCondition = (condition) => dispatch(fetchElement('conditions', condition.id))
  const fetchPage = (page) => dispatch(fetchElement('pages', page.id))
  const fetchQuestionSet = (questionset) => dispatch(fetchElement('questionsets', questionset.id))
  const fetchQuestion = (question) => dispatch(fetchElement('questions', question.id))
  const fetchTask = (task) => dispatch(fetchElement('tasks', task.id))

  return (
    <div className="mb-2">
      <p className="mb-1">
        <Html html={
          interpolate(ngettext(
            'This attribute is used for <b>%s values</b> in <b>one project</b>.',
            'This attribute is used for <b>%s values</b> in <b>%s projects</b>.',
            attribute.projects_count), [attribute.values_count, attribute.projects_count])
        } />
      </p>
      <p className="mb-1">
        <Html html={
          interpolate(ngettext(
            'This attribute has <b>one descendant</b>.',
            'This attribute has <b>%s descendants</b>.',
            attributes.length
          ), [attributes.length])
        } />
        {attributes.length > 0 && <ExtendLink extend={extendAttributes} onClick={toggleAttributes} />}
      </p>
      {
        extendAttributes && attributes.map((attribute, index) => (
          <p className="mb-1" key={index}>
            <CodeLink type="domain" uri={attribute.uri} onClick={() => fetchAttribute(attribute)} />
          </p>
        ))
      }
      <p className="mb-1">
        <Html html={
          interpolate(ngettext(
            'This attribute is used in <b>one condition</b>.',
            'This attribute is used in <b>%s conditions</b>.',
            conditions.length), [conditions.length])
        } />
        {conditions.length > 0 && <ExtendLink extend={extendConditions} onClick={toggleConditions} />}
      </p>
      {
        extendConditions && conditions.map((condition, index) => (
          <p key={index}>
            <CodeLink type="conditions" uri={condition.uri} onClick={() => fetchCondition(condition)} />
          </p>
        ))
      }
      <p className="mb-1">
        <Html html={
          interpolate(ngettext(
            'This attribute is used in <b>one page</b>.',
            'This attribute is used in <b>%s pages</b>.',
            pages.length), [pages.length])
        } />
        {pages.length > 0 && <ExtendLink extend={extendPages} onClick={togglePages} />}
      </p>
      {
        extendPages && pages.map((page, index) => (
          <p className="mb-1" key={index}>
            <CodeLink type="questions" uri={page.uri} onClick={() => fetchPage(page)} />
          </p>
        ))
      }
      <p className="mb-1">
        <Html html={
          interpolate(ngettext(
            'This attribute is used in <b>one questionset</b>.',
            'This attribute is used in <b>%s questionsets</b>.',
            questionsets.length), [questionsets.length])
        } />
        {questionsets.length > 0 && <ExtendLink extend={extendQuestionSets} onClick={toggleQuestionSets} />}
      </p>
      {
        extendQuestionSets && questionsets.map((questionset, index) => (
          <p className="mb-1" key={index}>
            <CodeLink type="questions" uri={questionset.uri} onClick={() => fetchQuestionSet(questionset)} />
          </p>
        ))
      }
      <p className="mb-1">
        <Html html={
          interpolate(ngettext(
            'This attribute is used in <b>one question</b>.',
            'This attribute is used in <b>%s questions</b>.',
            questions.length), [questions.length])
        } />
        {questions.length > 0 && <ExtendLink extend={extendQuestions} onClick={toggleQuestions} />}
      </p>
      {
        extendQuestions && questions.map((question, index) => (
          <p className="mb-1" key={index}>
            <CodeLink type="questions" uri={question.uri} onClick={() => fetchQuestion(question)} />
          </p>
        ))
      }
      <p className="mb-1">
        <Html html={
          interpolate(ngettext(
            'This attribute is used in <b>one task</b>.',
            'This attribute is used in <b>%s tasks</b>.',
            tasks.length), [tasks.length])
        } />
        {tasks.length > 0 && <ExtendLink extend={extendTasks} onClick={toggleTasks} />}
      </p>
      {
        extendTasks && tasks.map((task, index) => (
          <p className="mb-1" key={index}>
            <CodeLink type="tasks" uri={task.uri} onClick={() => fetchTask(task)} />
          </p>
        ))
      }
    </div>
  )
}

AttributeInfo.propTypes = {
  attribute: PropTypes.object.isRequired
}

export default AttributeInfo
