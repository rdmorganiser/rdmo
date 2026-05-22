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
  const newVal = fieldDiffData.newValue ?? ''
  const oldVal = fieldDiffData.oldValue ?? ''
  const changed = fieldDiffData.changed ?? false
  const compareMethod = fieldDiffData.compareMethod
  const splitView = false
  const hideLineNumbers = true
  const warnings = fieldDiffData.warnings ?? {}
  const errors = fieldDiffData.errors ?? []

  const newStyles = {
    variables: {
      light: {
        diffViewerBackground: '#fff',
        addedBackground: '#eafaf0',
        removedBackground: '#fff0f2',
        changedBackground: '#fff',
        gutterBackground: '#fff',
        wordAddedBackground: '#a7e8b8',
        wordRemovedBackground: '#f5b5bf',
      },
    },
    diffContainer: {
      minWidth: '100%',
      maxWidth: '100%',
      width: '100%',
    },
    marker: {
      width: '28px',
      minWidth: '28px',
      paddingLeft: 8,
      paddingRight: 4,
      textAlign: 'left',
      overflow: 'visible',
      pre: {
        backgroundColor: 'transparent',
        border: 'none',
        boxShadow: 'none',
        lineHeight: '1.6em',
        overflow: 'visible',
        padding: 0,
      },
    },
    contentText: {
      backgroundColor: '#fff !important',
      border: '1px solid #ccc',
      borderRadius: 4,
      display: 'block',
      lineHeight: '1.6em',
      overflowWrap: 'anywhere',
      padding: '5px 10px',
      wordBreak: 'break-word',
    },
  }

  return (changed &&
     <div className="field-diff col-sm-12 mt-10 mb-10">
      <ReactDiffViewer
          styles={newStyles}
          oldValue={oldVal}
          newValue={newVal}
          compareMethod={compareMethod}
          splitView={splitView}
          hideSummary={true}
          hideLineNumbers={hideLineNumbers}
          // leftTitle={leftTitle}
          // rightTitle={rightTitle}
          >
          </ReactDiffViewer>
      {
        !isEmpty(warnings) && <>
          <Warnings elementWarnings={fieldDiffData.warnings}
                    elementModel={element.model} elementURI={element.uri}
                    showTitle={true} shouldShowURI={false}/>
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
