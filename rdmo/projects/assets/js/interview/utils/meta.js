// take the baseurl from the <head> of the django template
import { toNumber } from 'lodash'
export const projectId = toNumber(document.querySelector('meta[name="project"]').content.replace(/\/+$/, ''))
