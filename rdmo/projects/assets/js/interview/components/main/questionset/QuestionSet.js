import React from 'react'
import PropTypes from 'prop-types'

import { getChildPrefix } from '../../../utils/set'

import Template from 'rdmo/core/assets/js/components/Template'

import Question from '../question/Question'

import QuestionSetHelp from './QuestionSetHelp'
import QuestionSetAddSet from './QuestionSetAddSet'
import QuestionSetRemoveSet from './QuestionSetRemoveSet'

const QuestionSet = ({ templates, questionset, sets, values, disabled, focus,
                       parentSet, createSet, updateSet, deleteSet,
                       createValue, updateValue, deleteValue }) => {

  const setPrefix = getChildPrefix(parentSet)

  const currentSets = sets.filter((set) => (
    set.set_prefix == setPrefix
  ))

  return (
    <div className="interview-questionset col-md-12">
      <strong>{questionset.title}</strong>
      <QuestionSetHelp questionset={questionset} />
      {
        questionset.is_collection && (
          <Template template={templates.project_interview_add_set_help} />
        )
      }
      <div className="">
        {
          currentSets.map((set, setIndex) => (
            <div key={setIndex} className="interview-block">
              <div className="interview-block-options">
                {
                  questionset.is_collection && (
                    <QuestionSetRemoveSet questionset={questionset} set={set} deleteSet={deleteSet} />
                  )
                }
              </div>
              <div className="row">
                {
                  currentSets && (
                    questionset.elements.map((element, elementIndex) => {
                      if (element.model == 'questions.questionset') {
                        return (
                          <QuestionSet
                            key={elementIndex}
                            templates={templates}
                            questionset={element}
                            sets={sets}
                            values={values.filter((value) => element.attributes.includes(value.attribute))}
                            disabled={disabled}
                            focus={focus && (setIndex === 0 && elementIndex === 0)}
                            parentSet={set}
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
                              value.set_prefix == set.set_prefix &&
                              value.set_index == set.set_index
                            ))}
                            disabled={disabled}
                            focus={focus && (setIndex === 0 && elementIndex === 0)}
                            currentSet={set}
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
            </div>
          ))
        }
      </div>
      {
        questionset.is_collection && (
          <QuestionSetAddSet questionset={questionset} sets={currentSets} setPrefix={setPrefix} createSet={createSet} />
        )
      }
    </div>
  )
}

QuestionSet.propTypes = {
  templates: PropTypes.object.isRequired,
  questionset: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  values: PropTypes.array.isRequired,
  disabled: PropTypes.bool.isRequired,
  focus: PropTypes.bool.isRequired,
  parentSet: PropTypes.object.isRequired,
  createSet: PropTypes.func.isRequired,
  updateSet: PropTypes.func.isRequired,
  deleteSet: PropTypes.func.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired
}

export default QuestionSet
