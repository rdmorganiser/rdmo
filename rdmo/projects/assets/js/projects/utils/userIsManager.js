import siteId from 'rdmo/core/assets/js/utils/siteId'

const userIsManager = (currentUser) => {
  if (currentUser.is_superuser ||
     (currentUser.role && currentUser.role.manager && currentUser.role.manager.some(manager => manager.id === siteId))) {
      return true
  }
  return false
}

export default userIsManager
