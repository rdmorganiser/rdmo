import { useState, useMemo, useCallback } from 'react'
import { de } from 'date-fns/locale'
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
    return language === 'de' ? 'dd.MM.yyyy' : 'MM/dd/yyyy'
  }, [])

  const getLocale = useCallback((lang) => {
    switch (lang) {
      case 'de':
        return de
      default:
        return undefined // defaults to English
    }
  }, [])

  const setStartDate = useCallback((type, date) => {
    const camelCaseType = camelCase(type)
    console.log(camelCaseType)
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
