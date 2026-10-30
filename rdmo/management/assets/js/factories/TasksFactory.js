import { siteId } from 'rdmo/core/assets/js/utils/meta'

class TasksFactory {

  static createTask(settings) {
    return {
      model: 'tasks.task',
      uri_prefix: settings.default_uri_prefix,
      sites: settings.multisite ? [siteId] : [],
      editors: settings.multisite ? [siteId] : [],
      task_type: 'task'
    }
  }

}

export default TasksFactory
