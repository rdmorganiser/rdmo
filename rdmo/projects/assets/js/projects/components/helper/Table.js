import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { get } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

import { fetchProjects } from '../../actions/projectsActions'

import EmptyTableRow from '../../../common/components/EmptyTableRow'

const Table = ({
  cellFormatters,
  columnWidths,
  data,
  headerFormatters,
  sortableColumns,
  emptyMessage,
  emptyActionLabel,
  onEmptyAction,
  /* order of elements in 'visibleColumns' corresponds to order of columns in table */
  visibleColumns,
}) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

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

  const handleHeaderClick = (column) => {
    if (sortableColumns.includes(column)) {
      if (sortColumn === column && sortOrder === 'asc') {
        dispatch(updateConfig('params.ordering', `-${column}`))
      } else {
        dispatch(updateConfig('params.ordering', column))
      }

      dispatch(fetchProjects())
    }
  }

  const renderSortIcon = (column) => {
    const isSortColumn = sortColumn === column

    let icon = 'bi-caret-down'
    if (isSortColumn && sortOrder === 'asc') icon = 'bi-caret-down-fill'
    if (isSortColumn && sortOrder === 'desc') icon = 'bi-caret-up-fill'

    return (
      <span className="ms-1 sort-icon">
        <i className={classNames('bi font-smaller', icon)} aria-hidden="true" />
      </span>
    )
  }

  const renderHeaders = () => {
    return (
      <thead>
        <tr>
          {
            visibleColumns.map((column, index) => {
              const headerFormatter = headerFormatters[column]
              const columnHeaderContent = headerFormatter && headerFormatter.render ? (
                headerFormatter.render(column)
              ) : column
              const columnHeaderLabel = headerFormatter && headerFormatter.label ? (
                headerFormatter.label(column)
              ) : columnHeaderContent

              return (
                <th
                  className={sortableColumns.includes(column) ? 'cursor-pointer' : undefined}
                  key={column} style={{ width: columnWidths[index] }} onClick={() => handleHeaderClick(column)}
                  aria-label={columnHeaderLabel}>
                  {columnHeaderContent}
                  {sortableColumns.includes(column) && renderSortIcon(column)}
                </th>
              )
            })
          }
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
        {
          data?.length ? (
            data.map((row) => (
              <tr key={row.id}>
                {
                  visibleColumns.map((column, index) => (
                    <td key={column} style={{ width: columnWidths[index] }}>
                      {formatCellContent(row, column, row[column])}
                    </td>
                  ))
                }
              </tr>
            ))
          ) : (
            emptyMessage && (
              <EmptyTableRow
                label={emptyActionLabel}
                colSpan={visibleColumns.length}
                message={emptyMessage}
                onClick={onEmptyAction}
              />
            )
          )
        }
      </tbody>
    )
  }

  return (
    <div id="projects-table" className="table-container">
      <table className="table">
        {renderHeaders()}
        {renderRows()}
      </table>
    </div>
  )
}

Table.propTypes = {
  cellFormatters: PropTypes.object,
  columnWidths: PropTypes.arrayOf(PropTypes.string),
  data: PropTypes.arrayOf(PropTypes.object).isRequired,
  headerFormatters: PropTypes.object,
  sortableColumns: PropTypes.arrayOf(PropTypes.string),
  visibleColumns: PropTypes.arrayOf(PropTypes.string),
  emptyMessage: PropTypes.string,
  emptyActionLabel: PropTypes.string,
  onEmptyAction: PropTypes.func,
}

export default Table
