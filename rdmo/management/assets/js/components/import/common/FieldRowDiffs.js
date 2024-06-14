import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'
import ReactDiffViewer from 'react-diff-viewer-continued'
import Warnings from './Warnings'
import Errors from './Errors'

const FieldRowDiffs = ({ element, field }) => {
  if (isEmpty(element.updated_and_changed[field])) {
      return null
  }
  const fieldDiffData = element.updated_and_changed[field]
  const newVal = fieldDiffData.newValue.toString() ?? ''
  const oldVal = fieldDiffData.oldValue.toString() ?? ''
  const changed = fieldDiffData.changed ?? false
  const splitView = false
  const hideLineNumbers = true
  const warnings = fieldDiffData.warnings ?? {}
  const errors = fieldDiffData.errors ?? []

  const newStyles = {
    variables: {
      light: {
        diffViewerBackground: '#fff',
        changedBackground: '#fff',
        gutterBackground: '#fff',
      },
    },
    contentText: {
      backgroundColor: '#fff !important',
    },
  }

  return (changed &&
     <div className="field-diff col-sm-12 mt-10 mb-10">
      <ReactDiffViewer
          styles={newStyles}
          oldValue={oldVal}
          newValue={newVal}
          splitView={splitView}
          hideLineNumbers={hideLineNumbers}
          // leftTitle={leftTitle}
          // rightTitle={rightTitle}
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

FieldRowDiffs.propTypes = {
  element: PropTypes.object.isRequired,
  field: PropTypes.string.isRequired,
}

export default FieldRowDiffs
