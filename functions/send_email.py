import yagmail
import os
from dotenv import load_dotenv
from datetime import datetime
from .read_params import get_info

def send_email(execution_type):

    # Credenciales
    load_dotenv()
    gmail = os.getenv("GMAIL")
    password = os.getenv("PASSWORD")
    date = datetime.now()

    # Convertir mes
    meses = get_info("month")
    mes_numero = str(date.month)
    mes_letra = meses[mes_numero]

    # Conectarme a mi correo
    yag = yagmail.SMTP(gmail,password)

    yag.send(
        to = "mariotirado2003@gmail.com",
        subject= "Ejecución diaria",
        contents= f"Ejecución día {date.day} de {mes_letra} {execution_type}"
    )
