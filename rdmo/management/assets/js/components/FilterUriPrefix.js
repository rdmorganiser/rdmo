import React, { Component} from 'react'
import PropTypes from 'prop-types'

const FilterUriPrefix = ({ value, options, onChange }) => {
  return (
    <div className="form-group mb-0">
      <select className="form-control" value={value} onChange={e => onChange(e.target.value)}>
        <option value="">{gettext('All URI prefixes')}</option>
        {
          options.map((option, index) => <option value={option} key={index}>{option}</option>)
        }
      </select>
    </div>
  )
}

FilterUriPrefix.propTypes = {
  options: PropTypes.array,
  value: PropTypes.string,
  onChange: PropTypes.func
}

export default FilterUriPrefix
