import { isNil } from 'lodash'

export const getParentPath = (projects, parentId, pathArray = []) => {
  const parent = projects.find((project) => project.id === parentId)
  if (parent) {
    const { title: parentTitle, parent: grandParentId } = parent
    pathArray.unshift(parentTitle)
    if (!isNil(grandParentId) && typeof grandParentId === 'number') {
      return getParentPath(projects, grandParentId, pathArray)
    }
  }
  return pathArray
}

export const getTitlePath = (projects, title, row) => {
  let parentPath = ''
  if (row.parent) {
    const path = getParentPath(projects, row.parent)
    parentPath = path.join(' / ')
  }

  const pathArray = parentPath ? [parentPath, title] : [title]
  return pathArray.join(' / ')
}
