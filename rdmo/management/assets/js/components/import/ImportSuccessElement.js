import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

import { codeClass, verboseNames } from '../../constants/elements'
import { isEmpty } from 'lodash'

const ImportSuccessElement = ({ element }) => {
  return (
    <li className="list-group-item">
      <p>
        <strong>{verboseNames[element.model]}{' '}</strong>
        <code className={codeClass[element.model]}>{element.uri}</code>
        {element.created && <span className="text-success">{' '}{gettext('created')}  </span> && <span className="muted element-link fa fa-plus"></span>}
        {element.updated && <span className="text-info">{' '}{gettext('updated')} </span> && <span className="muted element-link fa fa-pencil"></span>}
        {
          !isEmpty(element.errors) && !(element.created || element.updated) &&
          <span className="text-danger">{' '}{gettext('could not be imported')}</span>
        }
        {
          !isEmpty(element.errors) && (element.created || element.updated) &&
          <>{', '}<span className="text-danger">{gettext('but could not be added to parent element')}</span></>
        }
        {'.'}
      </p>
      {element.warnings.map(message => <p key={uniqueId()} className="text-warning">{message}</p>)}
      {element.errors.map(message => <p key={uniqueId()} className="text-danger">{message}</p>)}
    </li>
  )
}

ImportSuccessElement.propTypes = {
  element: PropTypes.object.isRequired,
}

export default ImportSuccessElement
