import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const Link = ({ href='', title, className, disabled=false, onClick, children }) => {
    const handleClick = (event) => {
        event.preventDefault()
        if (!disabled) onClick()
    }

    const classnames = classNames({
        [className]: true,
        disabled: disabled
    })

    return (
        <a href={href} title={title} className={classnames}
           onClick={event => handleClick(event)}>
            {children}
        </a>
    )
}

Link.propTypes = {
  href: PropTypes.string,
  title: PropTypes.string,
  className: PropTypes.string,
  disabled: PropTypes.bool,
  onClick: PropTypes.func.isRequired,
  children: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.node), PropTypes.node])
}

export default Link
