import React from 'react'
import PropTypes from 'prop-types'
// import ButtonGroup from 'rdmo/core/assets/js/components/ButtonGroup'

const Projects = ({ projects }) => {
  // useEffect(() => {
  //   projectsActions.fetchProjects()
  // }, [projectsActions.fetchProjects()])

// const handleMyProjectsClick = () => {
//   // Custom logic for 'My projects' button click
// }

// const handleAllProjectsClick = () => {
//   // Custom logic for 'All projects' button click
// }


// const buttons = [
//   { label: 'My projects', type: 'myProjects', onClick: handleMyProjectsClick },
//   { label: 'All projects', type: 'allProjects', onClick: handleAllProjectsClick },
//   // Add more buttons as needed
// ]

console.log('projects', projects.projects)
// console.log(projectList.map((project) => project.title))
// projectList.forEach((project) => {
//   console.log(project.title)
// })

  const renderProjects = () => {
    return projects.projects.map(project => {
      console.log('project %o', project)
      project?.title || 'no projects' })
  }

  return (
    <>
    {/* <ButtonGroup buttons={buttons} /> */}
      <div>
        {'Test'}
        {/* Render projects */}
        {renderProjects()}
      </div></>
  )
}

Projects.propTypes = {
  // projectsActions: PropTypes.object.isRequired,
  projects: PropTypes.object.isRequired,
}

export default Projects
