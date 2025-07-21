// ImportAggregatedWarningsPanel.js
import React from 'react'
import PropTypes from 'prop-types'
import { ShowLink } from '../common/Links'
import { generateWarningListItems } from './common/WarningsListGroup'
import {isTruthy} from 'rdmo/core/assets/js/utils/config'
import get from 'lodash/get'

// Function to aggregate warnings from elements
const aggregateWarnings = (elements) => {
  return elements.reduce((acc, element) => {
    Object.entries(element.warnings).forEach(([uri, messages]) => {
      acc.push({ elementWarnings: { [uri]: messages }, elementModel: element.model, elementURI: element.uri })
    })
    return acc
  }, [])
}

const ImportAggregatedWarningsPanel = ({ config, elements, configActions }) => {
  const updateShowWarnings = () => {
    const currentVal = isTruthy(get(config, 'filter.import.warnings.show', false))
    configActions.updateConfig('filter.import.warnings.show', !currentVal)
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
  config: PropTypes.object.isRequired,
  elements: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired
}

export default ImportAggregatedWarningsPanel
