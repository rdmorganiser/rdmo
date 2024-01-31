import React from 'react'
import PropTypes from 'prop-types'

import {ShowLink} from '../common/Links'

import Warnings from './common/Warnings'

import get from 'lodash/get'

const ImportWarnings = ({ config, elements, configActions }) => {

  const updateShowWarnings = () => {
    const currentVal = get(config, 'filter.import.warnings.show', false)
    configActions.updateConfig('filter.import.elements.changed', !currentVal)
  }

  const showWarnings = get(config, 'filter.import.warnings.show', false)
  // const toggleImport = () => importActions.updateElement(element, {import: !element.import})
  // const updateElement = (key, value) => importActions.updateElement(element, {[key]: value})
  return (
    <li className="list-group-item">
      <div className="pull-right">
        <ShowLink show={showWarnings} onClick={updateShowWarnings}/>
      </div>

      <div>
        <p>
          <strong>{gettext('Warnings')}{' '}({elements.length}){': '}</strong>
        </p>
      </div>

      <ul className="list-group">
        {showWarnings && (
          elements.map((element, index) => {
            <Warnings key={index} element={element} showWarningTitle={true}/>
          })
        )}
      </ul>
    </li>
  )
}

ImportWarnings.propTypes = {
  config: PropTypes.object.isRequired,
  elements: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired
}

export default ImportWarnings
