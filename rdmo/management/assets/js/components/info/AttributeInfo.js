import React from 'react'
import PropTypes from 'prop-types'

import { ExtendLink, CodeLink } from '../common/Links'

import useBool from '../../hooks/useBool'

const AttributeInfo = ({ attribute, elements, elementActions }) => {

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

  const fetchAttribute = (attribute) => elementActions.fetchElement('attributes', attribute.id)
  const fetchCondition = (condition) => elementActions.fetchElement('conditions', condition.id)
  const fetchPage = (page) => elementActions.fetchElement('pages', page.id)
  const fetchQuestionSet = (questionset) => elementActions.fetchElement('questionsets', questionset.id)
  const fetchQuestion = (question) => elementActions.fetchElement('questions', question.id)
  const fetchTask = (task) => elementActions.fetchElement('tasks', task.id)

  return (
    <div className="element-info">
      <p>
        <span dangerouslySetInnerHTML={{
          __html: interpolate(ngettext(
            'This attribute is used for <b>%s values</b> in <b>one project</b>.',
            'This attribute is used for <b>%s values</b> in <b>%s projects</b>.',
            attribute.projects_count), [attribute.values_count, attribute.projects_count])}} />
      </p>
      <p>
        <span dangerouslySetInnerHTML={{
          __html: interpolate(ngettext(
            'This attribute has <b>one descendant</b>.',
            'This attribute has <b>%s descendants</b>.',
            attributes.length
          ), [attributes.length])}} />
        {attributes.length > 0 && <ExtendLink extend={extendAttributes} onClick={toggleAttributes} />}
      </p>
      {
        extendAttributes && attributes.map((attribute, index) => (
          <p key={index}>
            <CodeLink className="code-domain" uri={attribute.uri} onClick={() => fetchAttribute(attribute)} />
          </p>
        ))
      }
      <p>
        <span dangerouslySetInnerHTML={{
          __html: interpolate(ngettext(
            'This attribute is used in <b>one condition</b>.',
            'This attribute is used in <b>%s conditions</b>.',
            conditions.length), [conditions.length])}} />
        {conditions.length > 0 && <ExtendLink extend={extendConditions} onClick={toggleConditions} />}
      </p>
      {
        extendConditions && conditions.map((condition, index) => (
          <p key={index}>
            <CodeLink className="code-conditions" uri={condition.uri} onClick={() => fetchCondition(condition)} />
          </p>
        ))
      }
      <p>
        <span dangerouslySetInnerHTML={{
          __html: interpolate(ngettext(
            'This attribute is used in <b>one page</b>.',
            'This attribute is used in <b>%s pages</b>.',
            pages.length), [pages.length])}} />
        {pages.length > 0 && <ExtendLink extend={extendPages} onClick={togglePages} />}
      </p>
      {
        extendPages && pages.map((page, index) => (
          <p key={index}>
            <CodeLink className="code-questions" uri={page.uri} onClick={() => fetchPage(page)} />
          </p>
        ))
      }
      <p>
        <span dangerouslySetInnerHTML={{
          __html: interpolate(ngettext(
            'This attribute is used in <b>one questionset</b>.',
            'This attribute is used in <b>%s questionsets</b>.',
            questionsets.length), [questionsets.length])}} />
        {questionsets.length > 0 && <ExtendLink extend={extendQuestionSets} onClick={toggleQuestionSets} />}
      </p>
      {
        extendQuestionSets && questionsets.map((questionset, index) => (
          <p key={index}>
            <CodeLink className="code-questions" uri={questionset.uri} onClick={() => fetchQuestionSet(questionset)} />
          </p>
        ))
      }
      <p>
        <span dangerouslySetInnerHTML={{
          __html: interpolate(ngettext(
            'This attribute is used in <b>one question</b>.',
            'This attribute is used in <b>%s questions</b>.',
            questions.length), [questions.length])}} />
        {questions.length > 0 && <ExtendLink extend={extendQuestions} onClick={toggleQuestions} />}
      </p>
      {
        extendQuestions && questions.map((question, index) => (
          <p key={index}>
            <CodeLink className="code-questions" uri={question.uri} onClick={() => fetchQuestion(question)} />
          </p>
        ))
      }
      <p>
        <span dangerouslySetInnerHTML={{
          __html: interpolate(ngettext(
            'This attribute is used in <b>one task</b>.',
            'This attribute is used in <b>%s tasks</b>.',
            tasks.length), [tasks.length])}} />
        {tasks.length > 0 && <ExtendLink extend={extendTasks} onClick={toggleTasks} />}
      </p>
      {
        extendTasks && tasks.map((task, index) => (
          <p key={index}>
            <CodeLink className="code-tasks" uri={task.uri} onClick={() => fetchTask(task)} />
          </p>
        ))
      }
    </div>
  )
}

AttributeInfo.propTypes = {
  attribute: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default AttributeInfo
