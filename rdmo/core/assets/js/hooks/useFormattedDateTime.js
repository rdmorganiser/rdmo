import { format } from 'date-fns'
import { de, enUS } from 'date-fns/locale'

const getLocaleObject = (language) => {
  return language === 'de' ? de : enUS
}

const FORMAT_STRINGS = {
  en: 'MMM d, yyyy, h:mm a',
  de: 'd. MMM yyyy, H:mm',
}

export const useFormattedDateTime  = (date, language) => {
  const locale = getLocaleObject(language)
  const formatString = language === 'de' ? FORMAT_STRINGS.de : FORMAT_STRINGS.en

  return format(new Date(date), formatString, { locale })
}

export default useFormattedDateTime
