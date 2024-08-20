from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import AgentSerializer, CrewSerializer, TaskSerializer, EdgeSerializer, ContextBinSerializer, EdgeSourceTargetRelatedField
from rest_framework.decorators import api_view
from .models import Agent, Crew, Edge, ContextBin, Task
from .crew_hub.workflow_hub import workflow_hub 
import pandas as pd


# Create your views here.
@api_view(['POST', 'GET'])
def run_Crew(request):
    agents = Agent.objects.all()
    relations = Edge.objects.all()
    tasks = Task.objects.all()
    contexts = ContextBin.objects.all()

    agent_df = pd.DataFrame(list(agents.values()))
    print("#######################################################")
    print("AGENT DF:")
    print(agent_df)
    print("#######################################################")
    relations_df = pd.json_normalize(list(relations.values()), sep='_')
    task_df = pd.DataFrame(list(tasks.values()))
    context_df = pd.DataFrame(list(contexts.values()))

    print("#######################################################")
    print("Relations DF:")
    print(relations_df)
    print("#######################################################")

    print("#######################################################")
    print("task DF:")
    print(task_df)
    print("#######################################################")


    print("#######################################################")
    print("context DF:")
    print(context_df)
    print("#######################################################")

    output = workflow_hub(agent_df, relations_df, task_df, context_df)
    return Response({"OUTPUT: ", output})




@api_view(['POST'])
def save_crewgraph(request):
    nodes = request.data.get('nodes', [])
    edges = request.data.get('fixedEdges', [])
    

    #IMPLEMENT: ABILITY TO SAVE CREWS, FIGURE OUT WHETHER TO KEEP AGENTS IN CREW CONTAINER, OR ALLOW FOR AGENT REUSE

    Agent.objects.all().delete()
    Edge.objects.all().delete()
    ContextBin.objects.all().delete()
    Task.objects.all().delete()
    print("###################################")
    print("NOPDESS:::: ", nodes[1])
    print("###################################")

    for node in nodes:
        data = node.get('data', {})
        
        type = data.get('Type')

        if (type == 'agent'):
            agent = Agent(
                name = data.get('Name'),
                agent_type = data.get('agent_type'),
                role = data.get('role'),
                goal = data.get('goal'),
                backstory = data.get('backstory'),
                
            )
            agent.save()

        
        elif (type =='context'):
            context = ContextBin(
                name = data.get('Name'),
                links = data.get('links')
            )
            
            context.save()
        elif (type == 'task'):
            print("TYPE RECEIVED")
            task = Task(
                name = data.get('Name'),
                description = data.get('description'),
                task_time = data.get('task_time'),
                input_format = data.get('input_format'),
                output_format = data.get('output_format'),
            )
            print("TYPE CREATED")
            task.save()
            print("TYPE SAVED")

    for edge in edges:
        print("+________________")
        print("EDGE: ", edge)
        print("________________")
        source_name = edge.get('source')
        target_name = edge.get('target') 
        relation_type = edge.get('relation_type')
        if (relation_type == 'context -> agent'):
            edge = Edge(
                source = ContextBin.objects.get(name = source_name),
                target = Agent.objects.get(name=target_name),
                
                relation_type = relation_type,
            )
            edge.save()
            print("###################################")
            print("EDGE:",edge.source)
            print("###################################")
        elif (relation_type == 'agent -> task'):
            print("AGENT TO TASK")
            edge = Edge(
                source = Agent.objects.get(name=source_name),
                target = Task.objects.get(name=target_name),
                relation_type = relation_type,
            )
            edge.save()
        elif (relation_type == 'task -> task'):
            edge = Edge(
                source = Task.objects.get(name=source_name),
                target = Task.objects.get(name=target_name),
                relation_type = relation_type,
            )
            edge.save()

        elif (relation_type == 'context -> task'):
            edge = Edge(
                source = ContextBin.objects.get(name=source_name),
                target = Task.objects.get(name=target_name),
                relation_type = relation_type,
            )
            edge.save()
    return Response({"Crew graph created"})



@api_view(['POST'])
def getAgentData(request):
    name = request.data.get('name')
    role = request.data.get('role')
    agent_type = request.data.get('agent_type')


   
    
    agent = Agent(
        name = name, 
        role = role, 
    )

    agent.save()

    return Response({"Agent created"})

def crew_output(crew):
    crews = Crew.objects.all().values('id', 'name')
    return JsonResponse(list(crews), safe=False)


@api_view(['POST'])
def run_crew(request):
    try: 
        crew_id = request.data.get('crew_id')
        crew = Crew.objects.get(id=crew_id)

        return crew_output(crew)

    except Crew.DoesNotExist:
        return JsonResponse({'error:' 'Crew not found'}, status = 404)
 
class AgentView(viewsets.ModelViewSet):
    serializer_class = AgentSerializer
    queryset = Agent.objects.all()

class ContextBinView(viewsets.ModelViewSet):
    serializer_class = ContextBinSerializer
    queryset = ContextBin.objects.all()


class EdgeView(viewsets.ModelViewSet):
    serializer_class = EdgeSerializer
    queryset = Edge.objects.all()

class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()




class CrewView(viewsets.ModelViewSet):
    serializer_class = CrewSerializer
    queryset = Crew.objects.all()