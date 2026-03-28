import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import { get, isEmpty } from 'lodash'

import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import Html from 'rdmo/core/assets/js/components/Html'

import { fetchElement, storeElement } from '../../actions/elementActions'
import { filterElement } from '../../utils/filter'
import { buildApiPath, buildPath } from '../../utils/location'

import { Drag, Drop } from '../common/DragAndDrop'
import { ElementErrors } from '../common/Errors'
import { ReadOnlyIcon } from '../common/Icons'
import { CodeLink, CopyLink, EditLink, ExportLink, LockedLink } from '../common/Links'

const Question = ({ question, display = 'list', indent = 0, filter = false, filterEditors = false, order }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const showElement = filterElement(config, filter, false, filterEditors, question)

  const editUrl = buildPath('questions', question.id)
  const copyUrl = buildPath('questions', question.id, 'copy')
  const exportUrl = buildApiPath('questions', 'questions', question.id, 'export')
  const attributeUrl = buildPath('attributes', question.attribute)

  const getConditionUrl = (index) => buildPath('conditions', question.conditions[index])
  const getOptionSetUrl = (index) => buildPath('optionsets', question.optionsets[index])

  const fetchEdit = () => dispatch(fetchElement('questions', question.id))
  const fetchCopy = () => dispatch(fetchElement('questions', question.id, 'copy'))
  const toggleLocked = () => dispatch(storeElement('questions', {...question, locked: !question.locked }))

  const fetchAttribute = () => dispatch(fetchElement('attributes', question.attribute))
  const fetchCondition = (index) => dispatch(fetchElement('conditions', question.conditions[index]))
  const fetchOptionSet = (index) => dispatch(fetchElement('optionsets', question.optionsets[index]))

  const displayUriQuestions = isTruthy(get(config, 'display.uri.questions', true))
  const displayUriAttributes = isTruthy(get(config, 'display.uri.attributes', true))
  const displayUriConditions = isTruthy(get(config, 'display.uri.conditions', true))
  const displayUriOptionSets = isTruthy(get(config, 'display.uri.optionsets', true))


  const elementNode = (
    <div className="d-flex flex-column gap-2">
      <div className="d-flex align-items-center gap-2">
        <strong>{gettext('Question')}{':'}</strong>
        <div className="flex-grow-1">
          <Html html={question.text} />
        </div>
        {
          question.is_optional && (
            <div className="me-1">
              <code className="code-optional" title={gettext('This is an optional question.')}>
                {gettext('optional')}
              </code>
            </div>
          )
        }
        {
          (question.default_text || question.default_option || question.default_external_id) && (
            <div className="me-1">
              <code className="code-default" title={gettext('This question has a default answer.')}>
                {gettext('default')}
              </code>
            </div>
          )
        }
        <div className="d-flex align-items-center gap-1">
          <ReadOnlyIcon title={gettext('This question is read only')} show={question.read_only} />
          <EditLink title={gettext('Edit question')} href={editUrl} onClick={fetchEdit} />
          <CopyLink title={gettext('Copy question')} href={copyUrl} onClick={fetchCopy} />
          <LockedLink title={question.locked ? gettext('Unlock question') : gettext('Lock question')}
            locked={question.locked} onClick={toggleLocked} disabled={question.read_only} />
          <ExportLink title={gettext('Export question')} exportUrl={exportUrl}
            exportFormats={config.settings.export_formats} full={true} />
          <Drag element={question} show={display == 'nested'} />
        </div>
      </div>
      {
        displayUriQuestions && (
          <CodeLink
            type="questions"
            uri={question.uri}
            href={editUrl}
            onClick={() => fetchEdit()}
            order={order} />
        )
      }
      {
        displayUriAttributes && question.attribute_uri && (
          <CodeLink
            type="domain"
            uri={question.attribute_uri}
            href={attributeUrl}
            onClick={() => fetchAttribute()} />
        )
      }
      {
        displayUriConditions && question.condition_uris.map((uri, index) => (
          <CodeLink
            key={index}
            type="conditions"
            uri={uri}
            href={getConditionUrl(index)}
            onClick={() => fetchCondition(index)} />
        ))
      }
      {
        displayUriOptionSets && question.optionset_uris.map((uri, index) => (
          <CodeLink
            key={index}
            type="options"
            uri={uri}
            href={getOptionSetUrl(index)}
            onClick={() => fetchOptionSet(index)} />
        ))
      }
      {
        !isEmpty(question.warning) && (
          <ul className="list-unstyled mb-0">
            {
              question.warning.no_attribute && (
                <li className="text-danger">
                  {gettext('Error: No attribute is set for this question!')}
                </li>
              )
            }
            {
              question.warning.double_attribute && (
                <li className="text-danger">
                  {gettext('Error: The attribute for this question is used several times (in this catalog).')}
                </li>
              )
            }
            {
              question.warning.missing_languages && (
                <li className="text-warning">
                  {gettext('Warning: Some of the language specific fields are not set properly.')}
                </li>
              )
            }
          </ul>
        )
      }
      <ElementErrors element={question} />
    </div>
  )

  switch (display) {
    case 'list':
      return showElement && (
        <li className="list-group-item">
          {elementNode}
        </li>
      )
    case 'nested':
      return (
        <div className="position-relative">
          {
            showElement && (
              <div className="card mt-2" style={{ marginLeft: `calc(${indent} * var(--rdmo-management-indent))` }}>
                <div className="card-body">
                  {elementNode}
                </div>
              </div>
            )
          }
          <Drop element={question} indent={indent} mode="after" />
        </div>
      )
  }
}

Question.propTypes = {
  question: PropTypes.object.isRequired,
  display: PropTypes.string,
  indent: PropTypes.number,
  filter: PropTypes.string,
  filterEditors: PropTypes.bool,
  order: PropTypes.number
}

export default Question
