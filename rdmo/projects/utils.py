import logging

logger = logging.getLogger(__name__)


def is_last_owner(project, user):
    # check if user is owner
    if user in project.owners:
        # check if the user is the last owner
        return project.owners.count() <= 1
    else:
        return False


def save_import_values(project, values, checked):
    for value in values:
        if value['value'].attribute:
            value_key = '{value.attribute.uri}[{value.set_index}][{value.collection_index}]'.format(
                value=value['value']
            )

            if value_key in checked:
                current_value = value.get('current')
                if current_value is None:
                    value['value'].project = project
                    value['value'].save()
                else:
                    # make sure we have the correct value
                    assert current_value.snapshot is None
                    assert current_value.attribute == value['value'].attribute
                    assert current_value.set_index == value['value'].set_index
                    assert current_value.collection_index == value['value'].collection_index

                    current_value.text = value['value'].text
                    current_value.option = value['value'].option
                    current_value.value_type = value['value'].value_type
                    current_value.unit = value['value'].unit
                    current_value.save()


def save_import_snapshot_values(project, snapshots, checked):
    for snapshot in snapshots:
        snapshot['snapshot'].project = project
        snapshot['snapshot'].save(copy_values=False)

        for value in snapshot['values']:
            if value['value'].attribute:
                value_key = '{value.attribute.uri}[{snapshot_index}][{value.set_index}][{value.collection_index}]'.format(
                    value=value['value'],
                    snapshot_index=snapshot['index']
                )

                if value_key in checked:
                    value['value'].project = project
                    value['value'].snapshot = snapshot['snapshot']
                    value['value'].save()


def save_import_tasks(project, tasks):
    for task in tasks:
        project.tasks.add(task)


def save_import_views(project, views):
    for view in views:
        project.views.add(view)
