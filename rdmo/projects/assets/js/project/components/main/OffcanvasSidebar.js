import React from 'react'
import PropTypes from 'prop-types'

const OffcanvasSidebar = ({ menuItems, onNavigate, activePage }) => {
  return (
    <div className="offcanvas offcanvas-start show" data-bs-scroll="true" data-bs-backdrop="false" tabIndex="-1" id="offcanvasScrolling" aria-labelledby="offcanvasScrollingLabel">
      <div className="offcanvas-header">
        <h5 className="offcanvas-title" id="offcanvasScrollingLabel">TU dmo</h5>
        {/* <button type="button" className="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button> */}
      </div>
      <div className="offcanvas-body">
        <hr />
        <ul className="nav nav-pills flex-column mb-auto">
          {menuItems.map((section) => (
            <div key={section.title}>
              {section.title && <h6 className="text-muted mt-3 mb-2">{section.title}</h6>}
              {section.items.map((item) => (
                <li key={item.id} className="nav-item">
                  <button
                    className={`nav-link w-100 text-start d-flex align-items-center gap-2 ${activePage === item.id ? 'active' : 'text-dark'}`}
                    onClick={() => onNavigate(item.id)}
                    style={{ paddingLeft: '0.5rem' }}
                  >
                    <i className={`bi ${item.icon}`}></i>
                    {item.name}
                  </button>
                </li>
              ))}
            </div>
          ))}
        </ul>
        <div className="mt-auto pt-3">
          <a
            href="/projects"
            className="nav-link text-dark w-100 text-start d-flex align-items-center gap-2"
            style={{ paddingLeft: '0.5rem' }}
          >
            <i className="bi bi-arrow-left"></i> Zur Projektübersicht
          </a>
        </div>
      </div>
    </div>
  )
}

OffcanvasSidebar.propTypes = {
  menuItems: PropTypes.arrayOf(
    PropTypes.shape({
      title: PropTypes.string,
      items: PropTypes.arrayOf(
        PropTypes.shape({
          id: PropTypes.string.isRequired,
          name: PropTypes.string.isRequired,
          icon: PropTypes.string,
        })
      ).isRequired,
    })
  ).isRequired,
  onNavigate: PropTypes.func.isRequired,
  activePage: PropTypes.string.isRequired, // ✅ Added to track selected item
}

export default OffcanvasSidebar
