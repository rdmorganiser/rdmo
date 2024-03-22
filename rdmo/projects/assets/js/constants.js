// projects table
export const INITIAL_TABLE_ROWS = '20'
export const ROWS_TO_LOAD = '10'
export const SORTABLE_COLUMNS = ['created', 'owner', 'progress', 'role', 'title', 'updated']
export const HEADER_FORMATTERS = {
  title: {render: () => gettext('Name')},
  role: {render: () => gettext('Role')},
  owner: {render: () =>  gettext('Owner')} ,
  progress: {render: () => gettext('Progress')},
  created: {render: () => gettext('Created')},
  updated: {render: () => gettext('Last changed')},
  actions: {render: () => null},
}

// date format
export const DATE_OPTIONS = {
  day: 'numeric',
  month: 'short',
  year: 'numeric',
  hour: 'numeric',
  minute: 'numeric'
}
