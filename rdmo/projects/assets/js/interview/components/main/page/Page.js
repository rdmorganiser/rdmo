import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'
import { isNil } from 'lodash'

import Html from 'rdmo/core/assets/js/components/Html'

import Question from '../question/Question'
import QuestionSet from '../questionset/QuestionSet'

import PageButtons from './PageButtons'
import PageHead from './PageHead'

const Page = ({ config, settings, templates, overview, page, sets, values, fetchPage, fetchContact,
                createValue, updateValue, deleteValue, copyValue,
                activateSet, createSet, updateSet, deleteSet, copySet }) => {

  const currentSetPrefix = ''
  let currentSetIndex = page.is_collection ? get(config, 'page.currentSetIndex', 0) : 0
  let currentSet = sets.find((set) => (set.set_prefix == currentSetPrefix && set.set_index == currentSetIndex))

  // sanity check
  if (isNil(currentSet)) {
    currentSetIndex = 0
    currentSet = sets.find((set) => (set.set_prefix == currentSetPrefix && set.set_index == 0))
  }

  const isManager = (overview.is_superuser || overview.is_editor || overview.is_reviewer)

  return (
    <div className="interview-page">
      <h2>{page.title}</h2>
      <Html html={page.help} />
      <PageHead
        templates={templates}
        page={page}
        sets={sets.filter((set) => (set.set_prefix == currentSetPrefix))}
        values={isNil(page.attribute) ? [] : values.filter((value) => (value.attribute == page.attribute))}
        currentSet={currentSet}
        activateSet={activateSet}
        createSet={createSet}
        updateSet={updateSet}
        deleteSet={deleteSet}
        copySet={copySet}
      />
      <div className="row">
        {
          currentSet && (
            page.elements.map((element, elementIndex) => {
              if (element.model == 'questions.questionset') {
                return (
                  <QuestionSet
                    key={elementIndex}
                    settings={settings}
                    templates={templates}
                    questionset={element}
                    sets={sets}
                    values={values.filter((value) => element.attributes.includes(value.attribute))}
                    disabled={overview.read_only}
                    isManager={isManager}
                    parentSet={currentSet}
                    createSet={createSet}
                    updateSet={updateSet}
                    deleteSet={deleteSet}
                    copySet={copySet}
                    createValue={createValue}
                    updateValue={updateValue}
                    deleteValue={deleteValue}
                    copyValue={copyValue}
                    fetchContact={fetchContact}
                  />
                )
              } else {
                return (
                  <Question
                    key={elementIndex}
                    settings={settings}
                    templates={templates}
                    question={element}
                    values={values.filter((value) => (
                      value.attribute == element.attribute &&
                      value.set_prefix == currentSetPrefix &&
                      value.set_index == currentSetIndex
                    ))}
                    siblings={values.filter((value) => (
                      value.attribute == element.attribute &&
                      value.set_prefix == currentSetPrefix &&
                      value.set_index != currentSetIndex
                    ))}
                    disabled={overview.read_only}
                    isManager={isManager}
                    currentSet={currentSet}
                    createValue={createValue}
                    updateValue={updateValue}
                    deleteValue={deleteValue}
                    copyValue={copyValue}
                    fetchContact={fetchContact}
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
  settings: PropTypes.object.isRequired,
  templates: PropTypes.object.isRequired,
  overview: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  values: PropTypes.array.isRequired,
  fetchPage: PropTypes.func.isRequired,
  fetchContact: PropTypes.func.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired,
  copyValue: PropTypes.func.isRequired,
  activateSet: PropTypes.func.isRequired,
  createSet: PropTypes.func.isRequired,
  updateSet: PropTypes.func.isRequired,
  deleteSet: PropTypes.func.isRequired,
  copySet: PropTypes.func.isRequired
}

export default Page
