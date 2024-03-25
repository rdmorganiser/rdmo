import React from 'react'
import PropTypes from 'prop-types'

import baseUrl from 'rdmo/core/assets/js/utils/baseUrl'

const Breadcrump = ({ overview, page, onClick }) => {

  const handleClick = (event) => {
    event.preventDefault()
    onClick(page.section.first)
  }

  return (
    <ul className="interview-breadcrumb breadcrumb">
      <li>
        <a href={`${baseUrl}/projects/`}>
          {gettext('My Projects')}
        </a>
      </li>
      <li>
        <a href={`${baseUrl}/projects/${overview.id}/`}>
          {overview.title}
        </a>
      </li>
      <li>
        <a href={`${baseUrl}/projects/${overview.id}/interview/${page.section.first}/`} onClick={handleClick}>
          {page.section.title}
        </a>
      </li>
    </ul>
  )
}

Breadcrump.propTypes = {
  overview: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  onClick: PropTypes.func.isRequired
}

export default Breadcrump
