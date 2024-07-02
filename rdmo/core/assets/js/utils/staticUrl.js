// take the staticurl from the <head> of the django template
export default document.querySelector('meta[name="staticurl"]').content.replace(/\/+$/, '')
