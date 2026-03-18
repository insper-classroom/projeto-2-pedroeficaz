import pytest
from unittest.mock import patch, MagicMock
from api import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# GET /imoveis

@patch("api.conectar_banco")
def test_listar_imoveis_vazio(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    mock_conectar_banco.return_value = mock_conn

    resp = client.get("/imoveis")

    assert resp.status_code == 200
    assert resp.get_json() == []

    mock_cursor.execute.assert_called_once_with(
        "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis"
    )

    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("api.conectar_banco")
def test_listar_imoveis_com_dados(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, "Rua A", "Rua", "Centro", "SP", "12345", "casa", 500000, "2020-01-01"),
        (2, "Rua B", "Avenida", "Zona Sul", "RJ", "22222", "apartamento", 600000, "2021-02-02"),
    ]

    mock_conectar_banco.return_value = mock_conn

    resp = client.get("/imoveis")

    assert resp.status_code == 200
    assert resp.get_json() == [
        {
            "id": 1,
            "logradouro": "Rua A",
            "tipo_logradouro": "Rua",
            "bairro": "Centro",
            "cidade": "SP",
            "cep": "12345",
            "tipo": "casa",
            "valor": 500000,
            "data_aquisicao": "2020-01-01"
        },
        {
            "id": 2,
            "logradouro": "Rua B",
            "tipo_logradouro": "Avenida",
            "bairro": "Zona Sul",
            "cidade": "RJ",
            "cep": "22222",
            "tipo": "apartamento",
            "valor": 600000,
            "data_aquisicao": "2021-02-02"
        },
    ]

    mock_cursor.execute.assert_called_once_with(
        "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis"
    )
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# GET /imoveis?tipo=

@patch("api.conectar_banco")
def test_filtrar_por_tipo(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, "Rua A", "Rua", "Centro", "SP", "12345", "casa", 500000, "2020-01-01"),
    ]

    mock_conectar_banco.return_value = mock_conn

    resp = client.get("/imoveis?tipo=casa")

    assert resp.status_code == 200
    assert resp.get_json() == [
    {
        "id": 1,
        "logradouro": "Rua A",
        "tipo_logradouro": "Rua",
        "bairro": "Centro",
        "cidade": "SP",
        "cep": "12345",
        "tipo": "casa",
        "valor": 500000,
        "data_aquisicao": "2020-01-01"
    }
    ]

    mock_cursor.execute.assert_called_once_with(
        "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis WHERE tipo = %s",
        ("casa",)
    )
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# GET /imoveis?cidade=
@patch("api.conectar_banco")
def test_filtrar_por_cidade(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (2, "Rua B", "Avenida", "Copacabana", "RJ", "22222", "apartamento", 600000, "2021-02-02"),
    ]

    mock_conectar_banco.return_value = mock_conn

    resp = client.get("/imoveis?cidade=RJ")

    assert resp.status_code == 200
    assert resp.get_json() == [
    {
        "id": 2,
        "logradouro": "Rua B",
        "tipo_logradouro": "Avenida",
        "bairro": "Copacabana",
        "cidade": "RJ",
        "cep": "22222",
        "tipo": "apartamento",
        "valor": 600000,
        "data_aquisicao": "2021-02-02"
    }
    ]

    mock_cursor.execute.assert_called_once_with(
        "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis WHERE cidade = %s",
        ("RJ",)
    )
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# POST /imoveis

