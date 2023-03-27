class TasksFactory {

  static createTask(config) {
    return {
      uri_prefix: config.default_uri_prefix
    }
  }

}

export default TasksFactory
