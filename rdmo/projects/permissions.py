from rdmo.core.permissions import HasObjectPermission


class HasProjectQuestionPermission(HasObjectPermission):

    def get_required_object_permissions(self, method, model_cls):
        return ('projects.view_questionset_object', )
