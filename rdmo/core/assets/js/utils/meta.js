// take information from the <head> of the django template

export const baseUrl = document.querySelector('meta[name="baseurl"]').content.replace(/\/+$/, '')

export const staticUrl = document.querySelector('meta[name="staticurl"]').content.replace(/\/+$/, '')

export const siteId = Number(document.querySelector('meta[name="site_id"]').content)

export const language = document.querySelector('meta[name="language"]').content

export const executeScriptTags = document.querySelector('meta[name="execute_script_tags"]')?.content === 'true'
