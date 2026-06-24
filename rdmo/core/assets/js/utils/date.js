import { enGB, de, it, es, fr, fi} from 'date-fns/locale'
import { parse, set } from 'date-fns'

import lang from 'rdmo/core/assets/js/utils/lang'

export const getLocale = () => {
  switch (lang) {
    case 'de':
      return de
    case 'it':
      return it
    case 'es':
      return es
    case 'fr':
      return fr
    case 'fi':
      return fi
    default:
      return enGB
  }
}

export const getDateFormat = () => {
  switch (lang) {
    case 'de':
      return 'dd.MM.yyyy'
    case 'it':
      return 'dd/MM/yyyy'
    case 'es':
      return 'dd/MM/yyyy'
    case 'fr':
      return 'dd/MM/yyyy'
    case 'fi':
      return 'dd/MM/yyyy'
    default:
      return 'dd/MM/yyyy'
  }
}

export const parseDate = (value, end = false) => {
  if (!value) return null

  if (/^\d{2}$/.test(value)) {
    const date = parse(value, 'yy', new Date())
    return end ? set(date, { month: 11, date: 31 }) : date
  } else if (/^\d{4}$/.test(value)) {
    const date = parse(value, 'yyyy', new Date())
    return end ? set(date, { month: 11, date: 31 }) : date
  } else {
    return parse(value, getDateFormat(), new Date())
  }
}
