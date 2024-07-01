import React from 'react'
import PropTypes from 'prop-types'
import Label from 'rdmo/management/assets/js/components/common/Labels'

const ChangedLabel = ({ onClick, show }) => {
  return <Label text={gettext('changed')}
                type="info"
                onClick={onClick}
                className={'ml-5'}
                show={show} />
}

ChangedLabel.propTypes = {
  onClick: PropTypes.func,
  show: PropTypes.bool,
}

const CreatedLabel = ({ onClick, show }) => {
    return <Label text={gettext('created')}
                type="success"
                onClick={onClick}
                className={'ml-5'}
                show={show} />
}

CreatedLabel.propTypes = {
  onClick: PropTypes.func,
  show: PropTypes.bool,
}

export { ChangedLabel, CreatedLabel }
