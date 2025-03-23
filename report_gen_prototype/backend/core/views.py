from rest_framework import viewsets, status
from .serializers import AgentSerializer, ReportSerializer, PaperSerializer, TeamLeadSerializer
from .models import Agent, Report, Paper, TeamLead
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import os
from django.http import HttpResponse, JsonResponse
from langchain_text_splitters import RecursiveCharacterTextSplitter
from django.core.files.base import ContentFile

from langchain_huggingface import HuggingFaceEmbeddings
from django.db import transaction
from core.chatbot_functionality.KnowledgeBase import KnowledgeBase
from core.chatbot_functionality.constants import recursive_chunker
from core.chatbot_functionality.Agent import ollama_engine
from core.chatbot_functionality.run_meeting import run_meeting
from datetime import datetime
import shutil

from django.conf import settings



# Create your views here.
class AgentView(viewsets.ModelViewSet):
    lookup_field = 'name'
    serializer_class = AgentSerializer
    queryset = Agent.objects.all()
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.stored_papers.clear()
        path = os.path.join(settings.BASE_DIR, 'agent_knowledge_bases', instance.name)
        print("Destroy path:", path)
        shutil.rmtree(path)
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
            
            #Now, create a knowledge base instance in root
            knowledge_path = f"./agent_knowledge_bases/{name}"
            agent_knowledge = KnowledgeBase(knowledge_path, embedder_name="HuggingFaceEmbeddings")
            #Add papers to knowledge base

            #print(request.data)
            papers = []
            
            for file in files:
                
                file_type = os.path.splitext(file.name)[1]
                file_type = file_type.lstrip(".")
                paper = Paper(file = file, name = file.name, file_type = file_type)
                #checking if same name paper alr exists

                if (Paper.objects.filter(name= file.name).exists()):
                    print("FILE ALR EXISTS")
                    return JsonResponse({"error": "File already exists."}, status=400)
                
                paper.save()
                papers.append(paper)

            print("Papers created")
            
            #papers created
            
            
            print("Knowledge base creation")
            agent = Agent(
                name = name,
                role = role,
                kb_path = knowledge_path,
                expertise = expertise,
                knowledge = knowledge_path
                
            )
            print("Agent init")
            agent.save()
            agent = Agent.objects.get(name=agent.name)

            chunker = RecursiveCharacterTextSplitter(
                                chunk_size=200,
                                chunk_overlap=20,
                                length_function=len,
                                is_separator_regex=False,
                            )
            #connect keys of papers in selFiles to agent obj

            for paper_name in selFiles:
                paper_ref = Paper.objects.get(name=paper_name) 
                agent.stored_papers.add(paper_ref)
                #Embed papers
                #parse text
                file_content = ""
                file_path = paper_ref.file.path
                #This is where you handle parsing the file text, depending on the format
                if paper_ref.file_type == "txt":
                    with open(file_path, 'r') as file:
                        file_content = file.read()

                #chunkers expect a list, not enclosing text in list yields 1 char chunks
                file_content = [file_content]
                agent_knowledge.upload_knowledge_1(text= file_content, source_name= paper_name, chunker = chunker)
            
            for paper in papers:
                agent.stored_papers.add(paper)
                #embed papers and parse text
                
                file_content = ""
                file_path = paper.file.path
                if paper.file_type == "txt":
                    with open(file_path, 'r') as file:
                        file_content = file.read()
                print("Text to be embedded:", file_content)
                paper_name = paper.name
                file_content = [file_content]
                agent_knowledge.upload_knowledge_1(text= file_content, source_name= paper_name, chunker = chunker)

            
            print("Papers added as key")
            return Response("Agents/papers created")




class PaperView(viewsets.ModelViewSet):
    lookup_field = "id"
    parser_class = (MultiPartParser)
    serializer_class = PaperSerializer
    queryset = Paper.objects.all()
    def create( self, request, *args, **kwargs):
        with transaction.atomic():
            file = request.FILES.get('file')
            name = file.name
            file_type = os.path.splitext(name)[1]
            file_type = file_type.lstrip(".")
            print(file_type)
            paper = Paper(
                file = file,
                file_type = file_type,
                name = name
            )
            paper.save()
            return Response("Paper created")
    
    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            instance = self.get_object()
            path = os.path.join(settings.MEDIA_ROOT, "papers", instance.name)
            print("Destroy path:", path)
            os.remove(path)
            instance.delete()
            return Response({"message": "Paper successfully deleted"}, status = status.HTTP_204_NO_CONTENT)
            
        
    
        

class TeamLeadView(viewsets.ModelViewSet):
    lookup_field = 'name'
    serializer_class = TeamLeadSerializer
    queryset = TeamLead.objects.all()
    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            instance = self.get_object()
            path = os.path.join(settings.BASE_DIR, 'leads_knowledge_bases', instance.name)
            print("Destroy path:", path)
            shutil.rmtree("your_directory")
            instance.delete()
            return Response({"message": "Paper successfully deleted"}, status = status.HTTP_204_NO_CONTENT)
        
        
    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            name = request.data.get('name')
            description = request.data.get('description')
            
            if TeamLead.objects.filter(name=name).exists():
                return Response({"error": "Lead name already exists."}, status = status.HTTP_400_BAD_REQUEST)
            else:
                knowledge_path = f"./leads_knowledge_bases/{name}"
                lead_knowledge = KnowledgeBase(knowledge_path, embedder_name="HuggingFaceEmbeddings")
                print("Knowledge base creation")
                lead = TeamLead(
                    kb_path = knowledge_path,
                    name = name,
                    description = description,
                )
            

            lead.save()
            return Response({"Lead created"})

