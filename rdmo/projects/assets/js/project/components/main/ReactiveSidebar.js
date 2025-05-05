import React from 'react'
import PropTypes from 'prop-types'

const ReactiveSidebar = ({ menuItems, onNavigate, activePage }) => {
  return (
    <>
      <button
        className="btn btn-outline-secondary d-lg-none m-2 p-2"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#sidebarOffcanvas"
        aria-controls="sidebarOffcanvas"
        style={{ position: 'fixed', top: '10px', left: '10px', zIndex: 1050, borderRadius: '8px' }}
      >
        <i className="bi bi-list" style={{ fontSize: '1.5rem' }}></i>
      </button>

      <div
        // className="offcanvas-lg offcanvas-start bg-light d-flex flex-column"
        className="offcanvas-lg offcanvas-start d-flex flex-column text-light sidebar-custom shadow-sm"
        tabIndex="-1"
        id="sidebarOffcanvas"
        aria-labelledby="sidebarOffcanvasLabel"
        style={{ width: '250px', height: '100vh' }}
      >
        <div className="p-3 pb-0">
          <h5 className="fw-bold mb-0">TU dmo</h5>
          <hr className="mb-0" />
        </div>

        <div className="offcanvas-body d-flex flex-column p-3 flex-grow-1">
          <ul className="nav nav-pills flex-column mb-auto">
            {menuItems.map((section) => (
              <div key={section.title}>
                {section.title && <h6 className="text-muted mt-3 mb-2">{section.title}</h6>}

                {section.items.map((item) => (
                  <li key={item.id} className="nav-item">
                    <button
                      className={`nav-link w-100 text-start d-flex align-items-center gap-2 ${activePage === item.id ? 'active' : 'text-light'}`}
                      onClick={() => {
                        onNavigate(item.id)
                      }}
                    >
                      <i className={`bi ${item.icon}`}></i>
                      {item.name}
                    </button>
                  </li>
                ))}
              </div>
            ))}
          </ul>
        </div>

        <div className="p-3 mt-auto">
          {/* <a href="/projects" className="nav-link text-dark w-100 text-start d-flex align-items-center gap-2"> */}
          <a href="/projects" className="nav-link text-light w-100 text-start d-flex align-items-center gap-2">

            <i className="bi bi-arrow-left"></i> {gettext('Back to projects overview')}
          </a>
        </div>
      </div>
    </>
  )
}

ReactiveSidebar.propTypes = {
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
  activePage: PropTypes.string.isRequired,
}

export default ReactiveSidebar
