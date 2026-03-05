import { useState, useMemo, useCallback } from 'react'
import { enGB, de, it, es, fr } from 'date-fns/locale'
import { camelCase } from 'lodash'

import { language } from 'rdmo/core/assets/js/utils'

const useDatePicker = () => {
  const [dateRange, setDateRange] = useState({
    createdStart: null,
    createdEnd: null,
    lastChangedStart: null,
    lastChangedEnd: null
  })

  const dateFormat = useMemo(() => {
    return language === 'de' ? 'dd.MM.yyyy' : 'dd/MM/yyyy'
  }, [])

  const getLocale = () => {
    switch (language) {
      case 'de':
        return de
      case 'it':
        return it
      case 'es':
        return es
      case 'fr':
        return fr
      default:
        return enGB
    }
  }

  const setStartDate = useCallback((type, date) => {
    const camelCaseType = camelCase(type)
    const startKey = `${camelCaseType}Start`
    setDateRange(prev => ({ ...prev, [startKey]: date }))
  }, [])

  const setEndDate = useCallback((type, date) => {
    const camelCaseType = camelCase(type)
    const endKey = `${camelCaseType}End`
    setDateRange(prev => ({ ...prev, [endKey]: date }))
  }, [])

  return {
    dateRange,
    dateFormat,
    getLocale,
    setStartDate,
    setEndDate
  }
}

export default useDatePicker
