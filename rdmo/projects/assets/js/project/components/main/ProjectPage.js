import React from 'react'
import PropTypes from 'prop-types'
// import { useSelector, useDispatch } from 'react-redux'
import { useSelector } from 'react-redux'
import Dashboard from '../pages/Dashboard'
// import DataManagement from '../pages/DataManagement'
// import Questionnaire from '../pages/Questionnaire'
// import Documents from '../pages/Documents'
import ProjectData from '../pages/ProjectData'

const ProjectPage = ({ activePage }) => {
  // Get Redux state
  const config = useSelector((state) => state.config)
  const settings = useSelector((state) => state.settings)
  // const templates = useSelector((state) => state.templates)
  const currentUser = useSelector((state) => state.user.currentUser)
  // const project = useSelector((state) => state.project.project)
  const catalogs = useSelector((state) => state.catalogs)

  // console.log('Project:', project)
  console.log('User:', currentUser)
  console.log('Settings: ', settings)
  console.log('Config:', config)
  console.log('Catalogs:', catalogs)
  // console.log('settings', settings)
  // console.log('templates', templates)
  // console.log('currentUser', currentUser)

  // const dispatch = useDispatch()

  const renderPage = (activePage) => {
    switch (activePage) {
      case 'dashboard':
        return <Dashboard />
      // case 'data-management':
      //   return <DataManagement settings={settings} />
      // case 'questionnaire':
      //   return <Questionnaire />
      // case 'documents':
      //   return <Documents />
      case 'project-data':
        return <ProjectData />
      default:
        return <h2>Page Not Found</h2>
    }
  }

  return (
    <div className="project-page-wrapper">
      <div className="project-page-container">
        {renderPage(activePage)}
      </div>
    </div>
  )
}

ProjectPage.propTypes = {
  activePage: PropTypes.string.isRequired
}

export default ProjectPage
