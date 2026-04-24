import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from datetime import datetime


# ─────────────────────────────────────────────
# CONFIGURACIÓN fastapi-mail
# Lee las variables de entorno de Vercel
# ─────────────────────────────────────────────

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


# ─────────────────────────────────────────────
# UTILIDAD INTERNA
# ─────────────────────────────────────────────

import asyncio

import asyncio

def _send_email(to_email: str, subject: str, html_body: str):
    try:
        message = MessageSchema(
            subject=subject,
            recipients=["luisdavid0720@gmail.com"],
            body=html_body,
            subtype=MessageType.html
        )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(fm.send_message(message))
        loop.close()

        print("Correo enviado correctamente")
        return True

    except Exception as e:
        print("ERROR ENVIANDO CORREO:", str(e))
        return False


def _base_template(title: str, color: str, content: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8"/>
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>
    <body style="margin:0;padding:0;background:#f4f6f8;font-family:Arial,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f6f8;padding:30px 0;">
        <tr><td align="center">
          <table width="600" cellpadding="0" cellspacing="0"
                 style="background:#ffffff;border-radius:8px;overflow:hidden;
                        box-shadow:0 2px 8px rgba(0,0,0,0.08);">
            <tr>
              <td style="background:{color};padding:24px 32px;">
                <h1 style="margin:0;color:#ffffff;font-size:22px;font-weight:700;">
                  Sistema PQRS
                </h1>
                <p style="margin:4px 0 0;color:rgba(255,255,255,0.85);font-size:14px;">
                  Notificación automática
                </p>
              </td>
            </tr>
            <tr>
              <td style="padding:32px;">
                <h2 style="margin:0 0 16px;color:#1a1a2e;font-size:18px;">{title}</h2>
                {content}
                <p style="margin:24px 0 0;font-size:12px;color:#999;">
                  Este es un mensaje automático. Por favor no responda a este correo.<br/>
                  © {datetime.now().year} Sistema PQRS
                </p>
              </td>
            </tr>
          </table>
        </td></tr>
      </table>
    </body>
    </html>
    """


def _info_row(label: str, value: str) -> str:
    return f"""
    <tr>
      <td style="padding:6px 0;color:#555;font-size:14px;width:40%;
                 border-bottom:1px solid #f0f0f0;"><strong>{label}</strong></td>
      <td style="padding:6px 0;color:#222;font-size:14px;
                 border-bottom:1px solid #f0f0f0;">{value}</td>
    </tr>
    """


# ═══════════════════════════════════════════════════════
# 1. USUARIO ELIMINADO
# ═══════════════════════════════════════════════════════

def notify_usuario_eliminado(correo_admin, nombre_usuario, cedula, cargo) -> bool:
    content = f"""
    <p style="color:#444;font-size:14px;line-height:1.6;">
      Se ha eliminado un usuario del sistema PQRS. A continuación los detalles:
    </p>
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:16px 0;">
      {_info_row("Nombre", nombre_usuario)}
      {_info_row("Cédula", cedula)}
      {_info_row("Cargo", cargo)}
      {_info_row("Fecha / hora", datetime.now().strftime("%d/%m/%Y %H:%M"))}
    </table>
    <p style="color:#e53e3e;font-size:13px;background:#fff5f5;padding:12px;
              border-left:4px solid #e53e3e;border-radius:4px;">
      ⚠️ Esta acción es permanente. El usuario ya no tendrá acceso al sistema.
    </p>
    """
    return _send_email(
        to_email=correo_admin,
        subject="⚠️ Usuario eliminado del sistema PQRS",
        html_body=_base_template(title="Usuario eliminado", color="#e53e3e", content=content)
    )


# ═══════════════════════════════════════════════════════
# 2. REPORTE GENERADO
# ═══════════════════════════════════════════════════════

def notify_reporte_generado(correo_destinatario, nombre_usuario, total_pqrs,
                             pendientes, en_proceso, resueltas, periodo="General") -> bool:
    content = f"""
    <p style="color:#444;font-size:14px;line-height:1.6;">
      Hola <strong>{nombre_usuario}</strong>, el reporte del sistema PQRS ha sido generado exitosamente.
    </p>
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:16px 0;">
      {_info_row("Período", periodo)}
      {_info_row("Total de PQRs", str(total_pqrs))}
      {_info_row("Pendientes", f'<span style="color:#d69e2e;">{pendientes}</span>')}
      {_info_row("En proceso", f'<span style="color:#3182ce;">{en_proceso}</span>')}
      {_info_row("Resueltas", f'<span style="color:#38a169;">{resueltas}</span>')}
      {_info_row("Generado el", datetime.now().strftime("%d/%m/%Y %H:%M"))}
    </table>
    """
    return _send_email(
        to_email=correo_destinatario,
        subject=f"📊 Reporte PQRS generado — {periodo}",
        html_body=_base_template(title="Reporte generado exitosamente", color="#3182ce", content=content)
    )


# ═══════════════════════════════════════════════════════
# 3. PQR CREADA
# ═══════════════════════════════════════════════════════

def notify_pqr_creada(correo_usuario, nombre_usuario, id_pqr,
                       descripcion, tipo, departamento, fecha) -> bool:
    resumen = descripcion[:120] + "..." if len(descripcion) > 120 else descripcion
    content = f"""
    <p style="color:#444;font-size:14px;line-height:1.6;">
      Hola <strong>{nombre_usuario}</strong>, tu solicitud ha sido registrada exitosamente en el sistema.
    </p>
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:16px 0;">
      {_info_row("N° de radicado", f"<strong>#{id_pqr}</strong>")}
      {_info_row("Tipo", tipo)}
      {_info_row("Departamento", departamento)}
      {_info_row("Fecha de radicado", fecha)}
      {_info_row("Descripción", resumen)}
    </table>
    <p style="color:#276749;font-size:13px;background:#f0fff4;padding:12px;
              border-left:4px solid #38a169;border-radius:4px;">
      ✅ Recibirás actualizaciones por correo a medida que tu solicitud sea procesada.
    </p>
    """
    return _send_email(
        to_email=correo_usuario,
        subject=f"✅ PQR #{id_pqr} registrada exitosamente",
        html_body=_base_template(title=f"Tu solicitud #{id_pqr} fue registrada", color="#38a169", content=content)
    )


# ═══════════════════════════════════════════════════════
# 4. CAMBIO DE ESTADO DE PQR
# ═══════════════════════════════════════════════════════

def notify_cambio_estado_pqr(correo_usuario, nombre_usuario, id_pqr,
                               estado_anterior, estado_nuevo) -> bool:
    colores_estado = {
        "pendiente": "#d69e2e", "en proceso": "#3182ce",
        "resuelto": "#38a169", "cerrado": "#718096",
    }
    color_nuevo = colores_estado.get(estado_nuevo.lower(), "#667eea")
    content = f"""
    <p style="color:#444;font-size:14px;line-height:1.6;">
      Hola <strong>{nombre_usuario}</strong>, el estado de tu PQR ha sido actualizado.
    </p>
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:16px 0;">
      {_info_row("N° de radicado", f"<strong>#{id_pqr}</strong>")}
      {_info_row("Estado anterior", estado_anterior)}
      {_info_row("Nuevo estado", f'<span style="color:{color_nuevo};font-weight:bold;">{estado_nuevo}</span>')}
      {_info_row("Actualizado el", datetime.now().strftime("%d/%m/%Y %H:%M"))}
    </table>
    <p style="color:#553c9a;font-size:13px;background:#faf5ff;padding:12px;
              border-left:4px solid #805ad5;border-radius:4px;">
      🔔 Ingresa al sistema para ver más detalles de tu solicitud.
    </p>
    """
    return _send_email(
        to_email=correo_usuario,
        subject=f"🔔 PQR #{id_pqr} — Estado actualizado: {estado_nuevo}",
        html_body=_base_template(title="Estado de tu PQR actualizado", color="#805ad5", content=content)
    )


# ═══════════════════════════════════════════════════════
# 5. ASIGNACIÓN DE RESPONSABLE
# ═══════════════════════════════════════════════════════

def notify_asignacion_responsable(correo_responsable, nombre_responsable, id_pqr,
                                   descripcion_pqr, departamento, prioridad, fecha_asignacion) -> bool:
    resumen = descripcion_pqr[:120] + "..." if len(descripcion_pqr) > 120 else descripcion_pqr
    colores_prioridad = {"alta": "#e53e3e", "media": "#d69e2e", "baja": "#38a169"}
    color_prior = colores_prioridad.get(prioridad.lower(), "#3182ce")
    content = f"""
    <p style="color:#444;font-size:14px;line-height:1.6;">
      Hola <strong>{nombre_responsable}</strong>, se te ha asignado una nueva PQR para gestión.
    </p>
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:16px 0;">
      {_info_row("N° de radicado", f"<strong>#{id_pqr}</strong>")}
      {_info_row("Departamento", departamento)}
      {_info_row("Prioridad", f'<span style="color:{color_prior};font-weight:bold;">{prioridad}</span>')}
      {_info_row("Fecha de asignación", fecha_asignacion)}
      {_info_row("Descripción", resumen)}
    </table>
    <p style="color:#c05621;font-size:13px;background:#fffaf0;padding:12px;
              border-left:4px solid #dd6b20;border-radius:4px;">
      📋 Por favor ingresa al sistema y atiende esta solicitud a la brevedad posible.
    </p>
    """
    return _send_email(
        to_email=correo_responsable,
        subject=f"📋 Nueva PQR #{id_pqr} asignada — Prioridad {prioridad}",
        html_body=_base_template(title="Nueva PQR asignada a tu gestión", color="#dd6b20", content=content)
    )


# ═══════════════════════════════════════════════════════
# 6. RESPUESTA A UNA PQR
# ═══════════════════════════════════════════════════════

def notify_respuesta_pqr(correo_usuario, nombre_usuario, id_pqr,
                          mensaje_respuesta, nombre_responsable) -> bool:
    content = f"""
    <p style="color:#444;font-size:14px;line-height:1.6;">
      Hola <strong>{nombre_usuario}</strong>, tu PQR ha recibido una respuesta.
    </p>
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:16px 0;">
      {_info_row("N° de radicado", f"<strong>#{id_pqr}</strong>")}
      {_info_row("Respondido por", nombre_responsable)}
      {_info_row("Fecha de respuesta", datetime.now().strftime("%d/%m/%Y %H:%M"))}
    </table>
    <div style="margin:16px 0;padding:16px;background:#f7fafc;border-radius:6px;
                border:1px solid #e2e8f0;">
      <p style="margin:0 0 8px;font-size:12px;color:#718096;text-transform:uppercase;">Mensaje de respuesta</p>
      <p style="margin:0;font-size:14px;color:#2d3748;line-height:1.7;">{mensaje_respuesta}</p>
    </div>
    <p style="color:#276749;font-size:13px;background:#f0fff4;padding:12px;
              border-left:4px solid #38a169;border-radius:4px;">
      💬 Ingresa al sistema para ver el hilo completo de tu solicitud.
    </p>
    """
    return _send_email(
        to_email=correo_usuario,
        subject=f"💬 Tu PQR #{id_pqr} tiene una nueva respuesta",
        html_body=_base_template(title="Nueva respuesta a tu PQR", color="#38a169", content=content)
    )