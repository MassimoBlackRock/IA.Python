import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class TradingAlerts:
    def __init__(self, patrones_file, alertas_file, smtp_config):
        self.patrones_file = patrones_file
        self.alertas_file = alertas_file
        self.smtp_config = smtp_config

    def leer_patrones(self):
        """Lee el archivo de patrones detectados y retorna una lista de patrones."""
        patrones = []
        try:
            with open(self.patrones_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    patrones.append(row)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {self.patrones_file}.")
        return patrones

    def generar_alertas(self, patrones):
        """Genera un archivo de texto con alertas basadas en los patrones detectados."""
        try:
            with open(self.alertas_file, mode='w') as file:
                file.write("Alertas generadas a partir de patrones detectados:\n\n")
                for patron in patrones:
                    alerta = f"Patrón detectado: {patron['patron']} en {patron['activo']} a las {patron['hora']} con nivel de impacto {patron['impacto']}."
                    file.write(alerta + "\n")
        except Exception as e:
            print(f"Error al generar el archivo de alertas: {e}")

    def enviar_alertas_email(self):
        """Envía las alertas generadas por correo electrónico usando SMTP."""
        try:
            # Configurar el cliente SMTP
            server = smtplib.SMTP(self.smtp_config['host'], self.smtp_config['port'])
            server.starttls()
            server.login(self.smtp_config['user'], self.smtp_config['password'])

            # Crear el mensaje
            with open(self.alertas_file, mode='r') as file:
                alertas_content = file.read()

            mensaje = MIMEMultipart()
            mensaje['From'] = self.smtp_config['user']
            mensaje['To'] = self.smtp_config['recipient']
            mensaje['Subject'] = "Alertas de Trading"

            mensaje.attach(MIMEText(alertas_content, 'plain'))

            # Enviar el correo
            server.send_message(mensaje)
            server.quit()
            print("Alertas enviadas por correo electrónico.")
        except Exception as e:
            print(f"Error al enviar las alertas por correo electrónico: {e}")

if __name__ == "__main__":
    # Configuración inicial
    smtp_config = {
        'host': 'smtp.example.com',
        'port': 587,
        'user': 'tu_email@example.com',
        'password': 'tu_contraseña',
        'recipient': 'destinatario@example.com'
    }

    # Archivos
    patrones_file = "patrones_detectados.csv"
    alertas_file = "alertas.txt"

    # Crear instancia del sistema de alertas
    sistema_alertas = TradingAlerts(patrones_file, alertas_file, smtp_config)

    # Leer patrones, generar alertas y enviar por correo
    patrones_detectados = sistema_alertas.leer_patrones()
    if patrones_detectados:
        sistema_alertas.generar_alertas(patrones_detectados)
        sistema_alertas.enviar_alertas_email()
