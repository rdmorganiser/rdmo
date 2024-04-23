import React from 'react'
import PropTypes from 'prop-types'

import baseUrl from 'rdmo/core/assets/js/utils/baseUrl'

const Breadcrump = ({ overview, currentPage, fetchPage }) => {

  const handleClick = (event) => {
    event.preventDefault()
    fetchPage(currentPage.section.first)
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
        <a href={`${baseUrl}/projects/${overview.id}/interview/${currentPage.section.first}/`} onClick={handleClick}>
          {currentPage.section.title}
        </a>
      </li>
    </ul>
  )
}

Breadcrump.propTypes = {
  overview: PropTypes.object.isRequired,
  currentPage: PropTypes.object.isRequired,
  fetchPage: PropTypes.func.isRequired
}

export default Breadcrump
