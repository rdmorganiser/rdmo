import React from 'react'
import PropTypes from 'prop-types'

const SearchField = ({ value, onChange, onSearch, placeholder }) => {

  const handleSearch = () => {
    onSearch(value)
  }

  const handleChange = (newValue) => {
    onChange(newValue)
  }

  const handleButtonClick = () => {
    onChange('')
    handleSearch()
  }

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className="form-group mb-0">
      <div className="input-group">
        <input
          type="text"
          className="form-control"
          placeholder={placeholder}
          value={value}
          onChange={(e) => handleChange(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <span className="input-group-btn">
          <button className="btn btn-default" onClick={handleButtonClick}>
            <span className="fa fa-times"></span>
          </button>
          <button className="btn btn-primary" onClick={handleSearch}>
            {gettext('Search')}
          </button>
        </span>
      </div>
    </div>
  )
}

SearchField.propTypes = {
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  onSearch: PropTypes.func.isRequired,
  placeholder: PropTypes.string.isRequired,
}

export default SearchField
