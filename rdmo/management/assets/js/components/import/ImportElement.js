import React from 'react'
import { useDispatch } from 'react-redux'
import PropTypes from 'prop-types'

import { isEmpty } from 'lodash'

import { updateElement } from '../../actions/importActions'

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


const ImportElement = ({ element }) => {
  const dispatch = useDispatch()

  const updateShowField = () => dispatch(updateElement(element, {show: !element.show}))
  const toggleImport = () => dispatch(updateElement(element, {import: !element.import}))
  const toggleAvailable = () => dispatch(updateElement(element, {available: !element.available}))

  return (
    <li className="list-group-item">
      <div className="d-flex align-items-center gap-2">
        <ImportSelectCheckbox element={element} toggleImport={toggleImport} updateShowField={updateShowField} />

        {
          (isEmpty(element.errors) && ('available' in element)) &&
           <AvailableLink available={element.available}
                          locked={element.locked} onClick={toggleAvailable}
                          title={element.available ? gettext('Make unavailable') : gettext('Make available')} />
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

      {
        element.show && <div className="mt-2">
          <Errors elementErrors={element.errors} />
          <Warnings elementWarnings={element.warnings}
                    elementModel={element.model} elementURI={element.uri}
                    showTitle={true} shouldShowURI={false} />
          <Form element={element} />
          <Fields element={element} />
        </div>
      }
    </li>
  )
}

ImportElement.propTypes = {
  element: PropTypes.object.isRequired
}

export default ImportElement
