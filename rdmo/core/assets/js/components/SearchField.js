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
    <div className="input-group mb-0 search-field">
      <input
        type="text"
        className="form-control"
        placeholder={placeholder}
        value={value}
        onChange={(e) => handleChange(e.target.value)}
        onKeyDown={handleKeyDown}
        aria-label={gettext('Search')}
      />
      <button
        type="button" className="btn btn-light btn-reset border" onClick={handleButtonClick}
        title={gettext('Reset')} aria-label={gettext('Reset')}>
        <span className="bi bi-x"></span>
      </button>
      <button type="button" className="btn btn-primary" onClick={handleSearch}>
        {gettext('Search')}
      </button>
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
