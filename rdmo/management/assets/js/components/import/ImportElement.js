import React from 'react'
import PropTypes from 'prop-types'

import {isEmpty} from 'lodash'

import {
  WarningLink,
  ErrorLink,
  ShowLink,
  AvailableLink,
  LockedLink,
} from '../common/Links'
import ImportSelectCheckbox from './common/ImportSelectCheckbox'
import Errors from './common/Errors'

import Warnings from './common/Warnings'
import Fields from './common/Fields'
import Form from './common/Form'


const ImportElement = ({ config, element, importActions }) => {
  const updateShowField = () => importActions.updateElement(element, {show: !element.show})
  const toggleImport = () => importActions.updateElement(element, {import: !element.import})
  const updateElement = (key, value) => importActions.updateElement(element, {[key]: value})
  const toggleAvailable = () => importActions.updateElement(element, {available: !element.available})

  return (
    <li className="list-group-item">

      <div className="pull-right">
        {
          (isEmpty(element.errors) && ('available' in element)) &&
           <AvailableLink available={element.available}
                          locked={element.locked} onClick={toggleAvailable}
                          title={element.available ? gettext('Make unavailable')
                                         : gettext('Make available')}/>
        }
        {
          !isEmpty(element.warnings) &&
          <WarningLink onClick={updateShowField} />
        }
        {
          !isEmpty(element.errors) &&
          <ErrorLink onClick={updateShowField} />
        }
        {
          (element.updated && element.locked) &&
          <LockedLink title={gettext('Locked')}
                      locked={element.locked} onClick={updateShowField} disabled={true} />

        }
        <ShowLink show={element.show} onClick={updateShowField} />
      </div>

      <ImportSelectCheckbox element={element} toggleImport={toggleImport} updateShowField={updateShowField} />

      {
        element.show && <>
          <Form config={config} element={element} updateElement={updateElement} />
          <Fields element={element} />
          <Errors elementErrors={element.errors} />
          <Warnings elementWarnings={element.warnings} elementModel={element.model} showTitle={true} shouldShowURI={false} />
        </>
      }
    </li>
  )
}

ImportElement.propTypes = {
  config: PropTypes.object.isRequired,
  element: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportElement
