import React from 'react'
import PropTypes from 'prop-types'
import Label from 'rdmo/management/assets/js/components/common/Labels'

const ChangedLabel = ({ text, onClick, show }) => {
  return <Label text={text}
                type="info"
                onClick={onClick}
                className={'ml-5'}
                show={show} />
}

ChangedLabel.propTypes = {
  text: PropTypes.string.isRequired,
  onClick: PropTypes.func,
  show: PropTypes.bool,
}

const CreatedLabel = ({ text, onClick, show }) => {
    return <Label text={text}
                type="success"
                onClick={onClick}
                className={'ml-5'}
                show={show} />
}

CreatedLabel.propTypes = {
  text: PropTypes.string.isRequired,
  onClick: PropTypes.func,
  show: PropTypes.bool,
}

export { ChangedLabel, CreatedLabel }
