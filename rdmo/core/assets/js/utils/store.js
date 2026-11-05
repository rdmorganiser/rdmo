import Cookies from 'js-cookie'
import isEmpty from 'lodash/isEmpty'

import { removeFromStale } from '../actions/staleActions'

export const checkStoreId = () => {
  const currentStoreId = Cookies.get('storeid')
  const localStoreId = localStorage.getItem('rdmo.storeid')

  if (isEmpty(localStoreId) || localStoreId !== currentStoreId) {
    localStorage.clear()
    localStorage.setItem('rdmo.storeid', currentStoreId)
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
