import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from config.db_config import get_db_connection
from models.pqr_model import Pqr
from services.email_service import (
    notify_pqr_creada,
    notify_cambio_estado_pqr
)


class PqrController:

    # =====================================================
    # UTILIDADES
    # =====================================================

    def _get_usuario_correo(self, cursor, id_usuario: int):
        try:
            cursor.execute(
                "SELECT nombre, correo FROM usuario WHERE id_usuario = %s",
                (id_usuario,)
            )
            row = cursor.fetchone()
            return (row[0], row[1]) if row else (None, None)
        except Exception:
            return (None, None)

    def _get_nombre(
        self,
        cursor,
        tabla: str,
        campo_id: str,
        campo_nombre: str,
        valor_id: int
    ):
        try:
            cursor.execute(
                f"SELECT {campo_nombre} FROM {tabla} WHERE {campo_id} = %s",
                (valor_id,)
            )
            row = cursor.fetchone()
            return row[0] if row else str(valor_id)
        except Exception:
            return str(valor_id)

    # =====================================================
    # CREAR PQR
    # =====================================================

    def create_pqr(self, pqr: Pqr):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO pqr
                (
                    descripcion,
                    fecha,
                    id_usuario,
                    id_tipo,
                    id_estado,
                    id_departamento,
                    id_prioridad
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                RETURNING id_pqr
            """, (
                pqr.descripcion,
                pqr.fecha,
                pqr.id_usuario,
                pqr.id_tipo,
                pqr.id_estado,
                pqr.id_departamento,
                pqr.id_prioridad
            ))

            nuevo_id = cursor.fetchone()[0]
            conn.commit()

            print("PQR creada:", nuevo_id)

            nombre_u, correo_u = self._get_usuario_correo(
                cursor,
                pqr.id_usuario
            )

            tipo = self._get_nombre(
                cursor,
                "tipo_pqr",
                "id_tipo",
                "nombre",
                pqr.id_tipo
            )

            depto = self._get_nombre(
                cursor,
                "departamento",
                "id_departamento",
                "nombre",
                pqr.id_departamento
            )

            if correo_u:
                notify_pqr_creada(
                    correo_usuario=correo_u,
                    nombre_usuario=nombre_u or "Usuario",
                    id_pqr=nuevo_id,
                    descripcion=pqr.descripcion,
                    tipo=tipo,
                    departamento=depto,
                    fecha=str(pqr.fecha)
                )

            return {
                "resultado": "PQR creada",
                "id_pqr": nuevo_id
            }

        except Exception as e:
            print("ERROR CREATE PQR:", e)

            if conn:
                conn.rollback()

            raise HTTPException(
                status_code=500,
                detail="Error al crear PQR"
            )

        finally:
            if conn:
                conn.close()

    # =====================================================
    # OBTENER UNA PQR
    # =====================================================

    def get_pqr(self, pqr_id: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM pqr WHERE id_pqr = %s",
                (pqr_id,)
            )

            result = cursor.fetchone()

            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="PQR no encontrada"
                )

            content = {
                "id_pqr": result[0],
                "descripcion": result[1],
                "fecha": result[2],
                "id_usuario": result[3],
                "id_tipo": result[4],
                "id_estado": result[5],
                "id_departamento": result[6],
                "id_prioridad": result[7]
            }

            return jsonable_encoder(content)

        finally:
            if conn:
                conn.close()

    # =====================================================
    # OBTENER TODAS LAS PQRS
    # =====================================================

    def get_pqrs(self):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM pqr")
            result = cursor.fetchall()

            payload = []

            for row in result:
                payload.append({
                    "id_pqr": row[0],
                    "descripcion": row[1],
                    "fecha": row[2],
                    "id_usuario": row[3],
                    "id_tipo": row[4],
                    "id_estado": row[5],
                    "id_departamento": row[6],
                    "id_prioridad": row[7]
                })

            return {"resultado": jsonable_encoder(payload)}

        finally:
            if conn:
                conn.close()

    # =====================================================
    # ACTUALIZAR PQR COMPLETA
    # =====================================================

    def update_pqr(self, pqr_id: int, pqr: Pqr):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE pqr
                SET descripcion = %s,
                    fecha = %s,
                    id_usuario = %s,
                    id_tipo = %s,
                    id_estado = %s,
                    id_departamento = %s,
                    id_prioridad = %s
                WHERE id_pqr = %s
            """, (
                pqr.descripcion,
                pqr.fecha,
                pqr.id_usuario,
                pqr.id_tipo,
                pqr.id_estado,
                pqr.id_departamento,
                pqr.id_prioridad,
                pqr_id
            ))

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="PQR no encontrada"
                )

            return {"resultado": "PQR actualizada"}

        finally:
            if conn:
                conn.close()

    # =====================================================
    # ELIMINAR PQR
    # =====================================================

    def delete_pqr(self, pqr_id: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM pqr WHERE id_pqr = %s",
                (pqr_id,)
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="PQR no encontrada"
                )

            return {"resultado": "PQR eliminada"}

        finally:
            if conn:
                conn.close()

    # =====================================================
    # CAMBIAR SOLO ESTADO
    # =====================================================

    def update_estado_pqr(self, pqr_id: int, nuevo_estado_id: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT p.id_usuario, e.nombre
                FROM pqr p
                JOIN estado e ON e.id_estado = p.id_estado
                WHERE p.id_pqr = %s
            """, (pqr_id,))

            row = cursor.fetchone()

            if not row:
                raise HTTPException(
                    status_code=404,
                    detail="PQR no encontrada"
                )

            id_usuario = row[0]
            estado_anterior = row[1]

            cursor.execute("""
                UPDATE pqr
                SET id_estado = %s
                WHERE id_pqr = %s
            """, (nuevo_estado_id, pqr_id))

            conn.commit()

            cursor.execute(
                "SELECT nombre FROM estado WHERE id_estado = %s",
                (nuevo_estado_id,)
            )

            nuevo = cursor.fetchone()
            estado_nuevo = nuevo[0] if nuevo else "Actualizado"

            nombre_u, correo_u = self._get_usuario_correo(
                cursor,
                id_usuario
            )

            if correo_u:
                notify_cambio_estado_pqr(
                    correo_usuario=correo_u,
                    nombre_usuario=nombre_u or "Usuario",
                    id_pqr=pqr_id,
                    estado_anterior=estado_anterior,
                    estado_nuevo=estado_nuevo
                )

            return {"resultado": "Estado actualizado"}

        finally:
            if conn:
                conn.close()

    # =====================================================
    # FILTRAR POR USUARIO
    # =====================================================

    def get_pqrs_by_usuario(self, usuario_id: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM pqr WHERE id_usuario = %s",
                (usuario_id,)
            )

            result = cursor.fetchall()

            payload = []

            for row in result:
                payload.append({
                    "id_pqr": row[0],
                    "descripcion": row[1],
                    "fecha": row[2],
                    "id_usuario": row[3],
                    "id_tipo": row[4],
                    "id_estado": row[5],
                    "id_departamento": row[6],
                    "id_prioridad": row[7]
                })

            return {"resultado": jsonable_encoder(payload)}

        finally:
            if conn:
                conn.close()

    # =====================================================
    # FILTRAR POR ESTADO
    # =====================================================

    def get_pqrs_by_estado(self, estado_id: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM pqr WHERE id_estado = %s",
                (estado_id,)
            )

            result = cursor.fetchall()

            payload = []

            for row in result:
                payload.append({
                    "id_pqr": row[0],
                    "descripcion": row[1],
                    "fecha": row[2],
                    "id_usuario": row[3],
                    "id_tipo": row[4],
                    "id_estado": row[5],
                    "id_departamento": row[6],
                    "id_prioridad": row[7]
                })

            return {"resultado": jsonable_encoder(payload)}

        finally:
            if conn:
                if conn:
                    conn.close()

    # =====================================================
    # FILTRAR POR DEPARTAMENTO
    # =====================================================

    def get_pqrs_by_departamento(self, departamento_id: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM pqr WHERE id_departamento = %s",
                (departamento_id,)
            )

            result = cursor.fetchall()

            payload = []

            for row in result:
                payload.append({
                    "id_pqr": row[0],
                    "descripcion": row[1],
                    "fecha": row[2],
                    "id_usuario": row[3],
                    "id_tipo": row[4],
                    "id_estado": row[5],
                    "id_departamento": row[6],
                    "id_prioridad": row[7]
                })

            return {"resultado": jsonable_encoder(payload)}

        finally:
            if conn:
                conn.close()

    # =====================================================
    # FILTRAR POR PRIORIDAD
    # =====================================================

    def get_pqrs_by_prioridad(self, prioridad_id: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM pqr WHERE id_prioridad = %s",
                (prioridad_id,)
            )

            result = cursor.fetchall()

            payload = []

            for row in result:
                payload.append({
                    "id_pqr": row[0],
                    "descripcion": row[1],
                    "fecha": row[2],
                    "id_usuario": row[3],
                    "id_tipo": row[4],
                    "id_estado": row[5],
                    "id_departamento": row[6],
                    "id_prioridad": row[7]
                })

            return {"resultado": jsonable_encoder(payload)}

        finally:
            if conn:
                conn.close()