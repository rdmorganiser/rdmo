import React, { useState } from 'react'
import PropTypes from 'prop-types'

const ButtonGroup = ({ buttons }) => {
  const [activeButton, setActiveButton] = useState(buttons[0].type)

  const handleButtonClick = (buttonType, onClick) => {
    setActiveButton(buttonType)
    onClick && onClick()
  }

  return (
    <div className="btn-group">
      {buttons.map((button) => (
        <button
          key={button.type}
          type="button"
          className={`btn ${activeButton === button.type ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => handleButtonClick(button.type, button.onClick)}
        >
          {button.label}
        </button>
      ))}
    </div>
  )
}

ButtonGroup.propTypes = {
  buttons: PropTypes.arrayOf(
    PropTypes.shape({
      label: PropTypes.string.isRequired,
      type: PropTypes.string.isRequired,
      onClick: PropTypes.func,
    })
  ).isRequired,
}

export default ButtonGroup
