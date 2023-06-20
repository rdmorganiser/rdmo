import React from 'react'
import PropTypes from 'prop-types'

const LinkButton = ({ title, className, disabled=false, onClick, children }) => {
    const handleClick = (event) => {
        event.preventDefault()
        onClick()
    }

    return (
        <button title={title} className={'btn-link ' + className} disabled={disabled}
                onClick={event => handleClick(event)}>
            {children}
        </button>
    )
}

LinkButton.propTypes = {
  title: PropTypes.string,
  className: PropTypes.string,
  disabled: PropTypes.bool,
  onClick: PropTypes.func.isRequired,
  children: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.node), PropTypes.node])
}

export default LinkButton
