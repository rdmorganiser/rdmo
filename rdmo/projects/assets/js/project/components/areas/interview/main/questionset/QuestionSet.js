import React from 'react'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

import Html from 'rdmo/core/assets/js/components/Html'

import { checkQuestionSet } from '../../../../../utils/page'
import { getChildPrefix } from '../../../../../utils/set'

import Question from '../question/Question'

import QuestionSetAddSet from './QuestionSetAddSet'
import QuestionSetAddSetHelp from './QuestionSetAddSetHelp'
import QuestionSetCopySet from './QuestionSetCopySet'
import QuestionSetHelp from './QuestionSetHelp'
import QuestionSetHelpTemplate from './QuestionSetHelpTemplate'
import QuestionSetManagement from './QuestionSetManagement'
import QuestionSetRemoveSet from './QuestionSetRemoveSet'

const QuestionSet = ({ questionset, sets, values, parentSet }) => {

  const setPrefix = getChildPrefix(parentSet)

  const currentSets = sets.filter((set) => (
    (set.set_prefix == setPrefix) &&
    (set.element == questionset)
  ))

  return checkQuestionSet(questionset, parentSet) && (
    <div className="project-interview-questionset col-md-12">
      <h3>
        <Html html={questionset.title} />
      </h3>
      <QuestionSetHelp questionset={questionset} />
      <QuestionSetHelpTemplate />
      <QuestionSetAddSetHelp questionset={questionset} />
      <QuestionSetManagement questionset={questionset} />
      {
        !isEmpty(questionset.elements) && !isEmpty(currentSets) && (
          <div className="d-flex flex-column justify-content-between gap-2 mb-2">
            {
              currentSets.map((set, setIndex) => (
                <div key={setIndex} className="project-interview-block">
                  <div className="d-flex gap-1 float-end">
                    <QuestionSetCopySet questionset={questionset} sets={sets} currentSet={set} />
                    <QuestionSetRemoveSet questionset={questionset} currentSet={set} />
                  </div>
                  <div className="row">
                    {
                      currentSets && (
                        questionset.elements.map((element, elementIndex) => {
                          if (element.model == 'questions.questionset') {
                            return (
                              <QuestionSet
                                key={elementIndex}
                                questionset={element}
                                sets={sets}
                                values={values.filter((value) => element.attributes.includes(value.attribute))}
                                parentSet={set}
                              />
                            )
                          } else {
                            return (
                              <Question
                                key={elementIndex}
                                question={element}
                                sets={
                                  sets.filter((set) => (
                                    set.set_prefix == setPrefix
                                  ))
                                }
                                values={
                                  values.filter((value) => (
                                    value.attribute == element.attribute &&
                                    value.set_prefix == set.set_prefix &&
                                    value.set_index == set.set_index
                                  ))
                                }
                                siblings={
                                  values.filter((value) => (
                                    value.attribute == element.attribute &&
                                    value.set_prefix == set.set_prefix &&
                                    value.set_index != set.set_index
                                  ))
                                }
                                currentSet={set}
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
        )
      }
      <QuestionSetAddSet questionset={questionset} sets={currentSets} setPrefix={setPrefix} />
    </div>
  )
}

QuestionSet.propTypes = {
  questionset: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  values: PropTypes.array.isRequired,
  parentSet: PropTypes.object.isRequired,
}

export default QuestionSet
