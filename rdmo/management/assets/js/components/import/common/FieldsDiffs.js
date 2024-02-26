import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'
import ReactDiffViewer from 'react-diff-viewer-continued'
import { isUndefined } from 'lodash'

const FieldsDiffs = ({ element, field }) => {
  const newVal = element.updated_and_changed[field].updated ?? ''
  const oldVal = element.updated_and_changed[field].current ?? ''
  return (!isUndefined(element) &&
          !isEmpty(element.updated_and_changed) &&
          !isUndefined(newVal) &&
     <div className="col-sm-12">
      <ReactDiffViewer
          oldValue={oldVal.toString()}
          newValue={newVal.toString()}
          splitView={true}
          hideLineNumbers={true}
          leftTitle={gettext('Current')}
          rightTitle={gettext('Uploaded')}
          >
          </ReactDiffViewer>
      </div>
  )
}

FieldsDiffs.propTypes = {
  element: PropTypes.object.isRequired,
  field: PropTypes.string.isRequired,
}

export default FieldsDiffs
