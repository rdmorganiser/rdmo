from django.contrib.sites.shortcuts import get_current_site

import rules

           
def is_editable_by_user(obj, user) -> bool:
    ''' checks permission for the given object and user '''
    
    # # compare the content_editor sites of the user with the sites_editors of the instance
    # if not is_locked:
    #     if self.serializer:
    #         instance_editable_by_user = is_editable_by_user(self.instance, self.serializer.context['request']._user)
    #         if not instance_editable_by_user:
    #             is_locked = True

    if not hasattr(obj, 'sites_editors'):
        # no sites_editors on object, so no locking (during development)
        return True

    if not user.role.editor.all().exists():
        # user has no content_editor rights
        return False

    obj_editable_by_sites = obj.sites_editors.all()
    user_role_sites_editors = user.role.content_editor.all()
    obj_editable_by_user = user_role_sites_editors.filter(id__in=obj_editable_by_sites).exists()

    return obj_editable_by_user


@rules.predicate
def is_object_editor(user, object):
    ''' Check if the user is a site editor for the object's site. '''
    
    if not user.is_authenticated:
        return False
    # if user is editor
    if not user.role.filter(name='editor').exists():
        return False
    if user.is_superuser or user.is_staff:
        return True
    
    user.groups.filter(name='editor') and user.role.members.filter(site=get_current_site(object))
    # and user.groups.filter(name='editor').sites.filter(id=get_current_site(request).id).exists()
    
        
    # current_site = get_current_site()
    if not user.role.manager.filter(pk=object._edited_by.site.pk).exists():
        return False
    # object._edited_by.site.pk
    # user
    return user in object.member
# or (project.parent and is_project_member(user, project.parent))

@rules.predicate
def is_instance_editor(user):
    if not user.is_authenticated:
        return False
    
    return user.role.instance_editor
        

@rules.predicate
def is_current_project_member(user, project):
    return user in project.member


rules.add_perm('projects.view_value_object', is_project_member | is_site_manager)
rules.add_perm('projects.add_value_object', is_project_author | is_project_manager | is_project_owner | is_site_manager)
rules.add_perm('projects.change_value_object', is_project_author | is_project_manager | is_project_owner | is_site_manager)
rules.add_perm('projects.delete_value_object', is_project_author | is_project_manager | is_project_owner | is_site_manager)

rules.add_perm('questions.view_questionset_object', is_project_member | is_site_manager)

# TODO: use one of the permissions above
rules.add_perm('projects.is_project_owner', is_project_owner)
