from rest_framework import viewsets, status
from .serializers import AgentSerializer, ReportSerializer, PaperSerializer, TeamLeadSerializer, UserLoginSerializer, UserRegistrationSerializer, CustomUserSerializer 
from .models import Agent, Report, Paper, TeamLead
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
import os
import json
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from langchain_text_splitters import RecursiveCharacterTextSplitter
from django.core.files.base import ContentFile
from django.db import transaction
from core.chatbot_functionality.KnowledgeBase import KnowledgeBase
from core.chatbot_functionality.run_meeting import run_meeting
from datetime import datetime
import shutil
from django.forms.models import model_to_dict
from pdfminer.high_level import extract_text

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
class UserInfoAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user
class UserLogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user =serializer.validated_data
        serializer = CustomUserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token),
                          "access": str(token.access_token)}
        return Response(data, status = status.HTTP_200_OK)

class userRegistrationAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh":str(token),
                          "access": str(token.access_token)
                          }
        return Response(data, status=status.HTTP_201_CREATED)
class AgentView(viewsets.ModelViewSet):
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Agent.objects.filter(user=user)
    
    
    
    
    #overrides retrieve s.t it only retrieves if name and user matches
    def list(self, request, *args, **kwargs):
        """Retrieve all agents for the authenticated user, or filter by name."""
        user = request.user
        lead_name = request.query_params.get("name", None)

        queryset = Agent.objects.filter(user=user)
        if lead_name:
            queryset = queryset.filter(name=lead_name)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific lead for the authenticated user."""
        user = request.user
        agent_name = kwargs.get("pk")
        
        try:
            lead = Agent.objects.get(user=user, name=agent_name)
        except Agent.DoesNotExist:
            return Response({"error": "Agent not found for this user."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(lead)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            user = request.user
            agent_name = kwargs.get('pk')
            
            try:
                agent = Agent.objects.get(user=user, name=agent_name)
            except Agent.DoesNotExist:
                return Response({"error": "Agent not found for this user."}, status=status.HTTP_404_NOT_FOUND)

            agent.stored_papers.clear()
            path = os.path.join(settings.BASE_DIR, f"{user.username}_knowledge_bases", f'agent', f"{agent.name}")
            print("Destroy path:", path)
            shutil.rmtree(path)
            agent.delete()
            return Response({"message": "Agent successfully deleted"}, status = status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            #create all papers objects
            user = request.user
            username = request.user.username
            name= request.data.get('name')
            print("user is", user)
            print("agent name", name)
            if Agent.objects.filter(name=name, user=user).exists():
                return Response({"error": "Agent name already exists for this user."}, status = status.HTTP_400_BAD_REQUEST)
            #IMPORTANT: check that name not taken
            role = request.data.get('role')
            expertise = request.data.get('expertise')
            files = request.FILES.getlist('files')
            selFiles = request.POST.getlist('selFiles')
            
            #Now, create a knowledge base instance in root
            knowledge_path = f"{username}_knowledge_bases/agent/{name}"
            print("Creating agent knowledge base at ", knowledge_path)
            agent_knowledge = KnowledgeBase(knowledge_path, embedder_name="HuggingFaceEmbeddings")
            #Add papers to knowledge base

            #print(request.data)
            papers = []
            
            for file in files:
                file_type = os.path.splitext(file.name)[1]
                
                file_type = file_type.lstrip(".")
                print("FILE TYPE:", file_type)
                if ("txt" not in file_type and "pdf" not in file_type):
                    print("no text/pdf")
                    return JsonResponse({"error": "File is not pdf/text. Is of type {file_type}"}, status=400)
                paper = Paper(file = file, name = file.name, file_type = file_type, user=user)
                #checking if same name paper alr exists

                if (Paper.objects.filter(name= file.name, user=user).exists()):
                    return JsonResponse({"error": "File already exists for this user."}, status=400)
                
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
                knowledge = knowledge_path,
                user = user
                
            )
            agent.save()
            agent = Agent.objects.get(name=agent.name, user = user)

            chunker = RecursiveCharacterTextSplitter(
                                chunk_size=200,
                                chunk_overlap=20,
                                length_function=len,
                                is_separator_regex=False,
                            )
            #connect keys of papers in selFiles to agent obj

            for paper_name in selFiles:
                paper_ref = Paper.objects.get(name=paper_name, user = user) 
                agent.stored_papers.add(paper_ref)
                #Embed papers
                #parse text
                file_content = ""
                file_path = paper_ref.file.path
                #This is where you handle parsing the file text, depending on the format
                if paper_ref.file_type == "txt":
                    with open(file_path, 'r') as file:
                        file_content = file.read()

                if paper_ref.file_type == "pdf":
                    file_content = extract_text(file_path)
                print("file content: ", file_content)
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
                        
                if paper.file_type == "pdf":
                    file_content = extract_text(file_path)
                print("Text to be embedded:", file_content)
                paper_name = paper.name
                file_content = [file_content]
                agent_knowledge.upload_knowledge_1(text= file_content, source_name= paper_name, chunker = chunker)

            
            print("Papers added as key")
            return Response("Agents/papers created")




class PaperView(viewsets.ModelViewSet):
    parser_class = (MultiPartParser)
    serializer_class = PaperSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Paper.objects.filter(user=user)
    
    
    
    
    #get for multiple: ie, all papers
    def list(self, request, *args, **kwargs):
        """Retrieve all papers for the authenticated user, or filter by name."""
        user = request.user
        paper_name = request.query_params.get("name", None)

        queryset = Paper.objects.filter(user=user)
        if paper_name:
            queryset = queryset.filter(name=paper_name)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            user = request.user
            username = request.user.username
            file = request.FILES.get('file')
            name = file.name
            file_type = os.path.splitext(name)[1]
            file_type = file_type.lstrip(".")
            print(file_type)
            if ("txt" not in file_type and "pdf" not in file_type):
                    print("no text/pdf")
                    return JsonResponse({"error": "File is not pdf/text. Is of type {file_type}"}, status=400)
            paper = Paper(
                file = file,
                file_type = file_type,
                name = name,
                user = user
            )
            paper.save()
            return Response("Paper created")
        
    #for getting one paper: ie, individual paper page
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific paper for the authenticated user."""
        user = request.user
        paper_id = kwargs.get("pk")
        
        try:
            paper = Paper.objects.get(user=user, id=paper_id)
        except Paper.DoesNotExist:
            return Response({"error": "paper not found for this user."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(paper)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            user = request.user
            paper_id = kwargs.get("pk")
            try:
                paper = Paper.objects.get(user=user, id=paper_id)
            except Paper.DoesNotExist:
                return Response({"error": "Paper not found for this user."}, status=status.HTTP_404_NOT_FOUND)

            path = os.path.join(settings.MEDIA_ROOT, user.username, f"papers", paper.name)
            print("Destroy path:", path)
            os.remove(path)
            paper.delete()
            return Response({"message": "Paper successfully deleted"}, status = status.HTTP_204_NO_CONTENT)
            
        
    
        

class TeamLeadView(viewsets.ModelViewSet):
    serializer_class = TeamLeadSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return TeamLead.objects.filter(user=user)
    
    def list(self, request, *args, **kwargs):
        """Retrieve all papers for the authenticated user, or filter by name."""
        user = request.user
        lead_name = request.query_params.get("name", None)

        queryset = TeamLead.objects.filter(user=user)
        if lead_name:
            queryset = queryset.filter(name=lead_name)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific lead for the authenticated user."""
        user = request.user
        lead_name = kwargs.get("pk")
        
        try:
            lead = TeamLead.objects.get(user=user, name=lead_name)
        except TeamLead.DoesNotExist:
            return Response({"error": "Lead not found for this user."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(lead)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            user = request.user
            lead_name = kwargs.get("pk")
            try:
                lead = TeamLead.objects.get(user=user, name=lead_name)
            except TeamLead.DoesNotExist:
                return Response({"error": "Lead not found for this user."}, status=status.HTTP_404_NOT_FOUND)

            path = os.path.join(settings.BASE_DIR, f"{user.username}_knowledge_bases", 'leads', lead.name)
            print("Destroy path:", path)
            shutil.rmtree(path)
            lead.delete()
            return Response({"message": "lead successfully deleted"}, status = status.HTTP_204_NO_CONTENT)
        
        
    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            name = request.data.get('name')
            description = request.data.get('description')
            user = request.user
            username = request.user.username
            
            if TeamLead.objects.filter(name=name, user=user).exists():
                return Response({"error": "Lead name already exists for this user."}, status = status.HTTP_400_BAD_REQUEST)
            else:
                
                knowledge_path = f"{username}_knowledge_bases/leads/{name}"
                lead_knowledge = KnowledgeBase(knowledge_path, embedder_name="HuggingFaceEmbeddings")
                print("Knowledge base creation")
                lead = TeamLead(
                    kb_path = knowledge_path,
                    name = name,
                    description = description,
                    user = user,
                )
            

            lead.save()
            return Response({"Lead created"})
        
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(["POST"])
def save_report_memory(request, name):
    if request.method == 'POST':
        report_inst = Report.objects.get(name=name, user = request.user)
        report_text = ""
        with open(report_inst.output.path, 'r') as file:
            report_text = file.read()
            print("Report text:", report_text)
        report_inst.saved_to_lead = True
        report_inst.save()
        lead = report_inst.lead
        lead_kb_path = lead.kb_path
        lead_kb = KnowledgeBase.from_path(lead_kb_path)

        chunker = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False,
        )
        report_text = [report_text]
        lead_kb.upload_knowledge_1(text= report_text, source_name= report_inst.name, chunker = chunker)
        return JsonResponse({'message': f'report saved in lead kb'})


class ReportView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportSerializer
    def get_queryset(self):
        user = self.request.user
        return Report.objects.filter(user=user)
    
    
    
    def list(self, request, *args, **kwargs):
        """Retrieve all reports for the authenticated user, or filter by name."""
        user = request.user
        report_name = request.query_params.get("name", None)

        queryset = Report.objects.filter(user=user)
        if report_name:
            queryset = queryset.filter(name=report_name)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific report for the authenticated user."""
        user = request.user
        report_name = kwargs.get("pk")
        
        try:
            report = Report.objects.get(user=user, name=report_name)
        except Report.DoesNotExist:
            return Response({"error": "Report not found for this user."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            user = request.user
            report_name = kwargs.get("pk")
            try:
                report = Report.objects.get(user=user, name=report_name)
            except Report.DoesNotExist:
                return Response({"error": "Report not found for this user."}, status=status.HTTP_404_NOT_FOUND)

            report_path = os.path.join(settings.MEDIA_ROOT, user.username, "output", "report_" + report.name + ".txt")
            chat_path = os.path.join(settings.MEDIA_ROOT, user.username, "report_logs", "chatlog_" + report.name + ".txt")
            os.remove(report_path)
            os.remove(chat_path)
            report.delete()
            return Response({"message": "Report successfully deleted"}, status = status.HTTP_204_NO_CONTENT)
            
        
    def create(self, request, *args, **kwargs):
        print("endpoint accessed")
        with transaction.atomic():
            name = request.data.get('name')
            user = request.user
            username = request.user.username
            #checks for duplicate names
            if Report.objects.filter(name=name, user = user).exists():
                return Response({"error": "report name already exists."}, status = status.HTTP_400_BAD_REQUEST)
            
            date = datetime.now()
            task = request.data.get('task')
            expectations = request.data.get('expectations')
            model = request.data.get('model')
            cycles = int(request.data.get('cycles'))
            reportGuidelines = request.data.get('reportGuidelines')
            method = int(request.data.get('method'))
            temperature = float(request.data.get('temperature'))
            engine = request.data.get('engine')
            lead_name = request.data.get('lead')
            lead_obj = TeamLead.objects.get(name=lead_name, user =user)
            files = request.FILES.getlist('context_files')
            selFiles = request.POST.getlist('selFiles')
            selAgents = request.POST.getlist('selAgents')
            draw_from_knowledge = False
            

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
                user = user,
                saved_to_lead = False
                
            )
            params = {"name": name, 
                      "date": date, 
                      "task": task, 
                      "expectations": expectations,
                      "model": model, 
                      "cycles": cycles,
                      "report_guidelines": reportGuidelines,
                      "method": method,
                      "temperature": temperature,
                      "engine": engine,
                      "lead_path": lead_obj.kb_path,
                      "draw_from_knowledge": draw_from_knowledge,
                      "user": username
                      }
            report.save()
            report = Report.objects.get(name=report.name, user = user)
            #selAgents setting
            potential_agents = []
            if selAgents[0] == "all":
                all_agents = Agent.objects.filter(user=user)
                report.potential_agents.add(*all_agents)
                potential_agents = list(Agent.objects.filter(user=user).values())
            else:
                for agent_name in selAgents:
                    agent_ref = Agent.objects.get(name=agent_name, user = user) 
                    report.potential_agents.add(agent_ref)
                    potential_agents.append(model_to_dict(agent_ref))
            params["potential_agents"] = potential_agents
            
            papers = []
            paper_names = []
            for file in files:
                print(file)
                if ("txt" or "pdf" not in file.content_type):
                    print("why failing?")
                    return JsonResponse({"error": "File not a text file"}, status=400) 
                file_type = os.path.splitext(file.name)[1]
                file_type = file_type.lstrip(".")
                paper = Paper(file = file, name = file.name, file_type = file_type, user = user)
                if (Paper.objects.filter(name= file.name, user = user).exists()):
                    print("FILE ALR EXISTS")
                    return JsonResponse({"error": "Paper file already exists."}, status=400)
                print("c3")
                paper.save()
                papers.append(paper)
                print("c4")
                

            print("Papers created")
            

            #connect keys of papers in selFiles to report obj

            for paper_name in selFiles:
                paper_ref = Paper.objects.get(name=paper_name, user = user) 
                print("Paper ref:", paper_ref)
                report.context.add(paper_ref)
                paper_names.append(paper_name)
            
            for paper in papers:
                report.context.add(paper)
                paper_names.append(paper.name)

            params["context"] = paper_names
            #Time to actually run the code to create a report!
            #Get the context papers
            try:
                def stream():
                    
                    print("starting to stream")
                    report_output = None
                    try:
                        for update in run_meeting(params):
                            if report_output is not None:
                                yield report_output
                            report_output = update
                    
                     
                        report_text = report_output["final_report"]
                        chat_log = report_output["chat_log"]
                        worker_team = report_output["worker_team"]
                        report_name = f"report_{report.name}.txt"
                        chatlog_name = f"chatlog_{report.name}.txt"
                        report.output.save(report_name, ContentFile(report_text))
                        report.chat_log.save(chatlog_name, ContentFile(chat_log))
                        #map agents to the report
                        for i in worker_team:
                            agent_ref = Agent.objects.get(name=i, user = user)
                            report.chosen_team.add(agent_ref)
                        
                        yield json.dumps("END") + '\n'
                    except Exception as e:
                        error_response = {
                            "status": "error",
                            "message": str(e)
                        }
                        yield json.dumps(error_response) + '\n'
                        

            

                response = StreamingHttpResponse(stream(), content_type="application/json")
                response['Cache-Control'] = 'no-cache'
                return response



            except Exception as e:
                report.delete()
                return JsonResponse({"error": e}, status=400) 



        


