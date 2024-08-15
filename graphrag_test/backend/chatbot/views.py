from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import AgentSerializer, CrewSerializer, EdgeSerializer
from rest_framework.decorators import api_view
from .models import Agent, Crew, Edge

# Create your views here.

@api_view(['POST'])
def save_crewgraph(request):
    nodes = request.data.get('nodes', [])
    edges = request.data.get('fixedEdges', [])
    

    #IMPLEMENT: ABILITY TO SAVE CREWS, FIGURE OUT WHETHER TO KEEP AGENTS IN CREW CONTAINER, OR ALLOW FOR AGENT REUSE

    Agent.objects.all().delete()
    Edge.objects.all().delete()

    for node in nodes:
        data = node.get('data', {})
        
        agent = Agent(
            name = data.get('Name'),
            
            role = data.get('Role'),
            goal = data.get('Goal'),
            backstory = data.get('Backstory'),
            input_format = data.get('input_format'),
            output_format = data.get('output_format'),
        )
        agent.save()

    for edge in edges:
        print("+________________")
        print("EDGE: ", edge)
        print("________________")
        source_name = edge.get('source')
        target_name = edge.get('target') 
        edge = Edge(
            source = Agent.objects.get(name=source_name),
            target = Agent.objects.get(name=target_name),
        )
        edge.save()
    return Response({"Crew graph created"})



@api_view(['POST'])
def getAgentData(request):
    name = request.data.get('name')
    role = request.data.get('role')
    input_format = request.data.get('input_format')
    output_format = request.data.get('output_format')


    if not all([name, role, input_format, output_format]):
        return Response({"error": "AJKDSLJFIOJKLJIOAF fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    
    agent = Agent(
        name = name, 
        role = role, 
        input_format = input_format,
        output_format = output_format,
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

class EdgeView(viewsets.ModelViewSet):
    serializer_class = EdgeSerializer
    queryset = Edge.objects.all()


class CrewView(viewsets.ModelViewSet):
    serializer_class = CrewSerializer
    queryset = Crew.objects.all()