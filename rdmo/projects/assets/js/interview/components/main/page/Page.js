import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'
import { isNil } from 'lodash'

import Question from '../question/Question'
import QuestionSet from '../questionset/QuestionSet'

import PageButtons from './PageButtons'
import PageHead from './PageHead'
import PageHelp from './PageHelp'

const Page = ({ config, templates, overview, page, sets, values, fetchPage,
                createValue, updateValue, deleteValue,
                activateSet, createSet, updateSet, deleteSet }) => {

  const currentSetPrefix = ''
  const currentSetIndex = page.is_collection ? get(config, 'page.currentSetIndex', 0) : 0
  const currentSet = sets.find((set) => (set.set_prefix == currentSetPrefix && set.set_index == currentSetIndex)) ||
                     sets.find((set) => (set.set_prefix == currentSetPrefix && set.set_index == 0))  // sanity check

  return (
    <div className="interview-page">
      <h2>{page.title}</h2>
      <PageHelp page={page} />
      {
        page.is_collection && (
          <PageHead
            page={page}
            help={templates.project_interview_page_tabs_help}
            sets={sets.filter((set) => (set.set_prefix == currentSetPrefix))}
            values={isNil(page.attribute) ? [] : values.filter((value) => (value.attribute == page.attribute))}
            currentSet={currentSet}
            activateSet={activateSet}
            createSet={createSet}
            updateSet={updateSet}
            deleteSet={deleteSet}
          />
        )
      }
      <div className="row">
        {
          currentSet && (
            page.elements.map((element, elementIndex) => {
              if (element.model == 'questions.questionset') {
                return (
                  <QuestionSet
                    key={elementIndex}
                    templates={templates}
                    questionset={element}
                    sets={sets}
                    values={values.filter((value) => element.attributes.includes(value.attribute))}
                    disabled={overview.read_only}
                    focus={elementIndex == 0}
                    parentSet={currentSet}
                    createSet={createSet}
                    updateSet={updateSet}
                    deleteSet={deleteSet}
                    createValue={createValue}
                    updateValue={updateValue}
                    deleteValue={deleteValue}
                  />
                )
              } else {
                return (
                  <Question
                    key={elementIndex}
                    templates={templates}
                    question={element}
                    values={values.filter((value) => (
                      value.attribute == element.attribute &&
                      value.set_prefix == currentSetPrefix &&
                      value.set_index == currentSetIndex
                    ))}
                    disabled={overview.read_only}
                    focus={elementIndex == 0}
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
      </div>

      <PageButtons page={page} fetchPage={fetchPage} />
    </div>
  )
}

Page.propTypes = {
  config: PropTypes.object.isRequired,
  templates: PropTypes.object.isRequired,
  overview: PropTypes.object.isRequired,
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
