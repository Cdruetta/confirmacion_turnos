import schedule
import time
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Configuración global para el servidor SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
CORREO_ORIGEN = "nuestro_correo@gmail.com"
CONTRASEÑA = "nuestra_clave"


def enviar_correo(correo_destino, asunto, mensaje):
    try:
        # Configuración del mensaje
        msg = MIMEMultipart()
        msg["From"] = CORREO_ORIGEN
        msg["To"] = correo_destino
        msg["Subject"] = asunto
        msg.attach(MIMEText(mensaje, "plain"))

        # Configuración del servidor
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as servidor:
            servidor.starttls()
            servidor.login(CORREO_ORIGEN, CONTRASEÑA)
            servidor.sendmail(CORREO_ORIGEN, correo_destino, msg.as_string())
    except Exception as e:
        print(f"Error al enviar correo: {e}")


def enviar_recordatorios():
    # Conectar con tu base de datos y obtener las reservas
    reservas = [
        {"correo": "afiliado_correo@gmail.com", "fecha": "2024-07-22", "hora": "10:00"},
        {"correo": "afiliado_correo@gmail.com", "fecha": "2024-07-23", "hora": "14:00"},
        {"correo": "afiliado_correo@gmail.com", "fecha": "2024-07-24", "hora": "16:00"},
    ]

    hoy = datetime.date.today().strftime("%Y-%m-%d")

    for reserva in reservas:
        if reserva["fecha"] == hoy:
            mensaje = f"Tu turno está programado para hoy a las {reserva['hora']}."
            enviar_correo(reserva["correo"], "Recordatorio de Turno", mensaje)


# Programar la tarea que se ejecuta cada día a las 08:00
schedule.every().day.at("08:00").do(enviar_recordatorios)

while True:
    schedule.run_pending()
    time.sleep(1)
