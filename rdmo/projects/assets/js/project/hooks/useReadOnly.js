import { isReadOnly } from '../../common/utils/permissions'

import { usePermissions } from './usePermissions'

export const useReadOnly = () => isReadOnly(usePermissions())
