from rest_framework import viewsets, status
from .serializers import AgentSerializer, ReportSerializer, PaperSerializer, TeamLeadSerializer
from .models import Agent, Report, Paper, TeamLead
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import os
from django.http import HttpResponse, JsonResponse
from langchain_huggingface import HuggingFaceEmbeddings
from django.db import transaction
from chatbot_functionality.KnowledgeBase import KnowledgeBase
from chatbot_functionality.Agent import ollama_engine

from datetime import datetime



# Create your views here.
class AgentView(viewsets.ModelViewSet):
    lookup_field = 'name'
    serializer_class = AgentSerializer
    queryset = Agent.objects.all()
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.stored_papers.clear()
        instance.delete()
        return Response({"message": "Agent successfully deleted"}, status = status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            #create all papers objects
            name= request.data.get('name')
            if Agent.objects.filter(name=name).exists():
                return Response({"error": "Agent name already exists."}, status = status.HTTP_400_BAD_REQUEST)
            #IMPORTANT: check that name not taken
            role = request.data.get('role')
            expertise = request.data.get('expertise')
            files = request.FILES.getlist('files')
            selFiles = request.POST.getlist('selFiles')
            
            
            #print(request.data)
            papers = []
            for file in files:
                print(type(file))
                paper = Paper(file = file, name = file.name)
                #checking if same name paper alr exists

                if (Paper.objects.filter(name= file.name).exists()):
                    print("FILE ALR EXISTS")
                    return JsonResponse({"error": "File already exists."}, status=400)

                paper.save()
                papers.append(paper)

            print("Papers created")
            
            #papers created
            #Now, create a knowledge base instance in root
            knowledge_path = f"./agent_knowledge_bases/{name}"
            
            agent_knowledge = KnowledgeBase(knowledge_path, embedder=HuggingFaceEmbeddings(), engine = ollama_engine('mistral'))
            print("Knowledge base creation")
            agent = Agent(
                name = name,
                role = role,
                expertise = expertise,
                knowledge = knowledge_path
                
            )
            print("Agent init")
            agent.save()
            agent = Agent.objects.get(name=agent.name)


            #connect keys of papers in selFiles to agent obj

            for paper_name in selFiles:
                paper_ref = Paper.objects.get(name=paper_name) 
                print("Paper ref:", paper_ref)
                agent.stored_papers.add(paper_ref)
            
            for paper in papers:
                agent_exists = Agent.objects.filter(name=agent.name).exists()
                print(f"Agent exists in DB: {agent_exists} (Agent ID: {agent.id})")

                # Confirm that the paper exists in the database
                paper_exists = Paper.objects.filter(id=paper.id).exists()
                print(f"Paper exists in DB: {paper_exists} (Paper ID: {paper.id})")
                agent.stored_papers.add(paper)

            
            print("Papers added as key")
            return Response("Agents/papers created")




class PaperView(viewsets.ModelViewSet):
    parser_class = (MultiPartParser)
    serializer_class = PaperSerializer
    queryset = Paper.objects.all()
    def create( self, request, *args, **kwargs):
        file = request.FILES.get('files')
        name = file.name
        paper = Paper(
            file = file,
            name = name
        )
        paper.save()
        return Response("Paper created")
    
    
        

class TeamLeadView(viewsets.ModelViewSet):
    lookup_field = 'name'
    serializer_class = TeamLeadSerializer
    queryset = TeamLead.objects.all()
    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        description = request.data.get('description')
        
        if TeamLead.objects.filter(name=name).exists():
            return Response({"error": "Lead name already exists."}, status = status.HTTP_400_BAD_REQUEST)
        else:
            lead = TeamLead(
                name = name,
                description = description,
            )
        

        lead.save()
        return Response({"Lead created"})


class ReportView(viewsets.ModelViewSet):
    lookup_field = 'name'
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            name = request.data.get('name')
            task = request.data.get('task')
            description = request.data.get('description')
            expectations = request.data.get('expectations')
            model = request.data.get('model')
            cycles = request.data.get('cycles')
            reportGuidelines = request.data.get('reportGuidelines')
            method = request.data.get('method')
            temperature = request.data.get('temperature')
            engine = request.data.get('engine')
            lead = request.data.get('lead')
            files = request.FILES.getlist('files')
            selFiles = request.POST.getlist('selFiles')

            if Report.objects.filter(name=name).exists():
                return Response({"error": "report name already exists."}, status = status.HTTP_400_BAD_REQUEST)

            papers = []
            for file in files:
                paper = Paper(file = file, name = file.name)

                if (Paper.objects.filter(name= file.name).exists()):
                    print("FILE ALR EXISTS")
                    return JsonResponse({"error": "Paper file already exists."}, status=400)

                paper.save()
                papers.append(paper)

            print("Papers created")
            
            report = Report(
                name = name,
                task = task,
                description = description,
                expectations = expectations,
                model = model,
                cycles = cycles,
                reportGuidelines = reportGuidelines,
                method = method,
                temperature = temperature,
                engine = engine,
                lead = lead,
                
            )
            print("Report init")
            report.save()
            report = report.objects.get(name=report.name)


            #connect keys of papers in selFiles to report obj

            for paper_name in selFiles:
                paper_ref = Paper.objects.get(name=paper_name) 
                print("Paper ref:", paper_ref)
                report.context.add(paper_ref)
            
            for paper in papers:
                report.context.add(paper)

            #Time to actually run the code to create a report!
                
            
            
            print("Papers added as key")
            return Response("Report generated/papers created")



        


