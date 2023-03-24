import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { ExtendLink } from '../common/Links'

import useBool from '../../hooks/useBool'

const ConditionInfo = ({ condition, elements }) => {

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

  return (
    <div className="element-info">
      {
        optionsets.length > 0 && <>
          <p>
            <span dangerouslySetInnerHTML={{
              __html: interpolate(ngettext(
                'This condition is used for <b>one optionset</b>.',
                'This condition is used for <b>%s optionsets</b>.',
                optionsets.length), [optionsets.length])}} />
            <ExtendLink extend={extendOptionSets} onClick={toggleOptionSets} />
          </p>
          {
            extendOptionSets && optionsets.map((optionset, index) => (
              <p key={index}>
                <code className="code-options">{optionset.uri}</code>
              </p>
            ))
          }
        </>
      }
      {
        pages.length > 0 && <>
          <p>
            <span dangerouslySetInnerHTML={{
              __html: interpolate(ngettext(
                'This condition is used for <b>one page</b>.',
                'This condition is used for <b>%s pages</b>.',
                pages.length), [pages.length])}} />
            <ExtendLink extend={extendPages} onClick={togglePages} />
          </p>
          {
            extendPages && pages.map((page, index) => (
              <p key={index}>
                <code className="code-questions">{page.uri}</code>
              </p>
            ))
          }
        </>
      }
      {
        questionsets.length > 0 && <>
          <p>
            <span dangerouslySetInnerHTML={{
              __html: interpolate(ngettext(
                'This condition is used for <b>one questionset</b>.',
                'This condition is used for <b>%s questionsets</b>.',
                questionsets.length), [questionsets.length])}} />
            <ExtendLink extend={extendQuestionSets} onClick={toggleQuestionSets} />
          </p>
          {
            extendQuestionSets && questionsets.map((questionset, index) => (
              <p key={index}>
                <code className="code-questions">{questionset.uri}</code>
              </p>
            ))
          }
        </>
      }
      {
        questions.length > 0 && <>
          <p>
            <span dangerouslySetInnerHTML={{
              __html: interpolate(ngettext(
                'This condition is used for <b>one question</b>.',
                'This condition is used for <b>%s questions</b>.',
                questions.length), [questions.length])}} />
            <ExtendLink extend={extendQuestions} onClick={toggleQuestion} />
          </p>
          {
            extendQuestions && questions.map((question, index) => (
              <p key={index}>
                <code className="code-questions">{question.uri}</code>
              </p>
            ))
          }
        </>
      }
      {
        tasks.length > 0 && <>
          <p>
            <span dangerouslySetInnerHTML={{
              __html: interpolate(ngettext(
                'This condition is used for <b>one task</b>.',
                'This condition is used for <b>%s tasks</b>.',
                tasks.length), [tasks.length])}} />
            <ExtendLink extend={extendTasks} onClick={toggleTasks} />
          </p>
          {
            extendTasks && tasks.map((task, index) => (
              <p key={index}>
                <code className="code-tasks">{task.uri}</code>
              </p>
            ))
          }
        </>
      }
    </div>
  )
}

ConditionInfo.propTypes = {
  condition: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired
}

export default ConditionInfo