def generate_report(request):
    res = run_meeting("test_pot_again4")
    print(res)
    return JsonResponse({"status": "success", "data": res})
#saves the report in "output" to the lead
def save_report_memory(request, name):
    report_inst = Report.objects.filter(name=name)
    report_text = ""
    with open(report_inst.output, 'r') as file:
        report_text = file.read()
    report_inst.output
    lead = report_inst.lead
    lead_kb_path = lead.kb_path
    lead_kb = KnowledgeBase.from_path(lead_kb_path)

    chunker = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )

    lead_kb.upload_knowledge_1(text= report_text, source_name= report_inst.name, chunker = chunker)
    return JsonResponse({'message': f'report saved in lead kb'})
    #Thought process…
    #If the report is deleted, leads wont show it
    #Save the report in the django db for the lead

class ReportView(viewsets.ModelViewSet):
    lookup_field = 'name'
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    """def update(self, request, *args, **kwargs):
        instance = self.get_object()
        with transaction.atomic():
            #First, handle updating the file obj(because serializer by default wont handle properly)
            if 'output' in request.FILES:
                if instance.output:
                    instance.output.delete(save=False)#Delete old file
                instance.output = request.FILES['output']#insert new file into output field of report
            
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data, status=status.HTTP_200_OK)
        """
    
    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            instance = self.get_object()
            report_path = os.path.join(settings.MEDIA_ROOT, "reports", "report_" + instance.name)
            chat_path = os.path.join(settings.MEDIA_ROOT, "reports", "chatlog_" + instance.name)
            os.remove(report_path)
            os.remove(chat_path)
            instance.delete()
            return Response({"message": "Report successfully deleted"}, status = status.HTTP_204_NO_CONTENT)
            
        

    def create(self, request, *args, **kwargs):
        #with transaction.atomic():
            name = request.data.get('name')
            #checks for duplicate names
            if Report.objects.filter(name=name).exists():
                return Response({"error": "report name already exists."}, status = status.HTTP_400_BAD_REQUEST)
            
            date = datetime.now()
            task = request.data.get('task')
            expectations = request.data.get('expectations')
            model = request.data.get('model')
            cycles = request.data.get('cycles')
            reportGuidelines = request.data.get('reportGuidelines')
            method = int(request.data.get('method'))
            temperature = float(request.data.get('temperature'))
            engine = request.data.get('engine')
            lead_name = request.data.get('lead')
            lead_obj = TeamLead.objects.get(name=lead_name)
            files = request.FILES.getlist('context_files')
            selFiles = request.POST.getlist('selFiles')
            selAgents = request.POST.getlist('selAgents')
            report = Report(
                name = name,
                date = date,
                task = task,
                expectations = expectations,
                model = model,
                cycles = cycles,
                report_guidelines = reportGuidelines,
                method = method,
                temperature = temperature,
                engine = engine,
                lead = lead_obj,
                
            )
            report.save()
            report = Report.objects.get(name=report.name)
            #selAgents setting
            if selAgents[0] == "all":
                all_agents = Agent.objects.all()
                report.potential_agents.add(*all_agents)
            else:
                for agent_name in selAgents:
                    agent_ref = Agent.objects.get(name=agent_name) 
                    report.potential_agents.add(agent_ref)
            
            
            papers = []
            print("savig report papers")
            for file in files:
                if ("text" or "pdf" not in file.content_type):
                    return JsonResponse({"error": "File not a text file"}, status=400) 
                
                file_type = os.path.splitext(file.name)[1]
                file_type = file_type.lstrip(".")
                paper = Paper(file = file, name = file.name, file_type = file_type)
                
                if (Paper.objects.filter(name= file.name).exists()):
                    print("FILE ALR EXISTS")
                    return JsonResponse({"error": "Paper file already exists."}, status=400)

                paper.save()
                papers.append(paper)

            print("Papers created")


            #connect keys of papers in selFiles to report obj

            for paper_name in selFiles:
                paper_ref = Paper.objects.get(name=paper_name) 
                print("Paper ref:", paper_ref)
                report.context.add(paper_ref)
            
            for paper in papers:
                report.context.add(paper)

            #Time to actually run the code to create a report!
            #Get the context papers
            try:
                report_output = run_meeting(id = report.name)
                print("meeting ran through")
                report_text = report_output["final_report"]
                chat_log = report_output["chat_log"]
                worker_team = report_output["worker_team"]
                report_name = f"report_{report.name}.txt"
                chatlog_name = f"chatlog_{report.name}.txt"
                report.output.save(report_name, ContentFile(report_text))
                report.chat_log.save(chatlog_name, ContentFile(chat_log))
                print("files saved")
                #map agents to the report
                #UNCOMMENT AFTER TESTING
                print("assigned fields")
                for i in worker_team:
                    agent_ref = Agent.objects.get(name=i)
                    report.chosen_team.add(agent_ref)
                
        
                serializer = ReportSerializer(report, context={"request": request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            except AssertionError:
                print("assertion error")
                return JsonResponse({"error": "Engine generated a conversation with agent not in django db"}, status=400) 



        


