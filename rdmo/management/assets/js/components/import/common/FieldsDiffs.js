import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'
import ReactDiffViewer from 'react-diff-viewer-continued'
import { isUndefined } from 'lodash'


const FieldsDiffs = ({ element, field }) => {

  return !isUndefined(element) &&
          !isUndefined(element[field]) &&
          !isEmpty(element.original) &&
          !isEmpty(element.original[field]) &&
          isEmpty(element.errors) &&
          typeof(element[field]) === 'string' &&
          typeof(element.original[field]) === 'string' &&
   <div className="col-sm-12">
    <ReactDiffViewer
        oldValue={element.original[field]}
        newValue={element[field]}
        splitView={true}
        hideLineNumbers={true}
        leftTitle={gettext('Current')}
        rightTitle={gettext('Uploaded')}
        >
        </ReactDiffViewer>
    </div>
}

FieldsDiffs.propTypes = {
  element: PropTypes.object.isRequired,
  field: PropTypes.string.isRequired,
}

export default FieldsDiffs
