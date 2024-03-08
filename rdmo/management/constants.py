
from rdmo.conditions.models import Condition
from rdmo.domain.models import Attribute
from rdmo.options.models import Option, OptionSet
from rdmo.questions.models import Catalog, Page, Question, QuestionSet, Section
from rdmo.tasks.models import Task
from rdmo.views.models import View

RDMO_MODEL_PATH_MAPPER = {
    'conditions.condition': Condition,
    'domain.attribute': Attribute,
    'options.optionset': OptionSet,
    'options.option': Option,
    'questions.catalog': Catalog,
    'questions.section': Section,
    'questions.page': Page,
    'questions.questionset': QuestionSet,
    'questions.question': Question,
    'tasks.task': Task,
    'views.view': View
    }
