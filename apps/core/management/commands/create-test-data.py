from django.core.management.base import BaseCommand
from django.utils import translation

from apps.domain.testing.factories import *
from apps.conditions.testing.factories import *
from apps.questions.testing.factories import *
from apps.tasks.testing.factories import *
from apps.projects.testing.factories import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        translation.activate('en')

        # domain

        AttributeEntityFactory(id=1, title='test')

        catalog = CatalogFactory(id=1, title='RDMO')

        ##################
        # single widgets #
        ##################

        AttributeEntityFactory(id=11, parent_entity_id=1, title='single')

        AttributeEntityFactory(id=111, parent_entity_id=11, title='1')
        AttributeEntityFactory(id=112, parent_entity_id=11, title='2')
        AttributeEntityFactory(id=113, parent_entity_id=11, title='3')
        AttributeEntityFactory(id=114, parent_entity_id=11, title='4')

        section = SectionFactory(id=1, catalog=catalog, order=1, title='Single')

        subsection = SubsectionFactory(id=11, section=section, order=1, title='Text')

        AttributeFactory(id=1111, parent_entity_id=111, title='text', value_type='text')
        AttributeFactory(id=1112, parent_entity_id=111, title='integer', value_type='integer')
        AttributeFactory(id=1113, parent_entity_id=111, title='float', value_type='float')

        QuestionFactory(id=1111, subsection=subsection, order=1, attribute_entity_id=1111, widget_type='text', text='text')
        QuestionFactory(id=1112, subsection=subsection, order=2, attribute_entity_id=1112, widget_type='text', text='integer')
        QuestionFactory(id=1113, subsection=subsection, order=3, attribute_entity_id=1113, widget_type='text', text='float')

        subsection = SubsectionFactory(id=12, section=section, order=2, title='Widgets')

        AttributeFactory(id=1121, parent_entity_id=112, title='textarea', value_type='text')
        AttributeFactory(id=1122, parent_entity_id=112, title='yesno', value_type='boolean')

        QuestionFactory(id=1121, subsection=subsection, order=1, attribute_entity_id=1121, widget_type='textarea', text='textarea')
        QuestionFactory(id=1122, subsection=subsection, order=2, attribute_entity_id=1122, widget_type='yesno', text='yesno')

        AttributeFactory(id=1131, parent_entity_id=113, title='date', value_type='datetime')
        AttributeFactory(id=1132, parent_entity_id=113, title='range', value_type='float')

        QuestionFactory(id=1131, subsection=subsection, order=3, attribute_entity_id=1131, widget_type='date', text='date')
        QuestionFactory(id=1132, subsection=subsection, order=4, attribute_entity_id=1132, widget_type='range', text='range')

        subsection = SubsectionFactory(id=13, section=section, order=3, title='Options')

        AttributeFactory(id=1141, parent_entity_id=114, title='radio', value_type='options')
        AttributeFactory(id=1142, parent_entity_id=114, title='select', value_type='options')
        AttributeFactory(id=1143, parent_entity_id=114, title='checkbox', value_type='options')

        QuestionFactory(id=1141, subsection=subsection, order=1, attribute_entity_id=1141, widget_type='radio', text='radio')
        QuestionFactory(id=1142, subsection=subsection, order=2, attribute_entity_id=1142, widget_type='select', text='select')
        QuestionFactory(id=1143, subsection=subsection, order=3, attribute_entity_id=1143, widget_type='checkbox', text='checkbox')

        ######################
        # collection widgets #
        ######################

        AttributeEntityFactory(id=12, parent_entity_id=1, title='collection')

        AttributeEntityFactory(id=121, parent_entity_id=12, title='1')
        AttributeEntityFactory(id=122, parent_entity_id=12, title='2')
        AttributeEntityFactory(id=123, parent_entity_id=12, title='3')
        AttributeEntityFactory(id=124, parent_entity_id=12, title='4')

        section = SectionFactory(id=2, catalog=catalog, order=2, title='Collection')

        subsection = SubsectionFactory(id=21, section=section, order=1, title='Text')

        AttributeFactory(id=1211, parent_entity_id=121, is_collection=True, title='text', value_type='text')
        AttributeFactory(id=1212, parent_entity_id=121, is_collection=True, title='integer', value_type='integer')
        AttributeFactory(id=1213, parent_entity_id=121, is_collection=True, title='float', value_type='float')

        QuestionFactory(id=1211, subsection=subsection, order=1, attribute_entity_id=1211, widget_type='text', text='text')
        QuestionFactory(id=1212, subsection=subsection, order=2, attribute_entity_id=1212, widget_type='text', text='integer')
        QuestionFactory(id=1213, subsection=subsection, order=3, attribute_entity_id=1213, widget_type='text', text='float')

        subsection = SubsectionFactory(id=22, section=section, order=2, title='Widgets')

        AttributeFactory(id=1221, parent_entity_id=122, is_collection=True, title='textarea', value_type='text')
        AttributeFactory(id=1222, parent_entity_id=122, is_collection=True, title='yesno', value_type='boolean')

        QuestionFactory(id=1221, subsection=subsection, order=1, attribute_entity_id=1221, widget_type='textarea', text='textarea')
        QuestionFactory(id=1222, subsection=subsection, order=2, attribute_entity_id=1222, widget_type='yesno', text='yesno')

        AttributeFactory(id=1231, parent_entity_id=123, is_collection=True, title='date', value_type='datetime')
        AttributeFactory(id=1232, parent_entity_id=123, is_collection=True, title='range', value_type='float')

        QuestionFactory(id=1231, subsection=subsection, order=3, attribute_entity_id=1231, widget_type='date', text='date')
        QuestionFactory(id=1232, subsection=subsection, order=4, attribute_entity_id=1232, widget_type='range', text='range')

        subsection = SubsectionFactory(id=23, section=section, order=3, title='Options')

        AttributeFactory(id=1241, parent_entity_id=124, is_collection=True, title='radio', value_type='options')
        AttributeFactory(id=1242, parent_entity_id=124, is_collection=True, title='select', value_type='options')

        QuestionFactory(id=1241, subsection=subsection, order=1, attribute_entity_id=1241, widget_type='radio', text='radio')
        QuestionFactory(id=1242, subsection=subsection, order=2, attribute_entity_id=1242, widget_type='select', text='select')

        ###############
        # set widgets #
        ###############

        AttributeEntityFactory(id=13, parent_entity_id=1, title='set_single')

        AttributeEntityFactory(id=131, parent_entity_id=13, title='1')
        AttributeEntityFactory(id=132, parent_entity_id=13, title='2')
        AttributeEntityFactory(id=133, parent_entity_id=13, title='3')
        AttributeEntityFactory(id=134, parent_entity_id=13, title='4')

        section = SectionFactory(id=3, catalog=catalog, order=3, title='Set')

        subsection = SubsectionFactory(id=31, section=section, order=1, title='Text')

        entity = QuestionEntityFactory(id=131, subsection=subsection, order=1, attribute_entity_id=131)

        AttributeFactory(id=1311, parent_entity_id=131, title='text', value_type='text')
        AttributeFactory(id=1312, parent_entity_id=131, title='integer', value_type='integer')
        AttributeFactory(id=1313, parent_entity_id=131, title='float', value_type='float')

        QuestionFactory(id=1311, subsection=subsection, parent_entity=entity, order=1, attribute_entity_id=1311, widget_type='text', text='text')
        QuestionFactory(id=1312, subsection=subsection, parent_entity=entity, order=2, attribute_entity_id=1312, widget_type='text', text='integer')
        QuestionFactory(id=1313, subsection=subsection, parent_entity=entity, order=3, attribute_entity_id=1313, widget_type='text', text='float')

        entity = QuestionEntityFactory(id=132, subsection=subsection, order=2, attribute_entity_id=132)

        AttributeFactory(id=1321, parent_entity_id=132, title='textarea', value_type='text')
        AttributeFactory(id=1322, parent_entity_id=132, title='yesno', value_type='boolean')

        QuestionFactory(id=1321, subsection=subsection, parent_entity=entity, order=1, attribute_entity_id=1321, widget_type='textarea', text='textarea')
        QuestionFactory(id=1322, subsection=subsection, parent_entity=entity, order=2, attribute_entity_id=1322, widget_type='yesno', text='yesno')

        entity = QuestionEntityFactory(id=133, subsection=subsection, order=3, attribute_entity_id=133)

        AttributeFactory(id=1331, parent_entity_id=133, title='date', value_type='datetime')
        AttributeFactory(id=1332, parent_entity_id=133, title='range', value_type='float')

        QuestionFactory(id=1331, subsection=subsection, parent_entity=entity, order=1, attribute_entity_id=1331, widget_type='date', text='date')
        QuestionFactory(id=1332, subsection=subsection, parent_entity=entity, order=2, attribute_entity_id=1332, widget_type='range', text='range')

        entity = QuestionEntityFactory(id=134, subsection=subsection, order=4, attribute_entity_id=134)

        AttributeFactory(id=1341, parent_entity_id=134, title='radio', value_type='options')
        AttributeFactory(id=1342, parent_entity_id=134, title='select', value_type='options')
        AttributeFactory(id=1343, parent_entity_id=134, title='checkbox', value_type='options')

        QuestionFactory(id=1341, subsection=subsection, parent_entity=entity, order=1, attribute_entity_id=1341, widget_type='radio', text='radio')
        QuestionFactory(id=1342, subsection=subsection, parent_entity=entity, order=2, attribute_entity_id=1342, widget_type='select', text='select')
        QuestionFactory(id=1343, subsection=subsection, parent_entity=entity, order=3, attribute_entity_id=1343, widget_type='checkbox', text='checkbox')

        ##########################
        # set colelction widgets #
        ##########################

        AttributeEntityFactory(id=14, parent_entity_id=1, title='set_collection', is_collection=True)

        AttributeEntityFactory(id=141, parent_entity_id=14, title='1')
        AttributeEntityFactory(id=142, parent_entity_id=14, title='2')
        AttributeEntityFactory(id=143, parent_entity_id=14, title='3')
        AttributeEntityFactory(id=144, parent_entity_id=14, title='4')

        AttributeFactory(id=1410, parent_entity_id=14, title='id', value_type='text')

        section = SectionFactory(id=4, catalog=catalog, order=4, title='Set collection')

        subsection = SubsectionFactory(id=41, section=section, order=4, title='Text')

        entity = QuestionEntityFactory(id=141, subsection=subsection, order=1, attribute_entity_id=141)

        AttributeFactory(id=1411, parent_entity_id=141, is_collection=True, title='text', value_type='text')
        AttributeFactory(id=1412, parent_entity_id=141, is_collection=True, title='integer', value_type='integer')
        AttributeFactory(id=1413, parent_entity_id=141, is_collection=True, title='float', value_type='float')

        QuestionFactory(id=1411, subsection=subsection, parent_entity=entity, order=1, attribute_entity_id=1411, widget_type='text', text='text')
        QuestionFactory(id=1412, subsection=subsection, parent_entity=entity, order=2, attribute_entity_id=1412, widget_type='text', text='integer')
        QuestionFactory(id=1413, subsection=subsection, parent_entity=entity, order=3, attribute_entity_id=1413, widget_type='text', text='float')

        entity = QuestionEntityFactory(id=142, subsection=subsection, order=2, attribute_entity_id=142)

        AttributeFactory(id=1421, parent_entity_id=142, is_collection=True, title='textarea', value_type='text')
        AttributeFactory(id=1422, parent_entity_id=142, is_collection=True, title='yesno', value_type='boolean')

        QuestionFactory(id=1421, subsection=subsection, parent_entity=entity, order=1, attribute_entity_id=1421, widget_type='textarea', text='textarea')
        QuestionFactory(id=1422, subsection=subsection, parent_entity=entity, order=2, attribute_entity_id=1422, widget_type='yesno', text='yesno')

        entity = QuestionEntityFactory(id=143, subsection=subsection, order=3, attribute_entity_id=143)

        AttributeFactory(id=1431, parent_entity_id=143, is_collection=True, title='date', value_type='datetime')
        AttributeFactory(id=1432, parent_entity_id=143, is_collection=True, title='range', value_type='float')

        QuestionFactory(id=1431, subsection=subsection, parent_entity=entity, order=1, attribute_entity_id=1431, widget_type='date', text='date')
        QuestionFactory(id=1432, subsection=subsection, parent_entity=entity, order=2, attribute_entity_id=1432, widget_type='range', text='range')

        entity = QuestionEntityFactory(id=144, subsection=subsection, order=4, attribute_entity_id=144)

        AttributeFactory(id=1441, parent_entity_id=144, is_collection=True, title='radio', value_type='options')
        AttributeFactory(id=1442, parent_entity_id=144, is_collection=True, title='select', value_type='options')

        QuestionFactory(id=1441, subsection=subsection, parent_entity=entity, order=1, attribute_entity_id=1441, widget_type='radio', text='radio')
        QuestionFactory(id=1442, subsection=subsection, parent_entity=entity, order=2, attribute_entity_id=1442, widget_type='select', text='select')

        ##############
        # conditions #
        ##############

        AttributeEntityFactory(id=15, parent_entity_id=1, title='conditions')

        section = SectionFactory(id=5, catalog=catalog, order=5, title='Conditions')

        # single condition

        subsection = SubsectionFactory(id=51, section=section, order=1, title='Condition')

        condition_yesno = AttributeFactory(id=1510, parent_entity_id=15, title='condition_yesno', value_type='bool')
        condition_attribute = AttributeFactory(id=1511, parent_entity_id=15, title='condition_attribute', value_type='text')

        QuestionFactory(id=1510, subsection=subsection, order=1, attribute_entity_id=1510, widget_type='yesno', text='condition_bool')
        QuestionFactory(id=1511, subsection=subsection, order=2, attribute_entity_id=1511, widget_type='text', text='condition_attribute')

        condition_attribute.conditions.add(ConditionFactory(id=51, source=condition_yesno))

        # condition for set

        subsection = SubsectionFactory(id=52, section=section, order=2, title='Condition set')

        condition_yesno = AttributeFactory(id=1520, parent_entity_id=15, title='condition_set_yesno', value_type='bool')
        condition_entity = AttributeEntityFactory(id=152, parent_entity_id=15, title='condition_set_entity')

        AttributeFactory(id=1521, parent_entity_id=152, title='condition_set_attribute', value_type='text')

        QuestionFactory(id=1520, subsection=subsection, order=1, attribute_entity_id=1520, widget_type='yesno', text='condition_set_bool')

        entity = QuestionEntityFactory(id=152, subsection=subsection, order=2, attribute_entity_id=152)
        QuestionFactory(id=1521, subsection=subsection, parent_entity=entity, order=1, attribute_entity_id=1521, widget_type='text', text='condition_set_attribute')

        condition_entity.conditions.add(ConditionFactory(id=52, source=condition_yesno))

        # condition for set collection

        subsection = SubsectionFactory(id=53, section=section, order=3, title='Condition set collection')

        condition_yesno = AttributeFactory(id=1530, parent_entity_id=15, title='condition_set_collection_yesno', value_type='bool')
        condition_entity = AttributeEntityFactory(id=153, is_collection=True, parent_entity_id=15, title='condition_set_collection_entity')

        AttributeFactory(id=1531, parent_entity_id=153, title='id', value_type='text')
        AttributeFactory(id=1532, parent_entity_id=153, title='text', value_type='text')

        QuestionFactory(id=1530, subsection=subsection, order=1, attribute_entity_id=1530, widget_type='yesno', text='condition_set_collection_bool')

        entity = QuestionEntityFactory(id=153, subsection=subsection, order=2, attribute_entity_id=153)
        QuestionFactory(id=1532, subsection=subsection, parent_entity=entity, order=1, attribute_entity_id=1532, widget_type='text', text='condition_set_collection_attribute')

        condition_entity.conditions.add(ConditionFactory(id=53, source=condition_yesno))

        #########
        # tasks #
        #########

        AttributeEntityFactory(id=16, parent_entity_id=1, title='tasks')

        section = SectionFactory(id=6, catalog=catalog, order=6, title='Tasks')

        subsection = SubsectionFactory(id=61, section=section, order=1, title='Task')

        task_yesno = AttributeFactory(id=1610, parent_entity_id=16, title='task_condition_bool', value_type='bool')
        task_attribute = AttributeFactory(id=1611, parent_entity_id=16, title='task_date', value_type='datetime')

        QuestionFactory(id=1610, subsection=subsection, order=1, attribute_entity_id=1610, widget_type='yesno', text='task_condition_bool')
        QuestionFactory(id=1611, subsection=subsection, order=2, attribute_entity_id=1611, widget_type='date', text='task_date')

        task = TaskFactory(id=1610, attribute=task_attribute)
        task.conditions.add(ConditionFactory(id=61, source=task_yesno))

        ## project

        ProjectFactory(catalog=catalog, owner=[1])
