// take the baseurl from the <head> of the django template
export default document.querySelector('meta[name="baseurl"]').content.replace(/\/+$/, '')
