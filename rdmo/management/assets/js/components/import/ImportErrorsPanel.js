import React from 'react'
import PropTypes from 'prop-types'
import {ShowLink} from '../common/Links'
import Errors from './common/Errors'
import get from 'lodash/get'

const ImportErrorsPanel = ({ config, elements, configActions }) => {
  const updateShowErrors = () => {
    const currentVal = get(config, 'filter.import.errors.show', false)
    configActions.updateConfig('filter.import.errors.show', !currentVal)
  }

  const showErrors = get(config, 'filter.import.errors.show', false)
  const listErrors = elements.map((element, index) => {
            return (<Errors key={index} element={element} />)
            })

  return (
    <div className="panel panel-danger">
      <div className="panel-heading"><strong>{gettext('Errors')}{' '}({elements.length}){' : '}</strong>
        <div className="pull-right">
          <ShowLink show={showErrors} onClick={updateShowErrors}/>
        </div>
      </div>
      <div className="panel-body">
        { showErrors &&
          <ul className="list-group">{listErrors}</ul>
        }
      </div>
    </div>
   )
}

ImportErrorsPanel.propTypes = {
  config: PropTypes.object.isRequired,
  elements: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired
}

export default ImportErrorsPanel
