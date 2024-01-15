import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

import { codeClass, verboseNames } from '../../constants/elements'
import { isEmpty } from 'lodash'

const ImportSuccessElement = ({ instance }) => {
  return (
    <li className="list-group-item">
      <p>
        <strong>{verboseNames[instance.model]}{' '}</strong>
        <code className={codeClass[instance.model]}>{instance.uri}</code>
        {instance.created && <span className="text-success">{' '}{gettext('created')}  </span> && <span className="muted element-link fa fa-plus"></span>}
        {instance.updated && <span className="text-info">{' '}{gettext('updated')} </span> && <span className="muted element-link fa fa-pencil"></span>}
        {
          !isEmpty(instance.errors) && !(instance.created || instance.updated) &&
          <span className="text-danger">{' '}{gettext('could not be imported')}</span>
        }
        {
          !isEmpty(instance.errors) && (instance.created || instance.updated) &&
          <>{', '}<span className="text-danger">{gettext('but could not be added to parent element')}</span></>
        }
        {'.'}
      </p>
      {instance.warnings.map(message => <p key={uniqueId()} className="text-warning">{message}</p>)}
      {instance.errors.map(message => <p key={uniqueId()} className="text-danger">{message}</p>)}
    </li>
  )
}

ImportSuccessElement.propTypes = {
  instance: PropTypes.object.isRequired,
}

export default ImportSuccessElement
