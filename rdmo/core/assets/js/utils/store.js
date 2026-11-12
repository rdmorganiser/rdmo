import Cookies from 'js-cookie'
import isEmpty from 'lodash/isEmpty'

import { removeFromStale } from '../actions/staleActions'

// bump this when the format of the data in the local storage changes
const STORE_VERSION = '2'

export const checkStoreId = () => {
  const currentStoreId = Cookies.get('storeid')
  const localStoreId = localStorage.getItem('rdmo.storeid')
  const localStoreVersion = localStorage.getItem('rdmo.storeversion')

  if (isEmpty(localStoreId) || localStoreId !== currentStoreId || localStoreVersion !== STORE_VERSION) {
    localStorage.clear()
    localStorage.setItem('rdmo.storeid', currentStoreId)
    localStorage.setItem('rdmo.storeversion', STORE_VERSION)
  }
}

export const configureStaleRefresh = (store, refreshers) => {
  window.addEventListener('pageshow', () => {
    store.getState().stale.items.forEach((item) => {
      const refresh = refreshers[item]

      if (refresh) {
        Promise.resolve()
          .then(refresh)
          .then(() => store.dispatch(removeFromStale(item)))
          .catch(() => {})
      }
    })
  })
}

export const configureLeaveWarning = (store, shouldWarn) => {
  window.addEventListener('beforeunload', (event) => {
    if (shouldWarn(store.getState())) {
      event.preventDefault()
      event.returnValue = ''  // needed for older browsers
    }
  })
}
