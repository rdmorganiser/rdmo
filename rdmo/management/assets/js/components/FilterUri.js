import React, { Component} from 'react'
import PropTypes from 'prop-types'

const FilterUri = ({ value, onChange }) => {
  return (
    <div className="form-group">
      <div className="input-group">
        <input type="text" className="form-control" placeholder={gettext('Search')}
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
  value: PropTypes.string,
  onChange: PropTypes.func
}

export default FilterUri
