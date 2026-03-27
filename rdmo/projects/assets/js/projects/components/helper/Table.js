import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const Table = ({
  cellFormatters,
  columnWidths,
  data,
  headerFormatters,
  onHeaderClick,
  sortableColumns,
  sortColumn,
  sortOrder,
  /* order of elements in 'visibleColumns' corresponds to order of columns in table */
  visibleColumns,
}) => {
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
                <th className={sortableColumns.includes(column) ? 'cursor-pointer' : undefined}
                  key={column} style={{ width: columnWidths[index] }} onClick={() => onHeaderClick(column)}
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
  onHeaderClick: PropTypes.func,
  sortableColumns: PropTypes.arrayOf(PropTypes.string),
  sortColumn: PropTypes.string,
  sortOrder: PropTypes.string,
  visibleColumns: PropTypes.arrayOf(PropTypes.string),
}

export default Table
