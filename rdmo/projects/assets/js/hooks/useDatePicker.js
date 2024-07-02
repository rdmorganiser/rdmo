import { useState, useMemo, useCallback } from 'react'
import { de } from 'date-fns/locale'
import { language } from 'rdmo/core/assets/js/utils'

const useDatePicker = () => {
    const [dateRange, setDateRange] = useState({
        createdStart: null,
        createdEnd: null,
        updatedStart: null,
        updatedEnd: null
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
        setDateRange(prev => ({ ...prev, [`${type}Start`]: date }))
    }, [])

    const setEndDate = useCallback((type, date) => {
        setDateRange(prev => ({ ...prev, [`${type}End`]: date }))
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
