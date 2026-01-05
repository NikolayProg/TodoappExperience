import base64
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
import requests
from django.shortcuts import render
import json
from django.views import View
import qrcode
import requests
from openai.resources.containers.files import content


class OpenRouterChatView(View):

    def get(self, request):
        wish_text = self.get_wish_from_neural_network()

        if wish_text:
            qr_code_image = self.generate_qr_code(wish_text)
            return HttpResponse(qr_code_image.getvalue(), content_type='image/png')
        else:
            return render(request, 'wishmellm/wish_response.html', {
                'error': "Не удалось получить пожелание от нейросети."
            })

    def get_access_token(self):
        auth_key = settings.AUTH_KEY
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        auth_header = f'Basic {auth_key}'

        payload = {
            'scope': 'GIGACHAT_API_PERS'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': 'e229d4e8-95ac-4f7c-be97-3ac165adc345',
            'Authorization': auth_header,
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        if response.status_code != 200:
            print("Ошибка при получении токена:", response.text)
            return

        token = response.json().get('access_token')

        if not token:
            print("Токен не получен")
        return token

    def get_wish_from_neural_network(self):
        url_ans = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        token = self.get_access_token()
        user_message = ("Предложи позитивное пожелание на русском языке, состоящее не более, чем из 20 слов.")

        payload = {"model": "GigaChat",
                   "messages": [
                       {
                           "content": user_message,
                            "role": "user",
                               }
                   ],
                   "stream": False,
                   "update_interval": 0}
        headers = {
            "Accept": "application/json",
            "Authorization": f'Bearer {token}',
            "Content-Type": "application/json",
        }

        print("Отправляемый JSON:", json.dumps(payload, ensure_ascii=False))

        response = requests.request("POST", url_ans, headers=headers, json=payload, verify=False)

        if response.status_code != 200:
            print("Ошибка при запросе к модели:", response.text)
            return

        answer = response.json()
        print("Ответ нейросети:", answer)

        if 'choices' in answer and len(answer['choices']) > 0:
            wish_text = answer['choices'][0]['message']['content']
            return wish_text
        else:
            print("Ответ не содержит ожидаемого текста.")
            return None

    def generate_qr_code(self, text):
        # Генерация QR-кода
        qr = qrcode.QRCode(version=1, box_size=5, border=2)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Сохранение QR-кода в байтовый поток
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf
