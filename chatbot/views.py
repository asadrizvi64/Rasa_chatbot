import json
import threading

from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from chatbot.models import *
from rasa.core.agent import Agent
from .serializers import *
from chatbot.models import *
import os
import yaml
import sys, io
import ruamel.yaml
import subprocess
import requests
 # Adjust this import based on your model

# Create your views here.

yaml = ruamel.yaml.YAML()
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.core.events import UserUttered, ActionExecuted
from rasa.shared.core.constants import ACTION_LISTEN_NAME
# rasa_agent = Agent.load("rasa_bot/models")


def literalize_list(v):
    assert isinstance(v, list)
    buf = io.StringIO()
    yaml.dump(v, buf)
    return ruamel.yaml.scalarstring.LiteralScalarString(buf.getvalue())


def transform_value(d, key, transformation):
    """recursively walk over data structure to find key and apply transformation on the value"""
    if isinstance(d, dict):
        for k, v in d.items():
            if k == key:
                d[k] = transformation(v)
            else:
                transform_value(v, key, transformation)
    elif isinstance(d, list):
        for elem in d:
            transform_value(elem, key, transformation)


def run_rasa_command():
    command = 'rasa train'  # Assuming you pass the command as a JSON field
    working_directory = 'rasa_bot'  # Replace with the actual path
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True,
                            cwd=working_directory)
    # output = result.stdout
    # error = result.stderr


class NluApiView(APIView):
    def post(self, request):
        nlu_data = []
        for example in Intent.objects.all():
            intent = example.intent_name
            # text = example.text
            nlu_dat = {"intent": intent, "examples": [item.example_name for item in example.example.all()]}
            nlu_data.append(nlu_dat)
        # Define the path to the output NLU YAML file
        output_file = os.path.join(os.getcwd(), 'rasa_bot/data/nlu.yml')
        nlu_content = {
            "version": "3.1",
            "nlu": nlu_data
        }
        transform_value(nlu_content, 'examples', literalize_list)

        # Write the NLU data to the YAML file with multiline scalar style
        with open(output_file, 'w') as yaml_file:
            yaml.dump(nlu_content, yaml_file)
        return Response("ok")

        self.stdout.write(self.style.SUCCESS('NLU data imported and nlu.yml file created'))


class StoryApiView(APIView):
    def post(self, request):
        story_data = []
        for item in Story.objects.all():
            story = item.story
            # text = example.text
            nlu_dat = {"story": story, "steps": item.steps}
            story_data.append(nlu_dat)
        # Define the path to the output NLU YAML file
        output_file = os.path.join(os.getcwd(), 'rasa_bot/data/stories.yml')
        nlu_content = {
            "version": "3.1",
            "stories": story_data
        }
        transform_value(nlu_content, 'examples', literalize_list)

        # Write the NLU data to the YAML file with multiline scalar style
        with open(output_file, 'w') as yaml_file:
            yaml.dump(nlu_content, yaml_file)
        return Response("ok")

        self.stdout.write(self.style.SUCCESS('NLU data imported and nlu.yml file created'))


class DomainApiView(APIView):
    def post(self, request):
        response_data = {}
        docstring = '```'

        for item in Responses.objects.all():
            dic = []
            for i in item.response_text:
                for key, value in i.items():
                    dic.append({'text': f'''{value}'''})
            response_data[item.action] = dic
            # response_data.append(nlu_dat)
        # # Define the path to the output NLU YAML file
        output_file = os.path.join(os.getcwd(), 'rasa_bot/domain.yml')
        nlu_content = {
            "version": "3.1",
            "intents": [item.intent_name for item in Intent.objects.all()],
            "responses": response_data,
            "actions": [item.action_name for item in CustomAction.objects.all()]
        }
        transform_value(nlu_content, 'examples', literalize_list)

        # Write the NLU data to the YAML file with multiline scalar style
        with open(output_file, 'w') as yaml_file:
            yaml.dump(nlu_content, yaml_file)
        return Response("ok")

        self.stdout.write(self.style.SUCCESS('NLU data imported and nlu.yml file created'))


