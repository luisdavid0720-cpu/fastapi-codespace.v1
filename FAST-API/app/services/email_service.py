import asyncio
import threading
from datetime import datetime

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType


# =====================================================
# CONFIGURACIÓN SMTP GMAIL
# =====================================================

conf = ConnectionConfig(
    MAIL_USERNAME="luisdavid0720@gmail.com",
    MAIL_PASSWORD="kupcedwwugvqhwvc",
    MAIL_FROM="luisdavid0720@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

fm = FastMail(conf)


# =====================================================
# ENVÍO INTERNO ASYNC
# =====================================================

async def _async_send(subject: str, html_body: str):
    message = MessageSchema(
        subject=subject,
        recipients=["luisdavid0720@gmail.com"],
        body=html_body,
        subtype=MessageType.html
    )

    await fm.send_message(message)


# =====================================================
# ENVÍO SEGURO PARA FASTAPI / RENDER
# =====================================================

def _send_email(subject: str, html_body: str):
    try:
        # Si ya existe event loop (FastAPI/Render)
        try:
            asyncio.get_running_loop()

            # Lo mandamos en hilo aparte
            def runner():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(
                    _async_send(subject, html_body)
                )
                loop.close()

            threading.Thread(target=runner).start()

        except RuntimeError:
            # Si NO hay loop abierto
            asyncio.run(
                _async_send(subject, html_body)
            )

        print("Correo enviado correctamente")
        return True

    except Exception as e:
        print("ERROR ENVIANDO CORREO:", e)
        return False


# =====================================================
# PLANTILLA BASE HTML
# =====================================================

def _base_template(title: str, color: str, content: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <body style="font-family:Arial;background:#f4f6f8;padding:30px;">
        <div style="
            max-width:600px;
            margin:auto;
            background:white;
            border-radius:8px;
            overflow:hidden;
            box-shadow:0 2px 8px rgba(0,0,0,.08);
        ">
            <div style="background:{color};padding:20px;color:white;">
                <h2 style="margin:0;">Sistema PQRS</h2>
                <p style="margin:5px 0 0;">Notificación automática</p>
            </div>

            <div style="padding:30px;">
                <h3>{title}</h3>
                {content}

                <hr style="margin-top:30px;">
                <small style="color:#777;">
                    © {datetime.now().year} Sistema PQRS
                </small>
            </div>
        </div>
    </body>
    </html>
    """


# =====================================================
# CORREO PQR CREADA
# =====================================================

def notify_pqr_creada(
    correo_usuario,
    nombre_usuario,
    id_pqr,
    descripcion,
    tipo,
    departamento,
    fecha
):
    body = f"""
    <p>Hola <strong>{nombre_usuario}</strong>, tu solicitud fue registrada exitosamente.</p>

    <table style="width:100%;border-collapse:collapse;">
        <tr><td><strong>Radicado:</strong></td><td>#{id_pqr}</td></tr>
        <tr><td><strong>Tipo:</strong></td><td>{tipo}</td></tr>
        <tr><td><strong>Departamento:</strong></td><td>{departamento}</td></tr>
        <tr><td><strong>Fecha:</strong></td><td>{fecha}</td></tr>
        <tr><td><strong>Descripción:</strong></td><td>{descripcion}</td></tr>
    </table>

    <p style="margin-top:20px;color:green;">
        ✅ Recibirás actualizaciones pronto.
    </p>
    """

    return _send_email(
        subject=f"PQR #{id_pqr} registrada",
        html_body=_base_template(
            "Nueva solicitud registrada",
            "#16a34a",
            body
        )
    )


# =====================================================
# CORREO CAMBIO DE ESTADO
# =====================================================

def notify_cambio_estado_pqr(
    correo_usuario,
    nombre_usuario,
    id_pqr,
    estado_anterior,
    estado_nuevo
):
    body = f"""
    <p>Hola <strong>{nombre_usuario}</strong>.</p>

    <p>Tu PQR <strong>#{id_pqr}</strong> cambió de estado.</p>

    <table style="width:100%;border-collapse:collapse;">
        <tr><td><strong>Estado anterior:</strong></td><td>{estado_anterior}</td></tr>
        <tr><td><strong>Nuevo estado:</strong></td><td>{estado_nuevo}</td></tr>
    </table>

    <p style="margin-top:20px;color:#2563eb;">
        🔔 Revisa la plataforma.
    </p>
    """

    return _send_email(
        subject=f"PQR #{id_pqr} actualizada",
        html_body=_base_template(
            "Cambio de estado",
            "#2563eb",
            body
        )
    )


# =====================================================
# TEST MANUAL
# =====================================================

def enviar_test():
    return _send_email(
        "Correo de prueba Render",
        _base_template(
            "Prueba exitosa",
            "#16a34a",
            "<p>Todo funciona correctamente.</p>"
        )
    )

def notify_usuario_eliminado(
    correo_admin,
    nombre_usuario,
    cedula,
    cargo
):
    body = f"""
    <p>Se eliminó un usuario del sistema.</p>

    <table>
        <tr><td><strong>Nombre:</strong></td><td>{nombre_usuario}</td></tr>
        <tr><td><strong>Cédula:</strong></td><td>{cedula}</td></tr>
        <tr><td><strong>Cargo:</strong></td><td>{cargo}</td></tr>
    </table>
    """

    return _send_email(
        subject="Usuario eliminado",
        html_body=_base_template(
            "Usuario eliminado",
            "#dc2626",
            body
        )
    )

def notify_respuesta_pqr(correo_usuario, nombre_usuario, id_pqr, respuesta):
  asunto = f"Respuesta a tu solicitud #{id_pqr}"

  cuerpo = f"""
Hola {nombre_usuario},

Tu solicitud #{id_pqr} fue respondida.

Respuesta:
{respuesta}

Gracias.
"""

    send_email(correo_usuario, asunto, cuerpo)