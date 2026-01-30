from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from .models import Booking


@api_view(['POST'])
def check_availability(request):
    """Проверяет доступность аудитории"""
    room = request.data.get('room')
    date = request.data.get('date')
    time_start = request.data.get('time_start')
    time_end = request.data.get('time_end')

    if not all([room, date, time_start, time_end]):
        return Response({
            'available': False,
            'reason': 'Не все поля заполнены'
        }, status=400)

    try:
        # Преобразуем строки в объекты
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        start_obj = datetime.strptime(time_start, "%H:%M").time()
        end_obj = datetime.strptime(time_end, "%H:%M").time()

        # Проверяем пересечения с существующими бронированиями
        conflicting = Booking.objects.filter(
            room=room,
            date=date_obj,
            time_start__lt=end_obj,
            time_end__gt=start_obj
        ).exists()

        if conflicting:
            return Response({
                'available': False,
                'reason': 'Аудитория занята в это время'
            })

        return Response({
            'available': True,
            'room': room
        })

    except Exception as e:
        return Response({
            'available': False,
            'reason': f'Ошибка: {str(e)}'
        }, status=400)


@api_view(['GET'])
def health_check(request):
    """Проверка работы сервиса"""
    return Response({
        'status': 'ok',
        'service': 'Availability Check Service'
    })