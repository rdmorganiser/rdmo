import { usePermissions } from './usePermissions'

export const useReadOnly = () => {
  const perms = usePermissions()

  return !(perms.can_add_value && perms.can_change_value && perms.can_delete_value)
}
