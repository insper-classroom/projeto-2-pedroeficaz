from flask import Flask, jsonify, request

app = Flask(__name__)


def conectar_banco():
    pass


@app.route("/imoveis", methods=["GET"])
def listar_imoveis():
    conn = conectar_banco()
    cursor = conn.cursor()

    tipo = request.args.get("tipo")
    cidade = request.args.get("cidade")

    if tipo:
        cursor.execute(
            "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis WHERE tipo = ?",
            (tipo,)
        )

    elif cidade:
        cursor.execute(
            "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis WHERE cidade = ?",
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
            "data_aquisicao": row[8],
        }
        for row in rows
    ]

    cursor.close()
    conn.close()

    return jsonify(imoveis), 200