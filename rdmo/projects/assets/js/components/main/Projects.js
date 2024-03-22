import React, {useEffect, useState} from 'react'
import PropTypes from 'prop-types'
import Table from '../helper/Table'
import Link from 'rdmo/core/assets/js/components/Link'
import { SearchField } from 'rdmo/core/assets/js/components/SearchAndFilter'
import FileUploadButton from 'rdmo/core/assets/js/components/FileUploadButton'
import language from 'rdmo/core/assets/js/utils/language'
import userIsManager from '../../utils/userIsManager'
import { getTitlePath } from '../../utils/getProjectTitlePath'
import { DATE_OPTIONS, HEADER_FORMATTERS, SORTABLE_COLUMNS } from '../../constants'
import { get } from 'lodash'

const Projects = ({ config, configActions, currentUserObject, projectsActions, projectsObject }) => {
  const { projects } = projectsObject
  const { currentUser } = currentUserObject
  const { myProjects } = config

  const [showTopButton, setShowTopButton] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      if (window.pageYOffset > 100) {
        setShowTopButton(true)
      } else {
        setShowTopButton(false)
      }
    }

    window.addEventListener('scroll', handleScroll)

    return () => {
      window.removeEventListener('scroll', handleScroll)
    }
  }, [])

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const displayedRows = get(config, 'tableRows', '')

  const currentUserId = currentUser.id
  const isManager = userIsManager(currentUser)

  const searchString = get(config, 'params.search', '')
  const updateSearchString = (value) => {
    const normedValue = value.toLowerCase()
    normedValue ? configActions.updateConfig('params.search', normedValue) : configActions.deleteConfig('params.search')
  }

  const baseUrl = window.location.origin

  const langOptions = language == 'de' ?
  { hour12: false } :
  { hour12: true }

  const dateOptions = {
    ...langOptions,
    DATE_OPTIONS
  }

  const viewLinkText = myProjects ? gettext('View all projects') : gettext('View my projects')
  const headline = myProjects ? gettext('My projects') : gettext('All projects')

  const handleView = () => {
    configActions.updateConfig('myProjects', !myProjects)
    myProjects ? configActions.deleteConfig('params.user') : configActions.updateConfig('params.user', currentUserId)
    projectsActions.fetchAllProjects()
  }

  const handleNew = () => {
    window.location.href = `${baseUrl}/projects/create`
  }

  const handleImport = (file) => { projectsActions.uploadProject('/projects/import/', file) }

  const renderTitle = (title, row) => {
    const pathArray = getTitlePath(projects, title, row).split(' / ')
    const lastChild = pathArray.pop()

    return (
      <a href={`${baseUrl}/projects/${row.id}`}>
        {pathArray.map((path, index) => (
          <span key={index}>{path} / </span>
        ))}
        <b>{lastChild}</b>
      </a>
    )
  }

  /* order of elements in 'visibleColumns' corresponds to order of columns in table */
  let visibleColumns = ['title', 'progress', 'updated', 'actions']
  let columnWidths

  if (myProjects) {
    visibleColumns.splice(2, 0, 'role')
    columnWidths = ['25%', '20%', '20%', '20%', '5%']
  } else {
    visibleColumns.splice(2, 0, 'created')
    visibleColumns.splice(2, 0, 'owner')
    columnWidths = ['25%', '10%', '20%', '20%', '20%', '5%']
  }

  const cellFormatters = {
    title: (content, row) => renderTitle(content, row),
    role: (_content, row) => {
      const arraysToSearch = ['authors', 'guests', 'managers', 'owners']
      let foundInArrays = []
      arraysToSearch.forEach(arrayName => {
        if (row[arrayName].some(item => item.id === currentUserId)) {
          let name = arrayName.charAt(0).toUpperCase() + arrayName.slice(1, -1)
          foundInArrays.push(gettext(name))
        }
      })
      return foundInArrays.length > 0 ? gettext(foundInArrays.join(', ')) : null
    },
    owner: (_content, row) => row.owners.map(owner => `${owner.first_name} ${owner.last_name}`).join('; '),
    progress: (_content, row) => `${row.progress_count ?? 0} ${gettext('of')} ${row.progress_total ?? 0}`,
    created: content => new Date(content).toLocaleString(language, dateOptions),
    updated: content => new Date(content).toLocaleString(language, dateOptions),
    actions: (_content, row) => {
      const rowUrl = `${baseUrl}/projects/${row.id}`
      const path = `?next=${window.location.pathname}`

      return (
        <div className="icon-container">
          <Link
            href={`${rowUrl}/update`}
            className="element-link fa fa-pencil"
            title={row.title}
            onClick={() => window.location.href = `${rowUrl}/update/${path}`}
          />
          <Link
            href={`${rowUrl}/delete`}
            className="element-link fa fa-trash"
            title={row.title}
            onClick={() => window.location.href = `${rowUrl}/delete/${path}`}
          />
        </div>
      )
    }
  }

  return (
    <>
      <div className="mb-10" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 className="ml-10 mt-0">{headline}</h2>
        <div className="icon-container ml-auto">
          <button className="btn btn-link mr-10" onClick={handleNew}>
            <i className="fa fa-plus" aria-hidden="true"></i> {gettext('New project')}
          </button>
          <FileUploadButton
           acceptedTypes={['application/xml', 'text/xml']}
           buttonProps={{'className': 'btn btn-link'}}
           buttonText={gettext('Import project')}
           onImportFile={handleImport}
          />
        </div>
      </div>
      <span>{parseInt(displayedRows) > projects.length ? projects.length : displayedRows} {gettext('of')} {projects.length} {gettext('projects are displayed')}</span>
      <div className="panel-body">
        <div className="row">
          <SearchField
            value={searchString}
            onChange={updateSearchString}
            onSearch={projectsActions.fetchAllProjects}
            placeholder={gettext('Search projects')}
          />
        </div>
      </div>
      {isManager &&
      <div className="mb-10">
        <Link className="element-link mb-20" onClick={handleView}>
            {viewLinkText}
        </Link>
      </div>
      }
      <Table
        cellFormatters={cellFormatters}
        columnWidths={columnWidths}
        config={config}
        configActions={configActions}
        data={projects}
        headerFormatters={HEADER_FORMATTERS}
        projectsActions={projectsActions}
        showTopButton={showTopButton}
        scrollToTop={scrollToTop}
        sortableColumns={SORTABLE_COLUMNS}
        visibleColumns={visibleColumns}
      />
    </>
  )
}

Projects.propTypes = {
  config: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  currentUserObject: PropTypes.object.isRequired,
  projectsActions: PropTypes.object.isRequired,
  projectsObject: PropTypes.object.isRequired,
}

export default Projects
