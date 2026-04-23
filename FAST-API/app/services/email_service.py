from fastapi_mail import FastMail, MessageSchema
from config.mail_config import conf

async def enviar_correo(destino, asunto, cuerpo):
    mensaje = MessageSchema(
        subject=asunto,
        recipients=[destino],
        body=cuerpo,
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(mensaje)