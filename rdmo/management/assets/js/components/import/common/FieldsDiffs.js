import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'
import ReactDiffViewer from 'react-diff-viewer-continued'
import { isUndefined } from 'lodash'


const FieldsDiffs = ({ instance, field }) => {

  return !isUndefined(instance) &&
          !isUndefined(instance[field]) &&
          !isEmpty(instance.original) &&
          !isEmpty(instance.original[field]) &&
          isEmpty(instance.errors) &&
          typeof(instance[field]) === 'string' &&
          typeof(instance.original[field]) === 'string' &&
   <div className="col-sm-12">
    <ReactDiffViewer
        oldValue={instance.original[field]}
        newValue={instance[field]}
        splitView={true}
        hideLineNumbers={true}
        leftTitle={gettext('Current')}
        rightTitle={gettext('Imported')}
        >
        </ReactDiffViewer>
    </div>
}

FieldsDiffs.propTypes = {
  instance: PropTypes.object.isRequired,
  field: PropTypes.string.isRequired,
}

export default FieldsDiffs
