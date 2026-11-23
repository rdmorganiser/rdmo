import React from 'react'
import PropTypes from 'prop-types'
import ReactSelect from 'react-select'

const Select = ({ options, onChange, value, ...props }) => {
  const selectedOption = options.find(option => option.value === value) || null

  const handleChange = (selected) => {
    onChange(selected ? selected.value : null)
  }

  return (
    <ReactSelect
      className="react-select"
      classNamePrefix="react-select"
      options={options}
      onChange={handleChange}
      value={selectedOption}
      isClearable
      {...props}
    />
  )
}

Select.propTypes = {
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  options: PropTypes.arrayOf(
    PropTypes.shape({
      value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
      label: PropTypes.oneOfType([PropTypes.string, PropTypes.node]).isRequired
    })
  ).isRequired,
  onChange: PropTypes.func,
}

export default Select
