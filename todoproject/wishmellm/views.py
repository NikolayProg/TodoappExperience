from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
import requests
from django.shortcuts import render
from django.views import View
import qrcode
from .models import Wish


class OpenRouterChatView(View):

    def get(self, request):
        # Запрос к нейросети для генерации пожелания
        wish_text = self.get_wish_from_neural_network()

        if wish_text:
            # Генерация QR-кода из текста пожелания
            qr_code_image = self.generate_qr_code(wish_text)

            # wish_qr = Wish.objects.create(qr=qr_code_image)
            # wish_qr.save() #оставить для тестов, потом может убрать

            return HttpResponse(qr_code_image.getvalue(), content_type='image/png')

        else:
            return render(request, 'wishmellm/wish_response.html', {
                'error': "Не удалось получить пожелание от нейросети."
            })

    def get_wish_from_neural_network(self):
        api_key = settings.OPENROUTER_API_KEY
        user_message = "Offer a positive wish on russian language."

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "deepseek/deepseek-r1-0528:free",
                "messages": [
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }
        )

        if response.status_code == 200:
            api_response = response.json()
            return api_response.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        return "Получить пожелание не получилось. Нейросеть занята"

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
