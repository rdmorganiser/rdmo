import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import { get } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { generateWarningListItems } from './common/WarningsListGroup'

import { ShowLink } from '../common/Links'

// Function to aggregate warnings from elements
const aggregateWarnings = (elements) => {
  return elements.reduce((acc, element) => {
    Object.entries(element.warnings).forEach(([uri, messages]) => {
      acc.push({ elementWarnings: { [uri]: messages }, elementModel: element.model, elementURI: element.uri })
    })
    return acc
  }, [])
}

const ImportAggregatedWarningsPanel = ({ elements }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const updateShowWarnings = () => {
    const currentVal = isTruthy(get(config, 'filter.import.warnings.show', false))
    dispatch(updateConfig('filter.import.warnings.show', !currentVal))
  }

  const showWarnings = isTruthy(get(config, 'filter.import.warnings.show', false))

  // Aggregate all warnings into a single list
  const aggregatedWarnings = aggregateWarnings(elements)

  const warningsHeadingText = <strong onClick={updateShowWarnings}>{gettext('Warnings')} ({elements.length}):</strong>

  return ( aggregatedWarnings.length > 0 &&
    <div className="panel panel-warning panel-import-warnings mt-10">
      <div className="panel-heading" onClick={updateShowWarnings}>
        {warningsHeadingText}
        <div className="pull-right">
          <ShowLink show={showWarnings} onClick={() => {}}/>
        </div>
      </div>
      {showWarnings && (
        <ul className="list-group mb-5 pb-5 pt-5 pl-5 pr-5">
          {aggregatedWarnings.map(({ elementWarnings, elementModel, elementURI }) =>
            generateWarningListItems(elementWarnings, elementModel, elementURI)
          )}
        </ul>
      )}
    </div>
  )
}

ImportAggregatedWarningsPanel.propTypes = {
  elements: PropTypes.array.isRequired
}

export default ImportAggregatedWarningsPanel
