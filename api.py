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



@app.route("/imoveis", methods=["POST"])
def criar_imovel():
    data = request.json or {}

    if "logradouro" not in data or "cidade" not in data:
        return jsonify({"erro": "Campos obrigatórios: logradouro, cidade"}), 400

    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
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
        "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis WHERE id = ?",
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
        "data_aquisicao": row[8],
    }

    cursor.close()
    conn.close()

    return jsonify(imovel), 200


@app.route("/imoveis/<int:id>", methods=["PUT"])
def atualizar_imovel(id):
    data = request.json or {}

    # validação mínima
    if "logradouro" not in data or "cidade" not in data:
        return jsonify({"erro": "Campos obrigatórios: logradouro, cidade"}), 400

    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE imoveis SET logradouro = ?, tipo_logradouro = ?, bairro = ?, cidade = ?, cep = ?, tipo = ?, valor = ?, data_aquisicao = ? WHERE id = ?",
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