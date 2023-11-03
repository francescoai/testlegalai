import logging
logger = logging.getLogger(__name__)
import os
import json
import openai
from django.http import JsonResponse, HttpResponseServerError, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

# Configura la tua chiave API di OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY') or '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'

# ID del modello fine-tuned
FINE_TUNED_MODEL_ID = 'ft:gpt-3.5-turbo-0613:personal::8EnoFVoZ'  # Sostituisci con il tuo modello fine-tuned

# La tua vista chat esistente
def chat(request):
    return render(request, 'chat.html')

@method_decorator(csrf_exempt, name='dispatch')
class ChatBotView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        message_text = data.get('message')
        if not message_text:
            return JsonResponse({'error': 'No message provided'}, status=400)

        messages = [
            {"role": "system", "content": "You are now chatting with an AI."},
            {"role": "user", "content": message_text}
        ]

        try:
            response = openai.ChatCompletion.create(
                model=FINE_TUNED_MODEL_ID,
                messages=messages,
                max_tokens=150,
                temperature=0.5,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            print("Response object:", response)

            message = response.choices[0].message['content']  # Percorso aggiornato per accedere al contenuto del messaggio
            return JsonResponse({'message': message})
        except Exception as e:
            print("Error:", e)
            logger.error("Error: %s", e, exc_info=True)
            return HttpResponseServerError(str(e))
@method_decorator(csrf_exempt, name='dispatch')
class UploadTrainingFileView(View):
    def post(self, request, *args, **kwargs):
        # Assumi che 'file' sia il nome del campo nel form di upload del file.
        if 'file' not in request.FILES:
            return HttpResponse("No file to upload.", status=400)

        file_to_upload = request.FILES['file']
        try:
            # Esempio di utilizzo dell'API di OpenAI per creare un file di addestramento
            response = openai.File.create(
                file=file_to_upload,
                purpose='fine-tune'
            )
            return JsonResponse({'file_id': response['id']})
        except Exception as e:
            # Restituisce un messaggio di errore se qualcosa va storto
            return HttpResponse(str(e), status=500)
