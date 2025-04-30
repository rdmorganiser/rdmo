// projects table
export const SORTABLE_COLUMNS = ['created', 'owner', 'progress', 'role', 'title', 'last_changed']
export const HEADER_FORMATTERS = {
  title: {render: () => gettext('Name')},
  role: {render: () => gettext('Role')},
  owner: {render: () =>  gettext('Owner')} ,
  progress: {render: () => gettext('Progress')},
  created: {render: () => gettext('Created')},
  last_changed: {render: () => gettext('Last changed')},
  actions: {render: () => null},
}
