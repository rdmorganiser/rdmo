import React from 'react'
import PropTypes from 'prop-types'

const Progress = ({ progress, help }) => {
  const low = progress.ratio <= 0.25
  const width = progress.ratio * 100
  const label = interpolate(gettext('%s of %s'), [progress.count, progress.total])

  return (
    <>
      <h2>{gettext('Progress')}</h2>

      <div className="interview-progress-help" dangerouslySetInnerHTML={{
        '__html': help
      }}></div>

      <div className="interview-progress">
        {low && <div className="interview-progress-count" dangerouslySetInnerHTML={{ __html: label }} />}

        <div className="progress">
          <div className="progress-bar" role="progressbar" style={{width: `${width}%`}}>
            {!low && <span dangerouslySetInnerHTML={{ __html: label }} />}
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
