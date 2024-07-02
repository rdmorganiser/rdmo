import React from 'react'
import PropTypes from 'prop-types'
import ReactSelect from 'react-select'

const Select = ({ options, onChange, placeholder, value }) => {
  const selectedOption = options.find(option => option.value === value) || null
  const handleChange = (selected) => {
    onChange(selected ? selected.value : null)
  }

  return (
    <div className="form-group mb-0">
      <ReactSelect
        className="react-select"
        classNamePrefix="react-select"
        options={options}
        onChange={handleChange}
        value={selectedOption}
        isClearable
        placeholder={placeholder}
      />
    </div>
  )
}

Select.propTypes = {
  value: PropTypes.string,
  options: PropTypes.arrayOf(
    PropTypes.shape({
      value: PropTypes.string.isRequired,
      label: PropTypes.string.isRequired
    })
  ).isRequired,
  onChange: PropTypes.func,
  placeholder: PropTypes.string
}

export default Select
