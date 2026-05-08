import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.asignacion_responsable_model import Asignacion_responsable
from fastapi.encoders import jsonable_encoder
from services.email_service import notify_asignacion_responsable


class Asignacion_responsableController:

    def _get_campo(self, cursor, tabla, campo_id, campo_nombre, valor):
        try:
            cursor.execute(f"SELECT {campo_nombre} FROM {tabla} WHERE {campo_id} = %s", (valor,))
            row = cursor.fetchone()
            return row[0] if row else str(valor)
        except Exception:
            return str(valor)

    # =====================================================
    # CREAR ASIGNACIÓN
    # =====================================================

    def create_asignacion_responsable(self, asignacion_responsable: Asignacion_responsable):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO asignacion_responsable (id_pqr, id_usuario, fecha_asignacion)
                VALUES (%s, %s, %s)
            """, (
                asignacion_responsable.id_pqr,
                asignacion_responsable.id_usuario,
                asignacion_responsable.fecha_asignacion
            ))
            conn.commit()

            # Notificar al responsable asignado
            try:
                cursor.execute(
                    "SELECT nombre, correo FROM usuario WHERE id_usuario = %s",
                    (asignacion_responsable.id_usuario,)
                )
                responsable = cursor.fetchone()

                cursor.execute(
                    "SELECT p.descripcion, p.id_departamento, p.id_prioridad FROM pqr p WHERE p.id_pqr = %s",
                    (asignacion_responsable.id_pqr,)
                )
                pqr_data = cursor.fetchone()

                if responsable and pqr_data:
                    depto     = self._get_campo(cursor, "departamento", "id_departamento", "nombre", pqr_data[1])
                    prioridad = self._get_campo(cursor, "prioridad",    "id_prioridad",    "nombre", pqr_data[2])
                    notify_asignacion_responsable(
                        correo_responsable=responsable[1],
                        nombre_responsable=responsable[0],
                        id_pqr=asignacion_responsable.id_pqr,
                        descripcion_pqr=pqr_data[0],
                        departamento=depto,
                        prioridad=prioridad,
                        fecha_asignacion=str(asignacion_responsable.fecha_asignacion)
                    )
            except Exception as email_err:
                print(f"[WARN] No se pudo enviar correo de asignación: {email_err}")

            return {"resultado": "Asignacion_responsable creado"}

        except HTTPException:
            raise
        except Exception as e:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()

    # =====================================================
    # OBTENER UNA ASIGNACIÓN
    # =====================================================

    def get_asignacion_responsable(self, asignacion_responsable_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM asignacion_responsable WHERE id_asignacion = %s",
                (asignacion_responsable_id,)
            )
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Asignacion no encontrada")
            return jsonable_encoder({
                'id_asignacion': result[0], 'id_pqr': result[1],
                'id_usuario': result[2], 'fecha_asignacion': result[3]
            })
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()

    # =====================================================
    # OBTENER TODAS LAS ASIGNACIONES
    # =====================================================

    def get_asignacion_responsables(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM asignacion_responsable")
            result = cursor.fetchall()
            if not result:
                raise HTTPException(status_code=404, detail="No hay asignaciones")
            payload = [
                {'id_asignacion': r[0], 'id_pqr': r[1], 'id_usuario': r[2], 'fecha_asignacion': r[3]}
                for r in result
            ]
            return {"resultado": jsonable_encoder(payload)}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()

    # =====================================================
    # ACTUALIZAR ASIGNACIÓN
    # =====================================================

    def update_asignacion_responsable(self, asignacion_responsable_id: int,
                                      asignacion_responsable: Asignacion_responsable):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE asignacion_responsable
                SET id_pqr = %s, id_usuario = %s, fecha_asignacion = %s
                WHERE id_asignacion = %s
            """, (
                asignacion_responsable.id_pqr,
                asignacion_responsable.id_usuario,
                asignacion_responsable.fecha_asignacion,
                asignacion_responsable_id
            ))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Asignacion no encontrada")
            return {"resultado": "Asignacion_responsable actualizado"}
        except HTTPException:
            raise
        except Exception as e:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()

    # =====================================================
    # ELIMINAR ASIGNACIÓN
    # =====================================================

    def delete_asignacion_responsable(self, asignacion_responsable_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM asignacion_responsable WHERE id_asignacion = %s",
                (asignacion_responsable_id,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Asignacion no encontrada")
            return {"resultado": "Asignacion_responsable eliminado"}
        except HTTPException:
            raise
        except Exception as e:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()

    # =====================================================
    # ASIGNACIONES POR USUARIO
    # =====================================================

    def get_asignaciones_by_usuario(self, usuario_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM asignacion_responsable WHERE id_usuario = %s ORDER BY fecha_asignacion DESC",
                (usuario_id,)
            )
            result = cursor.fetchall()
            if not result:
                raise HTTPException(status_code=404, detail="No hay asignaciones para este usuario")
            payload = [
                {'id_asignacion': r[0], 'id_pqr': r[1], 'id_usuario': r[2], 'fecha_asignacion': r[3]}
                for r in result
            ]
            return {"resultado": jsonable_encoder(payload)}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()

    # =====================================================
    # ASIGNACIÓN POR PQR
    # =====================================================

    def get_asignacion_by_pqr(self, pqr_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM asignacion_responsable WHERE id_pqr = %s",
                (pqr_id,)
            )
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="No hay asignacion para esta PQR")
            return jsonable_encoder({
                'id_asignacion': result[0], 'id_pqr': result[1],
                'id_usuario': result[2], 'fecha_asignacion': result[3]
            })
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()