import os
import yaml
from django.core.management.base import BaseCommand
from chatbot.models import *  # Adjust this import based on your model


class Command(BaseCommand):
    help = 'Import NLU data from the database and create nlu.yml'

    def handle(self, *args, **options):
        # Fetch NLU data from the database
        nlu_data = []
        for example in Intent.objects.all():
            intent = example.intent_name
            # text = example.text
            nlu_data.append({"intent": intent, "examples": [item.example_name for item in example.example.all()]})

        # Define the path to the output NLU YAML file
        output_file = os.path.join(os.getcwd(), 'nlu.yml')

        # Create a dictionary in the desired format
        # nlu_dict = {
        #     "version": "3.1",
        #     "nlu": [
        #         {"intent": intent, "examples": examples}
        #         for intent, examples in nlu_data.items()
        #     ]
        # }
        nlu_content = {
            "version": "3.1",
            "nlu": nlu_data
        }
        nlu_conten = dict(reversed(list(nlu_content.items())))

        # Write the NLU data to the YAML file with multiline scalar style
        with open(output_file, 'w') as yaml_file:
            yaml.dump(nlu_conten, yaml_file, default_flow_style=False)

        self.stdout.write(self.style.SUCCESS('NLU data imported and nlu.yml file created'))