class RunRasaTrainCommandView(APIView):
    def post(self, request):
        command = 'rasa train' # Assuming you pass the command as a JSON field
        working_directory = 'rasa_bot'  # Replace with the actual path

        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True,
                                    cwd=working_directory)
            output = result.stdout
            error = result.stderr
            return Response({'output': output, 'error': error})
        except Exception as e:
            return Response({'error': str(e)})


class RunRasaServerCommandView(APIView):
    def post(self, request):
        command = 'rasa run -m models --enable-api --cors “*” --debug' # Assuming you pass the command as a JSON field
        working_directory = 'rasa_bot'  # Replace with the actual path
        thread = threading.Thread(target=run_rasa_command)
        thread.start()
        return Response({"msg": "run rasa command"})


class RunCustomActionCommandView(APIView):
    def post(self, request):
        command = 'rasa run actions' # Assuming you pass the command as a JSON field
        working_directory = 'rasa_bot'  # Replace with the actual path

        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True,
                                    cwd=working_directory)
            output = result.stdout
            error = result.stderr
            return Response({'output': output, 'error': error})
        except Exception as e:
            return Response({'error': str(e)})


class TerminateRasaServerView(APIView):

    def post(self, request, format=None):
        rasa_server_url = "http://0.0.0.0:5005"
        response = requests.post(f'{rasa_server_url}/terminate')
        if response.status_code == 200:
            return Response('Rasa server terminated successfully.')
        else:
            return Response('Failed to terminate Rasa server.')


class ChatbotView(APIView):
    def post(self, request, format=None):
        rasa_endpoint = "http://0.0.0.0:5005"  # Replace with your actual Rasa API endpoint

        # Prepare the message payload
        message = {
            "message": "Hello, Rasa!",
        }

        # Send a POST request to the Rasa API
        response = requests.post(f"{rasa_endpoint}/webhooks/rest/webhook", json=message)

        # Check if the request was successful
        if response.status_code == 200:
            rasa_response = response.json()
            # Process the Rasa response as needed
            return Response(rasa_response, safe=False)
        else:
            # Handle the error, e.g., return an error response
            return Response({"error": "Failed to communicate with Rasa."})
            # user_message = request.data.get('message')  # Assuming the message is sent as a POST parameter
        # if user_message:
        #     pass
        #     # response = rasa_agent.handle_text(user_message)
        #     # bot_response = response[0]['text']
        #     # return Response({'message': bot_response})
        # else:
        #     return Response({'error': 'Please provide a message'}, status=status.HTTP_400_BAD_REQUEST)


class ChatView(TemplateView):
    template_name: str = "chat/chat.html"


def index_view(request):
    return render(request, 'chat/index.html', {
        'rooms': Room.objects.all(user=request.user),
    })




class GetPolicyInfo(APIView):
    def post(self, request):
        policy_number = request.data.get('policy_number')
        policy_info = PolicyInformation.objects.filter(policy_number=policy_number).first()
        if policy_info:
            serializer = PolicyInformationSerializer(policy_info)
            return Response(serializer.data)
        return Response({"msg": "you have no policy with this policy_number"})


class ApiCall(APIView):
    def post(self, request):
      end_point = "http://127.0.0.1:8000/chatbot/get_policy_info"
      data = {
          "policy_number": "123456"
      }
      response = requests.post(end_point, json=data)
      response = json.loads(response.text)
      return Response(response)


class RoomView(APIView):
    serializer_class = RoomSerializer

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        room = Room.objects.latest('id')
        room.name = f'{room.name}_{room.id}'
        room.save()
        return Response(serializer.data)


class ResponsesViewSeT(ModelViewSet):
    queryset = Responses.objects.all()
    serializer_class = ResponsesSerializer


class ContractorViewSet(ModelViewSet):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer


class DefinitionViewSet(ModelViewSet):
    queryset = Definition.objects.all()
    serializer_class = DefinitionSerializer


class InsuranceTypeViewSet(ModelViewSet):
    queryset = InsuranceType.objects.all()
    serializer_class = InsuranceTypeSerializer
