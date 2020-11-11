import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = str(os.getenv('TOKEN'))

PG_USER = str(os.getenv('PG_USER'))
PG_PASSWORD = str(os.getenv('PG_PASSWORD'))

IP = os.getenv('IP')

stations = [
            'Райымбек батыра', 'Жибек жолы', 'Алмалы', 'Абая', 'Байконыр',
            'Театр имени Мухтара Ауэзова', 'Алатау', 'Сайран', 'Москва'
            ]
