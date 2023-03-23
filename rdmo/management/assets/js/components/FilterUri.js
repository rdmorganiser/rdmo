import React, { Component} from 'react'
import PropTypes from 'prop-types'

const FilterUri = ({ value, onChange, placeholder }) => {
  return (
    <div className="form-group mb-0">
      <div className="input-group">
        <input type="text" className="form-control" placeholder={placeholder}
               value={ value } onChange={e => onChange(e.target.value)}></input>
        <span className="input-group-btn">
          <button className="btn btn-default" onClick={e => onChange('')}>
            <span className="fa fa-times"></span>
          </button>
        </span>
      </div>
    </div>
  )
}

FilterUri.propTypes = {
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  placeholder: PropTypes.string.isRequired
}

export default FilterUri
