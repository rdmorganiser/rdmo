// take the site_id from the <head> of the django template
export default Number(document.querySelector('meta[name="site_id"]').content)
