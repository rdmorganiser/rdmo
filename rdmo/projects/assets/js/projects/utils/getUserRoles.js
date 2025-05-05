import { ROLE_LABELS } from './constants'

export const getUserRoles = (project, currentUserId, arraysToSearch) => {
  if (!arraysToSearch || !arraysToSearch.length) {
    arraysToSearch = ['authors', 'guests', 'managers', 'owners']
  }

  const roleDefinitions = {
    authors: { roleLabel: ROLE_LABELS.author, roleBoolean: 'isProjectAuthor' },
    guests: { roleLabel: ROLE_LABELS.guest, roleBoolean: 'isProjectGuest' },
    managers: { roleLabel: ROLE_LABELS.manager, roleBoolean: 'isProjectManager' },
    owners: { roleLabel: ROLE_LABELS.owner, roleBoolean: 'isProjectOwner' }
  }

  let rolesFound = []
  let roleBooleans = {
    isProjectAuthor: false,
    isProjectGuest: false,
    isProjectManager: false,
    isProjectOwner: false
  }

  arraysToSearch.forEach(arrayName => {
    if (project[arrayName].some(item => item.id === currentUserId)) {
      const { roleLabel, roleBoolean } = roleDefinitions[arrayName]
      rolesFound.push(roleLabel)
      roleBooleans[roleBoolean] = true
    }
  })

  return {
    rolesString: rolesFound.length > 0 ? rolesFound.join(', ') : null,
    ...roleBooleans
  }
}

export default getUserRoles
