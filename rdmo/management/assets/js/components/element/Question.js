import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'

import { filterElement } from '../../utils/filter'

import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, LockedLink, ExportLink, CodeLink } from '../common/Links'
import { Drag, Drop } from '../common/DragAndDrop'

const Question = ({ config, question, elementActions, display='list', filter=null, indent=0 }) => {

  const verboseName = gettext('question')
  const showElement = filterElement(filter, question)

  const fetchEdit = () => elementActions.fetchElement('questions', question.id)
  const fetchCopy = () => elementActions.fetchElement('questions', question.id, 'copy')
  const toggleLocked = () => elementActions.storeElement('questions', {...question, locked: !question.locked })

  const fetchAttribute = () => elementActions.fetchElement('attributes', question.attribute)

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <EditLink element={question} verboseName={verboseName} onClick={fetchEdit} />
        <CopyLink element={question} verboseName={verboseName} onClick={fetchCopy} />
        <LockedLink element={question} verboseName={verboseName} onClick={toggleLocked} />
        <ExportLink element={question} elementType="questions" verboseName={verboseName}
                    exportFormats={config.settings.export_formats} />
        {display == 'nested' && <Drag element={question} />}
      </div>
      <div>
        <p>
          <strong className={question.is_optional ? 'text-muted' : ''}>{gettext('Question')}{': '}</strong>
          {question.text}
        </p>
        {
          config.display.uri.questions && <p>
            <CodeLink className="code-questions" uri={question.uri} onClick={() => fetchEdit()} />
          </p>
        }
        {
          config.display.uri.attributes && question.attribute_uri && <p>
            <CodeLink className="code-domain" uri={question.attribute_uri} onClick={() => fetchAttribute()} />
          </p>
        }
        <ElementErrors element={question} />
      </div>
    </div>
  )

  switch (display) {
    case 'list':
      return showElement && (
        <li className="list-group-item">
          { elementNode }
        </li>
      )
    case 'nested':
      return (
        <>
          {
            showElement && config.display.elements.questions && (
              <div className="panel panel-default panel-nested" style={{ marginLeft: 30 * indent }}>
                <div className="panel-body">
                  { elementNode }
                </div>
              </div>
            )
          }
          <Drop element={question} elementActions={elementActions} indent={indent} mode="after" />
        </>
      )
  }
}

Question.propTypes = {
  config: PropTypes.object.isRequired,
  question: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  display: PropTypes.string,
  filter: PropTypes.object,
  indent: PropTypes.number
}

export default Question
