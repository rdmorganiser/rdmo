import React from 'react'
import PropTypes from 'prop-types'

import {ShowLink} from '../common/Links'

import Warnings from './common/Warnings'

import get from 'lodash/get'

const ImportWarningsPanel = ({ config, elements, configActions }) => {

  const updateShowWarnings = () => {
    const currentVal = get(config, 'filter.import.warnings.show', false)
    configActions.updateConfig('filter.import.warnings.show', !currentVal)
  }
  const showWarnings = get(config, 'filter.import.warnings.show', false)
  const listWarnings = elements.map((element, index) => {
              return (<Warnings key={index} element={element} showWarningTitle={true} showTitle={false} />)
              })
  return (
    <div className="panel panel-warning">
      <div className="panel-heading"><strong onClick={updateShowWarnings}>{gettext('Warnings')}{' '}({elements.length}){': '}</strong>
        <div className="pull-right">
          <ShowLink show={showWarnings} onClick={updateShowWarnings}/>
        </div>
      </div>
      <div className="panel-body">
        { showWarnings &&
          listWarnings
        }
      </div>
    </div>
   )
}

ImportWarningsPanel.propTypes = {
  config: PropTypes.object.isRequired,
  elements: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired
}

export default ImportWarningsPanel
