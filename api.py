from flask import Flask, jsonify

app = Flask(__name__)


def conectar_banco():
    pass


@app.route("/imoveis", methods=["GET"])
def listar_imoveis():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis"
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify([]), 200