import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { ExtendLink } from '../common/ElementLinks'

import useBool from '../../hooks/useBool'

const AttributeInfo = ({ attribute, elements }) => {

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

  return (
    <div className="element-info">
      <p>
        <span dangerouslySetInnerHTML={{
          __html: interpolate(ngettext(
            'This attribute is used for <b>%s values</b> in <b>one project</b>.',
            'This attribute is used for <b>%s values</b> in <b>%s projects</b>.',
            attribute.projects_count), [attribute.values_count, attribute.projects_count])}} />
      </p>
      {
        attributes.length > 0 && <>
          <p>
            <span dangerouslySetInnerHTML={{
              __html: interpolate(ngettext(
                'This attribute has <b>one decendant</b>.',
                'This attribute has <b>%s decendants</b>.',
                attributes.length
              ), [attributes.length])}} />
            <ExtendLink extend={extendAttributes} onClick={toggleAttributes} />
          </p>
          {
            extendAttributes && attributes.map((attribute, index) => (
              <p key={index}>
                <code className="code-domain">{attribute.uri}</code>
              </p>
            ))
          }
        </>
      }
      {
        conditions.length > 0 && <>
          <p>
            <span dangerouslySetInnerHTML={{
              __html: interpolate(ngettext(
                'This attribute is used in <b>one condition</b>.',
                'This attribute is used in <b>%s conditions</b>.',
                conditions.length), [conditions.length])}} />
            <ExtendLink extend={extendConditions} onClick={toggleConditions} />
          </p>
          {
            extendConditions && conditions.map((condition, index) => (
              <p key={index}>
                <code className="code-conditions">{condition.uri}</code>
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
                'This attribute is used in <b>one page</b>.',
                'This attribute is used in <b>%s pages</b>.',
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
                'This attribute is used in <b>one questionset</b>.',
                'This attribute is used in <b>%s questionsets</b>.',
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
                'This attribute is used in <b>one question</b>.',
                'This attribute is used in <b>%s questions</b>.',
                questions.length), [questions.length])}} />
            <ExtendLink extend={extendQuestions} onClick={toggleQuestions} />
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
                'This attribute is used in <b>one task</b>.',
                'This attribute is used in <b>%s tasks</b>.',
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

AttributeInfo.propTypes = {
  attribute: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired
}

export default AttributeInfo
