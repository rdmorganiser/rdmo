// take the baseurl from the <head> of the django template
import { toNumber } from 'lodash'
export default toNumber(document.querySelector('meta[name="project"]').content.replace(/\/+$/, ''))
