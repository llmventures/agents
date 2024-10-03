from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import ConversationLogSerializer, StoredPapersSerializer
from rest_framework.decorators import api_view
from .models import ConversationLog, StoredPapers
from datetime import datetime


# Create your views here.

class ConversationLogView(viewsets.ModelViewSet):
    serializer_class = ConversationLogSerializer
    queryset = ConversationLog.objects.all()


class StoredPapersView(viewsets.ModelViewSet):
    serializer_class = StoredPapersSerializer
    queryset = StoredPapers.objects.all()

#DAILY RUN OPERATION:
    
#web_scrape gets 3 papers from biorxiv. Adding them to the knowledge base. Also 
#add their info the the backend db.
#run_convo adds 3 new conversation logs to chat_logs folder. Also add their info
#to the backend db

#Update backend db:

@api_view(['GET'])
def getMostRecentConvoLog(request):
    latest_log = ConversationLog.objects.latest('date')
    data = {
        'date': latest_log.date.strftime("%Y-%m-%d %H:%M:%S"),
        'title': latest_log.title,
        'agents': latest_log.agents,
        'topic_text': latest_log.topic_text,
        'topic_id': latest_log.topic_id,
        'log_text': latest_log.log_text,
        'engine': latest_log.engine,
    }
    return JsonResponse(data)
@api_view(['GET'])
def getSpecificLogFromDate(request, date):
    try:
        print("DATE IS: ", date)
        datetime_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        log = ConversationLog.objects.get(date= datetime_date)
        return JsonResponse({
            'date': date,
            'title': log.title,
            'agents': log.agents,
            'topic_text': log.topic_text,
            'topic_id': log.topic_id,
            'log_text': log.log_text,
            'engine': log.engine,
        })
    except ConversationLog.DoesNotExist:
        return JsonResponse({'error': "item not found"}, status = 404)


@api_view(['GET'])
def getStoredPapers(request):
    papers = StoredPapers.objects.all().values('title', 'doi')
    
    return JsonResponse(list(papers), safe= False)


@api_view(['GET'])
#DOI needs to be with - instead of slash to avoid errors with url pathing
def getPaperFromDOI(request, doi):
    try:
        print("DOI IS:", doi)
        mod_doi = doi.replace('-','/')
        paper = StoredPapers.objects.get(doi = mod_doi)
        return JsonResponse({
            'doi' : paper.doi,
            'title' : paper.title,
            'authors' : paper.authors,
            'date': paper.date,
            'date_accessed' : paper.date_accessed,
        })
    except StoredPapers.DoesNotExist:
        return JsonResponse({'error': "item not found"}, status = 404)

@api_view(['GET'])
def getAllConvoLogs(request):
    logs = ConversationLog.objects.all().values('date', 'topic_id')
    formatted_logs = [
        {
            'date': log['date'].strftime('%Y-%m-%d %H:%M:%S'),  # Change this format as needed
            'topic_id': log['topic_id']
        } 
        for log in logs
    ]
    return JsonResponse(list(formatted_logs), safe= False)
@api_view(['POST'])
def addConvoLog(request):
    nodeInfo = request.data
    date = datetime.strptime(nodeInfo['Date'], "%Y-%m-%d %H:%M:%S")
    newConvoLogEntry = ConversationLog(
        date = date,
        agents = nodeInfo['agents'],
        title = nodeInfo['title'],
        topic_text = nodeInfo['topic_text'],
        topic_id = nodeInfo['topic_id'],
        log_text = nodeInfo['convo_log'],
        engine = nodeInfo['engine']
       
    )

    newConvoLogEntry.save()
    return Response({"Convo Log added to backend"})

@api_view(['POST'])
def addStoredPaper(request):
    nodeInfo = request.data
    date = datetime.strptime(nodeInfo['Date'], "%Y-%m-%d")
    date_accessed = datetime.strptime(nodeInfo['Date_accessed'], "%Y-%m-%d %H:%M:%S")
    newStoredPaper = StoredPapers(
        doi = nodeInfo['DOI'],
        title = nodeInfo['Title'],
        authors = nodeInfo['Authors'],
        date = date,
        date_accessed = date_accessed
        
    )

    newStoredPaper.save()
    return Response({"Stored paper added to backend"})




