import Cookies from 'js-cookie'
import isEmpty from 'lodash/isEmpty'

const checkStoreId = () => {
  const currentStoreId = Cookies.get('storeid')
  const localStoreId = localStorage.getItem('rdmo.storeid')

  if (isEmpty(localStoreId) || localStoreId !== currentStoreId) {
    localStorage.clear()
    localStorage.setItem('rdmo.storeid', currentStoreId)
  }
}

export { checkStoreId }
