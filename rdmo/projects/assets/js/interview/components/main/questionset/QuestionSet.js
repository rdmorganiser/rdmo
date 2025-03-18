import React from 'react'
import PropTypes from 'prop-types'

import { checkQuestionSet } from '../../../utils/page'
import { getChildPrefix } from '../../../utils/set'

import Question from '../question/Question'

import QuestionSetAddSet from './QuestionSetAddSet'
import QuestionSetAddSetHelp from './QuestionSetAddSetHelp'
import QuestionSetCopySet from './QuestionSetCopySet'
import QuestionSetHelp from './QuestionSetHelp'
import QuestionSetHelpTemplate from './QuestionSetHelpTemplate'
import QuestionSetManagement from './QuestionSetManagement'
import QuestionSetRemoveSet from './QuestionSetRemoveSet'

const QuestionSet = ({ config, settings, templates, page, questionset, sets, values, disabled, isManager,
                       parentSet, createSet, updateSet, deleteSet, copySet,
                       createValue, updateValue, deleteValue, copyValue, fetchContact }) => {

  const setPrefix = getChildPrefix(parentSet)

  const currentSets = sets.filter((set) => (
    set.set_prefix == setPrefix
  ))

  return checkQuestionSet(questionset, parentSet) && (
    <div className="interview-questionset col-md-12">
      <div className="interview-questionset-label">
        <strong>{questionset.title}</strong>
      </div>
      <QuestionSetHelp questionset={questionset} />
      <QuestionSetHelpTemplate templates={templates} />
      <QuestionSetAddSetHelp templates={templates} questionset={questionset} disabled={disabled} />
      <QuestionSetManagement config={config} questionset={questionset} isManager={isManager} />
      <div>
        {
          currentSets.map((set, setIndex) => (
            <div key={setIndex} className="interview-block">
              <div className="interview-block-options">
                <QuestionSetCopySet questionset={questionset} sets={sets} currentSet={set} disabled={disabled} copySet={copySet} />
                <QuestionSetRemoveSet questionset={questionset} currentSet={set} disabled={disabled} deleteSet={deleteSet} />
              </div>
              <div className="row">
                {
                  currentSets && (
                    questionset.elements.map((element, elementIndex) => {
                      if (element.model == 'questions.questionset') {
                        return (
                          <QuestionSet
                            key={elementIndex}
                            config={config}
                            settings={settings}
                            templates={templates}
                            page={page}
                            questionset={element}
                            sets={sets}
                            values={values.filter((value) => element.attributes.includes(value.attribute))}
                            disabled={disabled}
                            isManager={isManager}
                            parentSet={set}
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
                            config={config}
                            settings={settings}
                            templates={templates}
                            page={page}
                            question={element}
                            sets={sets.filter((set) => (
                              set.set_prefix == setPrefix
                            ))}
                            values={values.filter((value) => (
                              value.attribute == element.attribute &&
                              value.set_prefix == set.set_prefix &&
                              value.set_index == set.set_index
                            ))}
                            siblings={values.filter((value) => (
                              value.attribute == element.attribute &&
                              value.set_prefix == set.set_prefix &&
                              value.set_index != set.set_index
                            ))}
                            disabled={disabled}
                            isManager={isManager}
                            currentSet={set}
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
            </div>
          ))
        }
      </div>

      <QuestionSetAddSet
        questionset={questionset}
        sets={currentSets}
        setPrefix={setPrefix}
        disabled={disabled}
        createSet={createSet}
      />
    </div>
  )
}

QuestionSet.propTypes = {
  config: PropTypes.object.isRequired,
  settings: PropTypes.object.isRequired,
  templates: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  questionset: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  values: PropTypes.array.isRequired,
  disabled: PropTypes.bool.isRequired,
  isManager: PropTypes.bool.isRequired,
  parentSet: PropTypes.object.isRequired,
  createSet: PropTypes.func.isRequired,
  updateSet: PropTypes.func.isRequired,
  deleteSet: PropTypes.func.isRequired,
  copySet: PropTypes.func.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired,
  copyValue: PropTypes.func.isRequired,
  fetchContact: PropTypes.func.isRequired
}

export default QuestionSet
