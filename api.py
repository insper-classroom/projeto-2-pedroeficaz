from flask import Flask, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()

app = Flask(__name__)


def conectar_banco():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            ssl_ca=os.getenv("SSL_CA_PATH")
        )
    except Error as err:
        raise Exception("Erro ao conectar ao banco")

    


@app.route("/imoveis", methods=["GET"])
def listar_imoveis():
    conn = conectar_banco()
    cursor = conn.cursor()

    tipo = request.args.get("tipo")
    cidade = request.args.get("cidade")

    if tipo:
        cursor.execute(
            "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis WHERE tipo = %s",
            (tipo,)
        )

    elif cidade:
        cursor.execute(
            "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis WHERE cidade = %s",
            (cidade,)
        )

    else:
        cursor.execute(
            "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis"
        )

    rows = cursor.fetchall()

    imoveis = [
        {
            "id": row[0],
            "logradouro": row[1],
            "tipo_logradouro": row[2],
            "bairro": row[3],
            "cidade": row[4],
            "cep": row[5],
            "tipo": row[6],
            "valor": row[7],
            "data_aquisicao": row[8].strftime("%Y-%m-%d") if hasattr(row[8], "strftime") else row[8],
        }
        for row in rows
    ]

    cursor.close()
    conn.close()

    return jsonify(imoveis), 200



@app.route("/imoveis", methods=["POST"])
def criar_imovel():
    data = request.json or {}

    if "logradouro" not in data or "cidade" not in data:
        return jsonify({"erro": "Campos obrigatórios: logradouro, cidade"}), 400

    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (
            data.get("logradouro"),
            data.get("tipo_logradouro"),
            data.get("bairro"),
            data.get("cidade"),
            data.get("cep"),
            data.get("tipo"),
            data.get("valor"),
            data.get("data_aquisicao"),
        )
    )

    conn.commit()
    new_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({"id": new_id}), 201




@app.route("/imoveis/<int:id>", methods=["GET"])
def obter_imovel(id):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis WHERE id = %s",
        (id,)
    )

    row = cursor.fetchone()

    if not row:
        cursor.close()
        conn.close()
        return jsonify({"erro": "Imóvel não encontrado"}), 404

    imovel = {
        "id": row[0],
        "logradouro": row[1],
        "tipo_logradouro": row[2],
        "bairro": row[3],
        "cidade": row[4],
        "cep": row[5],
        "tipo": row[6],
        "valor": row[7],
        "data_aquisicao": row[8].strftime("%Y-%m-%d") if hasattr(row[8], "strftime") else row[8],
    }

    cursor.close()
    conn.close()

    return jsonify(imovel), 200


@app.route("/imoveis/<int:id>", methods=["PUT"])
def atualizar_imovel(id):
    data = request.json or {}

    if "logradouro" not in data or "cidade" not in data:
        return jsonify({"erro": "Campos obrigatórios: logradouro, cidade"}), 400

    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s",
        (
            data.get("logradouro"),
            data.get("tipo_logradouro"),
            data.get("bairro"),
            data.get("cidade"),
            data.get("cep"),
            data.get("tipo"),
            data.get("valor"),
            data.get("data_aquisicao"),
            id
        )
    )

    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"erro": "Imóvel não encontrado"}), 404

    cursor.close()
    conn.close()

    return jsonify({"mensagem": "Imóvel atualizado com sucesso"}), 200



@app.route("/imoveis/<int:id>", methods=["DELETE"])
def deletar_imovel(id):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM imoveis WHERE id = %s",
        (id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"erro": "Imóvel não encontrado"}), 404

    cursor.close()
    conn.close()

    return jsonify({"mensagem": "Imóvel removido com sucesso"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)