@patch("api.conectar_banco")
def test_criar_imovel_ok(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.lastrowid = 10

    mock_conectar_banco.return_value = mock_conn

    payload = {
        "logradouro": "Rua Nova",
        "tipo_logradouro": "Rua",
        "bairro": "Centro",
        "cidade": "SP",
        "cep": "99999",
        "tipo": "casa",
        "valor": 400000,
        "data_aquisicao": "2022-01-01"
    }

    resp = client.post("/imoveis", json=payload)

    assert resp.status_code == 201
    assert resp.get_json() == {"id": 10}

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        ("Rua Nova", "Rua", "Centro", "SP", "99999", "casa", 400000, "2022-01-01")
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("api.conectar_banco")
def test_criar_imovel_erro_validacao(mock_conectar_banco, client):
    resp = client.post("/imoveis", json={"cidade": "SP"})

    assert resp.status_code == 400
    assert resp.get_json() == {"erro": "Campos obrigatórios: logradouro, cidade"}

    mock_conectar_banco.assert_not_called()


# GET /imoveis/<id>

@patch("api.conectar_banco")
def test_obter_imovel_ok(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (
        1, "Rua A", "Rua", "Centro", "SP", "12345", "casa", 500000, "2020-01-01"
    )

    mock_conectar_banco.return_value = mock_conn

    resp = client.get("/imoveis/1")

    assert resp.status_code == 200
    assert resp.get_json() == {
    "id": 1,
    "logradouro": "Rua A",
    "tipo_logradouro": "Rua",
    "bairro": "Centro",
    "cidade": "SP",
    "cep": "12345",
    "tipo": "casa",
    "valor": 500000,
    "data_aquisicao": "2020-01-01",
}

    mock_cursor.execute.assert_called_once_with(
        "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis WHERE id = %s",
        (1,)
    )
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("api.conectar_banco")
def test_obter_imovel_not_found(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    mock_conectar_banco.return_value = mock_conn

    resp = client.get("/imoveis/999")

    assert resp.status_code == 404
    assert resp.get_json() == {"erro": "Imóvel não encontrado"}

    mock_cursor.execute.assert_called_once_with(
        "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis WHERE id = %s",
        (999,)
    )
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# PUT /imoveis/<id>

@patch("api.conectar_banco")
def test_atualizar_imovel_ok(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    mock_conectar_banco.return_value = mock_conn

    payload = {
        "logradouro": "Rua Atualizada",
        "tipo_logradouro": "Rua",
        "bairro": "Centro",
        "cidade": "SP",
        "cep": "12345",
        "tipo": "casa",
        "valor": 550000,
        "data_aquisicao": "2023-01-01"
    }

    resp = client.put("/imoveis/1", json=payload)

    assert resp.status_code == 200
    assert resp.get_json() == {"mensagem": "Imóvel atualizado com sucesso"}

    mock_cursor.execute.assert_called_once_with(
        "UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s",
        ("Rua Atualizada", "Rua", "Centro", "SP", "12345", "casa", 550000, "2023-01-01", 1)
    )
    mock_conn.commit.assert_called_once()


@patch("api.conectar_banco")
def test_atualizar_imovel_not_found(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0

    mock_conectar_banco.return_value = mock_conn

    payload = {
        "logradouro": "Rua Atualizada",
        "tipo_logradouro": "Rua",
        "bairro": "Centro",
        "cidade": "SP",
        "cep": "12345",
        "tipo": "casa",
        "valor": 550000,
        "data_aquisicao": "2023-01-01"
    }

    resp = client.put("/imoveis/999", json=payload)

    assert resp.status_code == 404
    assert resp.get_json() == {"erro": "Imóvel não encontrado"}

    mock_conn.commit.assert_called_once()


@patch("api.conectar_banco")
def test_atualizar_imovel_erro_validacao(mock_conectar_banco, client):
    resp = client.put("/imoveis/1", json={"logradouro": "Rua"})

    assert resp.status_code == 400
    assert resp.get_json() == {"erro": "Campos obrigatórios: logradouro, cidade"}

    mock_conectar_banco.assert_not_called()


# DELETE /imoveis/<id>

@patch("api.conectar_banco")
def test_deletar_imovel_ok(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    mock_conectar_banco.return_value = mock_conn

    resp = client.delete("/imoveis/1")

    assert resp.status_code == 200
    assert resp.get_json() == {"mensagem": "Imóvel removido com sucesso"}

    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM imoveis WHERE id = %s",
        (1,)
    )
    mock_conn.commit.assert_called_once()


@patch("api.conectar_banco")
def test_deletar_imovel_not_found(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0

    mock_conectar_banco.return_value = mock_conn

    resp = client.delete("/imoveis/999")

    assert resp.status_code == 404
    assert resp.get_json() == {"erro": "Imóvel não encontrado"}

    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM imoveis WHERE id = %s",
        (999,)
    )
    mock_conn.commit.assert_called_once()