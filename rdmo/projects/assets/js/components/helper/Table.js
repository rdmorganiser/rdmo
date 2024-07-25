import React from 'react'
import PropTypes from 'prop-types'
import { get } from 'lodash'

const Table = ({
  cellFormatters,
  columnWidths,
  config,
  configActions,
  data,
  hasNext,
  headerFormatters,
  projectsActions,
  showTopButton = false,
  scrollToTop,
  sortableColumns,
  /* order of elements in 'visibleColumns' corresponds to order of columns in table */
  visibleColumns,
}) => {
  const page = get(config, 'params.page') ?? 1

  const extractSortingParams = (params) => {
    const { ordering } = params || {}

    if (!ordering) {
        return { sortOrder: undefined, sortColumn: undefined }
    }

    const sortOrder = ordering.startsWith('-') ? 'desc' : 'asc'
    const sortColumn = sortOrder === 'desc' ? ordering.substring(1) : ordering

    return { sortColumn, sortOrder }
  }

  const params = get(config, 'params', {})
  const { sortColumn, sortOrder } = extractSortingParams(params)

  const loadMore = () => {
    configActions.updateConfig('params.page', (parseInt(page) + 1).toString())
    projectsActions.fetchAllProjects()
  }

  const renderLoadButtons = () => {
    return (
          <div className="icon-container ml-auto">
            {data.length > 0 && showTopButton &&
              <button className="elliptic-button" onClick={scrollToTop} title={gettext('Scroll to top')}>
                <i className="fa fa-arrow-up" aria-hidden="true"></i>
              </button>
            }
            {hasNext &&
            <button onClick={loadMore} className="elliptic-button">
              {gettext('Load more')}
            </button>
            }
          </div>
    )
  }

  const handleHeaderClick = (column) => {
    if (sortableColumns.includes(column)) {
      if (sortColumn === column) {
        if (sortOrder === 'asc') {
          configActions.updateConfig('params.ordering', `-${column}`)
        } else if (sortOrder === 'desc') {
          configActions.deleteConfig('params.ordering')
        } else {
        configActions.updateConfig('params.ordering', column)
        }
      } else {
        configActions.updateConfig('params.ordering', column)
      }
      projectsActions.fetchAllProjects()
    }
  }

  const renderSortIcon = (column) => {
    const isSortColumn = sortColumn === column
    const isAsc = sortOrder === 'asc'

    return (
      <span className="ml-5 sort-icon">
        <i className={`fa fa-sort${isSortColumn ? isAsc ? '-asc' : '-desc' : ''} ${isSortColumn ? '' : 'text-muted'}`} />
      </span>
    )
  }

  const renderHeaders = () => {
    return (
      <thead className="thead-dark">
        <tr>
          {visibleColumns.map((column, index) => {
            const headerFormatter = headerFormatters[column]
            const columnHeaderContent = headerFormatter && headerFormatter.render ? headerFormatter.render(column) : column

            return (
              <th key={column} style={{ width: columnWidths[index] }} onClick={() => handleHeaderClick(column)}>
                {columnHeaderContent}
                {sortableColumns.includes(column) && renderSortIcon(column)}
              </th>
            )
          })}
        </tr>
      </thead>
    )
  }

  const formatCellContent = (row, column, content) => {
    if (cellFormatters && cellFormatters[column] && typeof cellFormatters[column] === 'function') {
      return cellFormatters[column](content, row)
    }
    return content
  }

  const renderRows = () => {
    return (
      <tbody>
        {data.map((row, index) => (
          <tr key={index}>
            {visibleColumns.map((column, index) => (
              <td key={column} style={{ width: columnWidths[index] }}>
                {formatCellContent(row, column, row[column])}
                </td>
            ))}
          </tr>
        ))}
      </tbody>
    )
  }

  return (
    <div id="projects-table" className="table-container">
      <table className="table table-borderless">
        {renderHeaders()}
        {renderRows()}
      </table>
      {renderLoadButtons()}
    </div>
  )
}

Table.propTypes = {
  cellFormatters: PropTypes.object,
  columnWidths: PropTypes.arrayOf(PropTypes.string),
  config: PropTypes.object,
  configActions: PropTypes.object,
  data: PropTypes.arrayOf(PropTypes.object).isRequired,
  hasNext: PropTypes.bool.isRequired,
  headerFormatters: PropTypes.object,
  projectsActions: PropTypes.object,
  showTopButton: PropTypes.bool,
  scrollToTop: PropTypes.func,
  sortableColumns: PropTypes.arrayOf(PropTypes.string),
  visibleColumns: PropTypes.arrayOf(PropTypes.string),
}

export default Table
