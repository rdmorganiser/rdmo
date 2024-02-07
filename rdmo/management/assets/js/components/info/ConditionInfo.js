import React from 'react'
import PropTypes from 'prop-types'

import { ExtendLink, CodeLink } from '../common/Links'

import useBool from '../../hooks/useBool'

const ConditionInfo = ({ condition, elements, elementActions }) => {

  const [extendOptionSets, toggleOptionSets] = useBool(false)
  const [extendPages, togglePages] = useBool(false)
  const [extendQuestionSets, toggleQuestionSets] = useBool(false)
  const [extendQuestions, toggleQuestion] = useBool(false)
  const [extendTasks, toggleTasks] = useBool(false)

  const optionsets = elements.optionsets.filter(e => condition.optionsets.includes(e.id))
  const pages = elements.pages.filter(e => condition.pages.includes(e.id))
  const questionsets = elements.questionsets.filter(e => condition.questionsets.includes(e.id))
  const questions = elements.questions.filter(e => condition.questions.includes(e.id))
  const tasks = elements.tasks.filter(e => condition.tasks.includes(e.id))

  const fetchOptionSet = (optionset) => elementActions.fetchElement('optionsets', optionset.id)
  const fetchPage = (page) => elementActions.fetchElement('pages', page.id)
  const fetchQuestionSet = (questionset) => elementActions.fetchElement('questionsets', questionset.id)
  const fetchQuestion = (question) => elementActions.fetchElement('questions', question.id)
  const fetchTask = (task) => elementActions.fetchElement('tasks', task.id)

  return (
    <div className="element-info">
      <p>
        <span dangerouslySetInnerHTML={{
          __html: interpolate(ngettext(
            'This condition is used for <b>one optionset</b>.',
            'This condition is used for <b>%s optionsets</b>.',
            optionsets.length), [optionsets.length])}} />
        {optionsets.length > 0 && <ExtendLink extend={extendOptionSets} onClick={toggleOptionSets} />}
      </p>
      {
        extendOptionSets && optionsets.map((optionset, index) => (
          <p key={index}>
            <CodeLink className="code-options" uri={optionset.uri} onClick={() => fetchOptionSet(optionset)} />
          </p>
        ))
      }
      <p>
        <span dangerouslySetInnerHTML={{
          __html: interpolate(ngettext(
            'This condition is used for <b>one page</b>.',
            'This condition is used for <b>%s pages</b>.',
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
            'This condition is used for <b>one questionset</b>.',
            'This condition is used for <b>%s questionsets</b>.',
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
            'This condition is used for <b>one question</b>.',
            'This condition is used for <b>%s questions</b>.',
            questions.length), [questions.length])}} />
        {questions.length > 0 && <ExtendLink extend={extendQuestions} onClick={toggleQuestion} />}
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
            'This condition is used for <b>one task</b>.',
            'This condition is used for <b>%s tasks</b>.',
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

ConditionInfo.propTypes = {
  condition: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default ConditionInfo
