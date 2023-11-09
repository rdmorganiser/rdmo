import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'
import ReactDiffViewer from 'react-diff-viewer-continued'


const Diffs = ({ element, field }) => {
  return !isEmpty(element.diffs[field]) && <div className="col-sm-12">
    <ReactDiffViewer
        oldValue={element.diffs[field].new_value}
        newValue={element.diffs[field].old_value}
        splitView={true}
        hideLineNumbers={true}
        leftTitle={gettext('Current')}
        rightTitle={gettext('Imported')}
        >
        </ReactDiffViewer>
    </div>
}

Diffs.propTypes = {
  element: PropTypes.object.isRequired,
  field: PropTypes.string.isRequired,
}

export default Diffs
