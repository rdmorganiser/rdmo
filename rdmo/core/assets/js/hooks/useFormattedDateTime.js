import { format, parseISO } from 'date-fns'
import { de, enUS } from 'date-fns/locale'

const getLocaleObject = (language) => {
  return language === 'de' ? de : enUS
}

const FORMAT_STRINGS = {
  dateTime: {
    en: 'MMM d, yyyy, h:mm a',
    de: 'd. MMM yyyy, H:mm',
  },
  dateOnly: {
    en: 'MMM d, yyyy',
    de: 'd. MMM yyyy',
  },
}

export const useFormattedDateTime = (date, language, formatType = 'dateTime') => {
  const locale = getLocaleObject(language)
  const formatString = FORMAT_STRINGS[formatType][language] ?? FORMAT_STRINGS[formatType].en

  return format(parseISO(date), formatString, { locale })
}

export default useFormattedDateTime
