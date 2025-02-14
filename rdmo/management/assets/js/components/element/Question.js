import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { filterElement } from '../../utils/filter'
import { buildApiPath, buildPath } from '../../utils/location'

import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, LockedLink, ExportLink, CodeLink } from '../common/Links'
import { ReadOnlyIcon } from '../common/Icons'
import { Drag, Drop } from '../common/DragAndDrop'

const Question = ({ config, question, elementActions, display='list', indent=0,
                    filter=false, filterEditors=false, order }) => {

  const showElement = filterElement(config, filter, false, filterEditors, question)

  const editUrl = buildPath('questions', question.id)
  const copyUrl = buildPath('questions', question.id, 'copy')
  const exportUrl = buildApiPath('questions', 'questions', question.id, 'export')
  const attributeUrl = buildPath('attributes', question.attribute)

  const getConditionUrl = (index) => buildPath('conditions', question.conditions[index])
  const getOptionSetUrl = (index) => buildPath('optionsets', question.optionsets[index])

  const fetchEdit = () => elementActions.fetchElement('questions', question.id)
  const fetchCopy = () => elementActions.fetchElement('questions', question.id, 'copy')
  const toggleLocked = () => elementActions.storeElement('questions', {...question, locked: !question.locked })

  const fetchAttribute = () => elementActions.fetchElement('attributes', question.attribute)
  const fetchCondition = (index) => elementActions.fetchElement('conditions', question.conditions[index])
  const fetchOptionSet = (index) => elementActions.fetchElement('optionsets', question.optionsets[index])

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <ReadOnlyIcon title={gettext('This question is read only')} show={question.read_only} />
        <EditLink title={gettext('Edit question')} href={editUrl} onClick={fetchEdit} />
        <CopyLink title={gettext('Copy question')} href={copyUrl} onClick={fetchCopy} />
        <LockedLink title={question.locked ? gettext('Unlock question') : gettext('Lock question')}
                    locked={question.locked} onClick={toggleLocked} disabled={question.read_only} />
        <ExportLink title={gettext('Export question')} exportUrl={exportUrl}
                    exportFormats={config.settings.export_formats} full={true} />
        <Drag element={question} show={display == 'nested'} />
      </div>
      <div>
        <p>
          <strong className={question.is_optional ? 'text-muted' : ''}>{gettext('Question')}{': '}</strong>
          <span dangerouslySetInnerHTML={{ __html: question.text }}></span>
        </p>
        {
          get(config, 'display.uri.questions', true) && <p>
            <CodeLink
              className="code-questions"
              uri={question.uri}
              href={editUrl}
              onClick={() => fetchEdit()}
              order={order} />
          </p>
        }
        {
          get(config, 'display.uri.attributes', true) && question.attribute_uri && <p>
            <CodeLink
              className="code-domain"
              uri={question.attribute_uri}
              href={attributeUrl}
              onClick={() => fetchAttribute()} />
          </p>
        }
        {
          get(config, 'display.uri.conditions', true) && question.condition_uris.map((uri, index) => (
            <p key={index}>
              <CodeLink
                className="code-conditions"
                uri={uri}
                href={getConditionUrl(index)}
                onClick={() => fetchCondition(index)} />
            </p>
          ))
        }
        {
          get(config, 'display.uri.optionsets', true) && question.optionset_uris.map((uri, index) => (
            <p key={index}>
              <CodeLink
                className="code-options"
                uri={uri}
                href={getOptionSetUrl(index)}
                onClick={() => fetchOptionSet(index)} />
            </p>
          ))
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
            showElement && (
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
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  display: PropTypes.string,
  indent: PropTypes.number,
  filter: PropTypes.string,
  filterEditors: PropTypes.bool,
  order: PropTypes.number
}

export default Question
