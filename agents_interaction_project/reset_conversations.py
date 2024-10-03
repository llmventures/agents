import os
import sys
import django

def reset_conversations():
    with open('cur_chunk_id_pointer', 'w') as file:
        file.write("0")

    directory = "./chat_logs"


    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    #reset django backend
    sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    django.setup()
    from dialogue_display.models import ConversationLog

    ConversationLog.objects.all().delete()


reset_conversations()

