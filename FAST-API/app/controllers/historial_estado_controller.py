import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from fastapi.encoders import jsonable_encoder
from models.historial_estado_model import Historial_estado

# CREATE
def create_historial_estado(self, historial_estado: Historial_estado):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO historial_estado (fecha, id_pqr, id_estado)
            VALUES (%s, %s, %s)
            RETURNING id_historial
        """, (
            historial_estado.fecha,
            historial_estado.id_pqr,
            historial_estado.id_estado
        ))

        new_id = cursor.fetchone()[0]
        conn.commit()

        return {
            "resultado": "Historial creado correctamente",
            "id_historial": new_id
        }

    except psycopg2.Error as err:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(err))

    finally:
        if conn:
            conn.close()


# GET BY ID
def get_historial_estado(self, historial_estado_id: int):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM historial_estado WHERE id_historial = %s",
            (historial_estado_id,)
        )

        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Historial no encontrado")

        content = {
            "id_historial": result[0],
            "fecha": result[1],
            "id_pqr": result[2],
            "id_estado": result[3]
        }

        return jsonable_encoder(content)

    except psycopg2.Error as err:
        raise HTTPException(status_code=500, detail=str(err))

    finally:
        if conn:
            conn.close()


# GET ALL
def get_historial_estados(self):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM historial_estado")
        results = cursor.fetchall()

        if not results:
            raise HTTPException(status_code=404, detail="No hay registros")

        payload = []

        for row in results:
            payload.append({
                "id_historial": row[0],
                "fecha": row[1],
                "id_pqr": row[2],
                "id_estado": row[3]
            })

        return {"resultado": jsonable_encoder(payload)}

    except psycopg2.Error as err:
        raise HTTPException(status_code=500, detail=str(err))

    finally:
        if conn:
            conn.close()


# UPDATE
def update_historial_estado(self, historial_estado_id: int, historial_estado: Historial_estado):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE historial_estado
            SET fecha = %s,
                id_pqr = %s,
                id_estado = %s
            WHERE id_historial = %s
        """, (
            historial_estado.fecha,
            historial_estado.id_pqr,
            historial_estado.id_estado,
            historial_estado_id
        ))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Historial no encontrado")

        conn.commit()

        return {"resultado": "Historial actualizado correctamente"}

    except psycopg2.Error as err:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(err))

    finally:
        if conn:
            conn.close()


# DELETE
def delete_historial_estado(self, historial_estado_id: int):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM historial_estado WHERE id_historial = %s",
            (historial_estado_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Historial no encontrado")

        conn.commit()

        return {"resultado": "Historial eliminado correctamente"}

    except psycopg2.Error as err:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(err))

    finally:
        if conn:
            conn.close()