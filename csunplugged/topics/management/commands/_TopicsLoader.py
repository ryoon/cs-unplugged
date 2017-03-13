from django.db import transaction
from utils.BaseLoader import BaseLoader
from ._FollowUpActivitiesLoader import FollowUpActivitiesLoader
from ._ProgrammingExercisesLoader import ProgrammingExercisesLoader
from ._UnitPlanLoader import UnitPlanLoader
from topics.models import Topic


class TopicsLoader(BaseLoader):
    """Loader for the topics content"""

    def __init__(self, structure, BASE_PATH):
        """Initiates the learning outcomes loader

        Args:
            structure: dictionary containing list of topics, each with
            a dictionary of attributes.
        """
        super().__init__(BASE_PATH)
        self.structure = structure

    @transaction.atomic
    def load(self):
        """load the content for topics"""
        for topic_structure in self.structure['topics']:
            topic_data = self.convert_md_file(self.BASE_PATH.format(topic_structure['md-file']))

            # If other resources are given, convert to html
            other_resources_file = topic_structure['other-resources-md-file']
            if other_resources_file:
                md_data = self.convert_md_file(self.BASE_PATH.format(other_resources_file))
                other_resources_html = md_data.html_string
            else:
                other_resources_html = ''

            # Create topic objects and save to the db
            topic = Topic(
                slug=topic_structure['slug'],
                name=topic_data.title,
                content=topic_data.html_string,
                other_resources=other_resources_html,
                icon=topic_structure['icon']
            )
            topic.save()
            self.log('Added Topic: {}'.format(topic.name))

            # Load unit plans
            for unit_plan_structure_file in topic_structure['unit-plans']:
                UnitPlanLoader(
                    self.load_log,
                    unit_plan_structure_file,
                    topic,
                    self.BASE_PATH
                ).load()

            # Load programming exercises (if there are any)
            if topic_structure['programming-exercises']:
                ProgrammingExercisesLoader(
                    self.load_log,
                    topic_structure['programming-exercises'],
                    topic,
                    self.BASE_PATH
                ).load()

            # Load follow up activities (if there are any)
            if topic_structure['follow-up-activities']:
                FollowUpActivitiesLoader(
                    self.load_log,
                    topic_structure['follow-up-activities'],
                    topic,
                    self.BASE_PATH
                ).load()

        # Print log output
        self.print_load_log()