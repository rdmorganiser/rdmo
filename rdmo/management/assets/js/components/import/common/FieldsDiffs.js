import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'
import ReactDiffViewer from 'react-diff-viewer-continued'
import { isUndefined } from 'lodash'
import Warnings from './Warnings'
import Errors from './Errors'

const FieldsDiffs = ({ element, field }) => {
  if (isEmpty(element.updated_and_changed[field])) {
      return null
  }
  const fieldDiffData = element.updated_and_changed[field]
  const newVal = fieldDiffData.newValue ?? ''
  const oldVal = fieldDiffData.oldValue ?? ''
  const changed = fieldDiffData.changed ?? false
  const hideLineNumbers = fieldDiffData.hideLineNumbers ?? true
  const splitView = fieldDiffData.splitView ?? true
  const leftTitle = fieldDiffData.leftTitle ?? gettext('Current')
  const rightTitle = fieldDiffData.rightTitle ?? gettext('Uploaded')
  const warnings = fieldDiffData.warnings ?? {}
  const errors = fieldDiffData.errors ?? []

  return (changed && !isUndefined(newVal) && !isUndefined(oldVal) &&
     <div className="col-sm-12">
      <ReactDiffViewer
          oldValue={oldVal.toString()}
          newValue={newVal.toString()}
          splitView={splitView}
          hideLineNumbers={hideLineNumbers}
          leftTitle={leftTitle}
          rightTitle={rightTitle}
          >
          </ReactDiffViewer>
      {
        !isEmpty(warnings) && <>
        <Warnings element={fieldDiffData} showTitle={true} shouldShowURI={false}/>
        </>
      }
      {
        !isEmpty(errors) && <>
        <Errors element={fieldDiffData} />
        </>
      }
      </div>
  )
}

FieldsDiffs.propTypes = {
  element: PropTypes.object.isRequired,
  field: PropTypes.string.isRequired,
}

export default FieldsDiffs
