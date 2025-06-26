import React from 'react'
import { useSelector } from 'react-redux'

import Dashboard from './pages/Dashboard'
// import Interview from '../pages/Interview'
// import Documents from '../pages/Documents'
// import Snapshots from '../pages/Snapshots'
// import Membership from '../pages/Membership'
import ProjectData from './pages/ProjectData'

const ProjectPage = () => {
  // Get Redux state
  // const config = useSelector((state) => state.config)
  // const settings = useSelector((state) => state.settings)
  // const templates = useSelector((state) => state.templates)
  // const currentUser = useSelector((state) => state.user.currentUser)
  // const project = useSelector((state) => state.project.project)
  // const catalogs = useSelector((state) => state.catalogs)

  // console.log('Project:', project)
  // console.log('User:', currentUser)
  // console.log('Settings: ', settings)
  // console.log('Config:', config)
  // console.log('Catalogs:', catalogs)
  // console.log('settings', settings)
  // console.log('templates', templates)
  // console.log('currentUser', currentUser)

  // const dispatch = useDispatch()

  const page = useSelector((state) => state.config.page)

  switch (page) {
    case '':
      return <Dashboard />
    // case 'interview':
    //   return <Interview />
    // case 'documents':
    //   return <Documents />
    // case 'snapshots':
    //   return <Snapshots />
    case 'project-information':
      return <ProjectData />
      // case 'membership':
      // return <Membership />
    default:
      return <h2>Page Not Found</h2>
  }
}

export default ProjectPage
