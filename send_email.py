from retrieve_data import retrieve_active_alerts, change_enviado_field
from babel.numbers import format_currency
from email.message import EmailMessage
import smtplib
import ssl
from datetime import datetime
import os
import pytz

br_tz = pytz.timezone("America/Sao_Paulo")

password = os.getenv("EMAIL_PASSWORD")
from_email = 'cryptoradaroficial@gmail.com'

def send_emails(filtered_alerts):
    """Envia os e-mails de alerta."""
    success_count = 0
    fail_count = 0

    safe = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=safe) as smtp:
            smtp.login(from_email, password)

            for alert in filtered_alerts:
                try:
                    message = EmailMessage()
                    message['From'] = from_email
                    message['To'] = alert["email"]
                    message['Subject'] = f"[Alerta] {alert['cripto'].capitalize()} atingiu o valor de {alert['tipo']} definido!"

                    body = f"""\
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <title>Alerta de Criptomoeda</title>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                background-color: #f4f4f4;
                                margin: 0;
                                padding: 0;
                            }}
                            .container {{
                                width: 80%;
                                max-width: 600px;
                                background: #ffffff;
                                margin: 20px auto;
                                padding: 20px;
                                border-radius: 10px;
                                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                            }}
                            .content {{
                                font-size: 16px;
                                color: #333;
                                line-height: 1.5;
                            }}
                            .bold {{
                                font-weight: bold;
                            }}
                            .info {{
                                background: #f8f8f8;
                                padding: 10px;
                                border-radius: 5px;
                                margin-top: 10px;
                            }}
                            .footer {{
                                text-align: left;
                                font-size: 15px;
                                color: #333;
                                margin-top: 24px;
                            }}
                        </style>
                    </head>
                    <body>

                        <div class="container">
                            <div class="content">
                                <p style="color: #333;">Olá, {alert['nome']} 👋</p>

                                <p style="color: #333;">Temos novidades para você! A criptomoeda <span class="bold">{alert['cripto'].capitalize()}</span> atingiu o valor de <span class="bold">{alert['tipo']}</span> que você definiu.</p>

                                <div class="info">
                                    <p>🔹 <span class="bold">Valor definido:</span> {format_currency(alert['valor'], alert['moeda'].upper(), locale='pt_BR')}</p>
                                    <p>🔹 <span class="bold">Cotação atual:</span> {format_currency(alert['cotacao_atual'], alert['moeda'].upper(), locale='pt_BR')}</p>
                                    <p>📅 <span class="bold">Data e horário da cotação:</span> {alert['horario_cotacao_atual']}</p>
                                </div>

                                <p style="color: #333;">Caso queira adicionar um novo alerta para esta criptomoeda, acesse sua conta em nosso sistema.</p>
                            </div>

                            <div class="footer">
                                <span>Atenciosamente,</span>
                                <span style="display: block; margin-top: 5px;">Equipe CryptoRadar</span>
                            </div>
                        </div>

                    </body>
                    </html>
                    """

                    message.set_content("Seu cliente de e-mail não suporta HTML. Acesse sua conta para visualizar o alerta.")
                    message.add_alternative(body, subtype="html")

                    response = smtp.sendmail(from_email, alert["email"], message.as_string())

                    if not response:
                        print(f"E-mail enviado com sucesso para {alert['email']}")
                        success_count += 1
                        change_enviado_field(alert['id'])
                    else:
                        print(f"Falha no envio do e-mail para {alert['email']}. Resposta SMTP: {response}")
                        fail_count += 1

                except smtplib.SMTPException as e:
                    print(f"Erro ao enviar e-mail para {alert['email']}: {e}")
                    fail_count += 1

    except smtplib.SMTPException as e:
        print(f"Erro ao conectar ao servidor SMTP: {e}")
        return

    print(f"\nData e hora: {datetime.now(br_tz).strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Total de e-mails enviados: {success_count}")
    print(f"Total de falhas no envio: {fail_count}")

if __name__ == "__main__":
    filtered_alerts = retrieve_active_alerts()
    if filtered_alerts:  # Só chama send_emails() se houver alertas ativos
        send_emails(filtered_alerts)
    else:
        print("Nenhum alerta ativo encontrado.")
