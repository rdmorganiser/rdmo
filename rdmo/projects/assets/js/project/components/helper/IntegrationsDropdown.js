import React from 'react'
import PropTypes from 'prop-types'
import { Dropdown } from 'bootstrap'

const IntegrationsDropdown = ({ providers, onChange }) => {
  const handleClick = (event, providerKey) => {
    event.stopPropagation()

    onChange(providerKey)

    const dropdownElement = event.currentTarget.closest('.dropdown')?.querySelector('[data-bs-toggle="dropdown"]')
    const dropdown = Dropdown.getInstance(dropdownElement)
    dropdown?.hide()
  }

  return (
    <div className="dropdown dropdown-menu-end">
      <button
        type="button"
        className="link text-nowrap"
        data-bs-toggle="dropdown"
        data-bs-popper-config='{"strategy":"fixed"}'
        aria-expanded="false"
        onClick={(event) => event.stopPropagation()}
        title={gettext('Add integration')}
      >
        <i className="bi bi-plus-lg me-1" aria-hidden="true" />
        <span>{gettext('Add integration')}</span>
        <i className="bi bi-caret-down-fill ms-1" aria-hidden="true" />
      </button>

      <ul className="dropdown-menu">
        {
          Object.entries(providers).map(([key, provider]) => (
            <li key={key}>
              <button
                type="button"
                className="dropdown-item"
                onClick={(event) => handleClick(event, key)}
              >
                {provider.label}
              </button>
            </li>
          ))
        }
      </ul>
    </div>
  )
}

IntegrationsDropdown.propTypes = {
  providers: PropTypes.object.isRequired,
  onChange: PropTypes.func.isRequired
}

export default IntegrationsDropdown
