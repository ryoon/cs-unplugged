"""Custom loader for loading a topic."""

import os.path
from django.db import transaction
from utils.BaseLoader import BaseLoader
from ._CurriculumIntegrationsLoader import CurriculumIntegrationsLoader
from ._ProgrammingExercisesLoader import ProgrammingExercisesLoader
from ._UnitPlanLoader import UnitPlanLoader
from topics.models import Topic


class TopicLoader(BaseLoader):
    """Custom loader for loading a topic."""

    def __init__(self, structure_file, BASE_PATH):
        """Create the loader for loading a topic.

        Args:
            structure_file: File path for structure YAML file (string).
            BASE_PATH: Base file path (string).
        """
        super().__init__(BASE_PATH)
        self.structure_file = os.path.join(self.BASE_PATH, structure_file)
        self.BASE_PATH = os.path.join(self.BASE_PATH, os.path.split(structure_file)[0])

    @transaction.atomic
    def load(self):
        """Load the content for a topic."""
        topic_structure = self.load_yaml_file(self.structure_file)
        topic_data = self.convert_md_file(os.path.join(self.BASE_PATH, topic_structure['md-file']))

        # If other resources are given, convert to html
        other_resources_file = topic_structure['other-resources-md-file']
        if other_resources_file:
            md_data = self.convert_md_file(os.path.join(self.BASE_PATH, other_resources_file))
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

        # Load programming exercises (if there are any)
        if topic_structure['programming-exercises']:
            ProgrammingExercisesLoader(
                self.load_log,
                topic_structure['programming-exercises'],
                topic,
                self.BASE_PATH
            ).load()

        # Load unit plans
        for unit_plan_structure_file in topic_structure['unit-plans']:
            UnitPlanLoader(
                self.load_log,
                unit_plan_structure_file,
                topic,
                self.BASE_PATH
            ).load()

        # Load curriculum integrations (if there are any)
        if topic_structure['curriculum-integrations']:
            CurriculumIntegrationsLoader(
                self.load_log,
                topic_structure['curriculum-integrations'],
                topic,
                self.BASE_PATH
            ).load()

        # Print log output
        self.print_load_log()