import React from 'react'
import { useDispatch } from 'react-redux'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

import { updateElement } from '../../actions/importActions'

import { codeClass, verboseNames } from '../../constants/elements'

import Warnings from './common/Warnings'
import Errors from './common/Errors'

const ImportSuccessElement = ({ element }) => {
  const dispatch = useDispatch()

  const updateShowField = () => dispatch(updateElement(element, { show: !element.show }))

  const changedLabelText = gettext('Changed')
  const createdLabelText = gettext('Created')

  return (
    <li className="list-group-item">
      <div className="d-flex align-items-center gap-2">
        <strong>{verboseNames[element.model]}</strong>
        <code className={codeClass[element.model]}>{element.uri}</code>

        {
          (element.changed && element.updated) && (
            <span className="badge text-bg-info" onClick={updateShowField}>
              {changedLabelText}
            </span>
          )
        }

        {
          element.created && (
            <span className="badge text-bg-success" onClick={updateShowField}>
              {createdLabelText}
            </span>
          )
        }

        {
          !isEmpty(element.errors) && (
            <span className="text-danger">
              {' '}{gettext('could not be imported')}
              {(element.created || element.updated) && `, ${gettext('but could not be added to parent element')}`}
              {'.'}
            </span>
          )
        }
      </div>

      <Errors elementErrors={element.errors} />
      <Warnings elementWarnings={element.warnings}
                elementModel={element.model} elementURI={element.uri}
                showTitle={true} shouldShowURI={false} />
    </li>
  )
}

ImportSuccessElement.propTypes = {
  element: PropTypes.object.isRequired
}

export default ImportSuccessElement
