import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'
import { isNil } from 'lodash'

import Question from '../question/Question'
import QuestionSet from '../questionset/QuestionSet'

import PageButtons from './PageButtons'
import PageHead from './PageHead'
import PageHelp from './PageHelp'

const Page = ({ config, templates, page, sets, values, fetchPage,
                createValue, updateValue, deleteValue,
                activateSet, createSet, updateSet, deleteSet }) => {

  const currentSet = sets.find((set) => (
    set.set_prefix == '' && set.set_index == (page.is_collection ? get(config, 'page.currentSetIndex', 0) : 0)
  ))
  const pageSets = sets.filter((set) => (
    set.set_prefix == currentSet.set_prefix
  ))
  const pageValues = values.filter((value) => (
    value.set_prefix == currentSet.set_prefix && value.set_index == currentSet.set_index
  ))

  return (
    <div className="interview-page">
      <h2>{page.title}</h2>
      <PageHelp page={page} />
      {
        page.is_collection && (
          <PageHead
            page={page}
            help={templates.project_interview_page_tabs_help}
            sets={pageSets}
            values={
              isNil(page._attribute) ? [] : values.filter((value) => (value.attribute == page._attribute.id))
            }
            currentSet={currentSet}
            activateSet={activateSet}
            createSet={createSet}
            updateSet={updateSet}
            deleteSet={deleteSet}
          />
        )
      }
      {
        currentSet && (
          page.elements.map((element, elementIndex) => {
            if (element.model == 'questions.questionset') {
              return (
                <QuestionSet
                  key={elementIndex}
                  questionset={element}
                  values={values}
                />
              )
            } else {
              return (
                <Question
                  key={elementIndex}
                  templates={templates}
                  question={element}
                  values={
                    pageValues.filter((value) => (value.attribute == element._attribute.id))
                  }
                  currentSet={currentSet}
                  createValue={createValue}
                  updateValue={updateValue}
                  deleteValue={deleteValue}
                />
              )
            }
          })
        )
      }

      <PageButtons page={page} fetchPage={fetchPage} />
    </div>
  )
}

Page.propTypes = {
  config: PropTypes.object.isRequired,
  templates: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  values: PropTypes.array.isRequired,
  fetchPage: PropTypes.func.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired,
  activateSet: PropTypes.func.isRequired,
  createSet: PropTypes.func.isRequired,
  updateSet: PropTypes.func.isRequired,
  deleteSet: PropTypes.func.isRequired
}

export default Page
