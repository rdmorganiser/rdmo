import React from 'react'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

const Progress = ({ progress, help }) => {

  const low = progress.ratio <= 0.25
  const width = progress.ratio * 100
  const label = interpolate(gettext('%s of %s'), [progress.count, progress.total])

  return (
    <>
      <h2>{gettext('Progress')}</h2>
      <Html html={help} />

      <div className="interview-progress">
        {low && <div className="interview-progress-count">{label}</div>}

        <div className="progress">
          <div className="progress-bar" role="progressbar" style={{width: `${width}%`}}>
            {!low && <span>{label}</span>}
          </div>
        </div>
      </div>
    </>
  )
}

Progress.propTypes = {
  progress: PropTypes.object.isRequired,
  help: PropTypes.string.isRequired
}

export default Progress
