import isNil from 'lodash/isNil'

import { getData, postData, putData } from 'rdmo/core/assets/js/utils/api'

class TasksApi {

  static fetchTasks(index=false) {
    let url = '/api/v1/tasks/tasks/'
    if (index) url += 'index/'
    return getData(url)
  }

  static fetchTask(id) {
    return getData(`/api/v1/tasks/tasks/${id}/`)
  }

  static storeTask(task) {
    if (isNil(task.id)) {
      return postData(`/api/v1/tasks/tasks/`, task)
    } else {
      return putData(`/api/v1/tasks/tasks/${task.id}/`, task)
    }
  }

}

export default TasksApi
