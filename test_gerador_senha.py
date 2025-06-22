import pytest
import random
import requests
from zxcvbn import zxcvbn
import subprocess
import sys
import tempfile
import json
from gerador_senha import (
    ConfiguracaoSenha,
    gerar_senha,
    CARACTERES_MINUSCULOS,
    CARACTERES_MAIUSCULOS,
    CARACTERES_NUMERICOS,
    CARACTERES_SIMBOLOS_PADRAO
)

def contem_algum(texto, conjunto_chars):
    return any(c in conjunto_chars for c in texto)

def contem_apenas(texto, conjunto_chars_permitidos):
    return all(c in conjunto_chars_permitidos for c in texto)


def test_config_comprimento_invalido():
    with pytest.raises(ValueError, match="O comprimento da senha deve ser positivo."):
        ConfiguracaoSenha(comprimento=0)
    with pytest.raises(ValueError, match="O comprimento da senha deve ser positivo."):
        ConfiguracaoSenha(comprimento=-5)

def test_config_nenhum_tipo_char_selecionado():
    with pytest.raises(ValueError, match="Pelo menos um tipo de caractere deve ser selecionado."):
        ConfiguracaoSenha(comprimento=8)


def test_gerar_comprimento_muito_curto_para_garantidos():
    config = ConfiguracaoSenha(comprimento=2, incluir_minusculas=True, incluir_maiusculas=True, incluir_numeros=True)
    with pytest.raises(ValueError, match="Não é possível garantir todos os tipos de caracteres selecionados"):
        gerar_senha(config)

@pytest.mark.parametrize("comprimento", [1, 5, 8, 12, 16, 32, 64])
def test_gerar_senha_comprimento_correto(comprimento):
    config = ConfiguracaoSenha(comprimento=comprimento, incluir_minusculas=True)
    senha = gerar_senha(config)
    assert len(senha) == comprimento

def test_gerar_apenas_minusculas():
    config = ConfiguracaoSenha(comprimento=12, incluir_minusculas=True)
    senha = gerar_senha(config)
    assert contem_apenas(senha, CARACTERES_MINUSCULOS)
    assert contem_algum(senha, CARACTERES_MINUSCULOS)

def test_gerar_apenas_maiusculas():
    config = ConfiguracaoSenha(comprimento=12, incluir_maiusculas=True)
    senha = gerar_senha(config)
    assert contem_apenas(senha, CARACTERES_MAIUSCULOS)
    assert contem_algum(senha, CARACTERES_MAIUSCULOS)

def test_gerar_apenas_numeros():
    config = ConfiguracaoSenha(comprimento=12, incluir_numeros=True)
    senha = gerar_senha(config)
    assert contem_apenas(senha, CARACTERES_NUMERICOS)
    assert contem_algum(senha, CARACTERES_NUMERICOS)

def test_gerar_apenas_simbolos_padrao():
    config = ConfiguracaoSenha(comprimento=12, incluir_simbolos=True)
    senha = gerar_senha(config)
    assert contem_apenas(senha, CARACTERES_SIMBOLOS_PADRAO)
    assert contem_algum(senha, CARACTERES_SIMBOLOS_PADRAO)

def test_gerar_apenas_simbolos_personalizados():
    simbolos_pers = "@#$%"
    config = ConfiguracaoSenha(comprimento=12, incluir_simbolos=True, simbolos_personalizados=simbolos_pers)
    senha = gerar_senha(config)
    assert contem_apenas(senha, simbolos_pers)
    assert contem_algum(senha, simbolos_pers)

def test_gerar_simbolos_personalizados_vazios_com_incluir_simbolos_e_outro_tipo():
    config = ConfiguracaoSenha(comprimento=12, incluir_simbolos=True, simbolos_personalizados="", incluir_minusculas=True)
    senha = gerar_senha(config)
    assert not contem_algum(senha, CARACTERES_SIMBOLOS_PADRAO)
    assert contem_algum(senha, CARACTERES_MINUSCULOS)

def test_gerar_simbolos_personalizados_vazios_com_incluir_simbolos_apenas_tipo():
    config = ConfiguracaoSenha(comprimento=12, incluir_simbolos=True, simbolos_personalizados="")
    with pytest.raises(ValueError, match="O conjunto de caracteres permitidos está vazio"):
        gerar_senha(config)

def test_gerar_minusculas_e_numeros():
    config = ConfiguracaoSenha(comprimento=12, incluir_minusculas=True, incluir_numeros=True)
    senha = gerar_senha(config)
    conjunto_esperado = CARACTERES_MINUSCULOS + CARACTERES_NUMERICOS
    assert contem_apenas(senha, conjunto_esperado)
    assert contem_algum(senha, CARACTERES_MINUSCULOS)
    assert contem_algum(senha, CARACTERES_NUMERICOS)

def test_gerar_todos_tipos_char_simbolos_padrao():
    config = ConfiguracaoSenha(
        comprimento=16,
        incluir_minusculas=True,
        incluir_maiusculas=True,
        incluir_numeros=True,
        incluir_simbolos=True
    )
    senha = gerar_senha(config)
    conjunto_esperado = CARACTERES_MINUSCULOS + CARACTERES_MAIUSCULOS + CARACTERES_NUMERICOS + CARACTERES_SIMBOLOS_PADRAO
    assert contem_apenas(senha, conjunto_esperado)
    assert contem_algum(senha, CARACTERES_MINUSCULOS)
    assert contem_algum(senha, CARACTERES_MAIUSCULOS)
    assert contem_algum(senha, CARACTERES_NUMERICOS)
    assert contem_algum(senha, CARACTERES_SIMBOLOS_PADRAO)

def test_gerar_sem_maiusculas():
    config = ConfiguracaoSenha(comprimento=12, incluir_minusculas=True, incluir_numeros=True, incluir_simbolos=True, incluir_maiusculas=False)
    senha = gerar_senha(config)
    assert not contem_algum(senha, CARACTERES_MAIUSCULOS)

def test_gerar_sem_minusculas():
    config = ConfiguracaoSenha(comprimento=12, incluir_maiusculas=True, incluir_numeros=True, incluir_simbolos=True, incluir_minusculas=False)
    senha = gerar_senha(config)
    assert not contem_algum(senha, CARACTERES_MINUSCULOS)

def test_gerar_sem_numeros():
    config = ConfiguracaoSenha(comprimento=12, incluir_minusculas=True, incluir_maiusculas=True, incluir_simbolos=True, incluir_numeros=False)
    senha = gerar_senha(config)
    assert not contem_algum(senha, CARACTERES_NUMERICOS)

def test_gerar_sem_simbolos():
    config = ConfiguracaoSenha(comprimento=12, incluir_minusculas=True, incluir_maiusculas=True, incluir_numeros=True, incluir_simbolos=False)
    senha = gerar_senha(config)
    assert not contem_algum(senha, CARACTERES_SIMBOLOS_PADRAO)
    if config.simbolos_personalizados:
         assert not contem_algum(senha, config.simbolos_personalizados)

def test_gerar_senha_unicidade():
    config = ConfiguracaoSenha(comprimento=16, incluir_minusculas=True, incluir_maiusculas=True, incluir_numeros=True, incluir_simbolos=True)
    senhas = set()
    for _ in range(30):
        senha = gerar_senha(config)
        assert senha not in senhas
        senhas.add(senha)

@pytest.mark.parametrize("comprimento, minus, maius, num, simb, simb_pers, msg_erro_parcial", [
    (1, True, True, False, False, None, "Não é possível garantir"),
    (3, True, True, True, True, None, "Não é possível garantir"),
    (0, True, False, False, False, None, "O comprimento da senha deve ser positivo"),
    (8, False, False, False, False, None, "Pelo menos um tipo de caractere deve ser selecionado"),
])
def test_gerar_varias_configs_invalidas(comprimento, minus, maius, num, simb, simb_pers, msg_erro_parcial):
    with pytest.raises(ValueError, match=msg_erro_parcial):
        cfg = ConfiguracaoSenha(comprimento=comprimento, incluir_minusculas=minus, incluir_maiusculas=maius, incluir_numeros=num, incluir_simbolos=simb, simbolos_personalizados=simb_pers)
        if comprimento > 0 and (minus or maius or num or simb):
            gerar_senha(cfg)

def test_gerar_comprimento_1_todos_tipos_garantidos():
    config = ConfiguracaoSenha(comprimento=1, incluir_minusculas=True, incluir_maiusculas=True, incluir_numeros=True, incluir_simbolos=True)
    with pytest.raises(ValueError, match="Não é possível garantir"):
        gerar_senha(config)

def test_gerar_comprimento_1_um_tipo():
    config = ConfiguracaoSenha(comprimento=1, incluir_numeros=True)
    senha = gerar_senha(config)
    assert len(senha) == 1
    assert contem_apenas(senha, CARACTERES_NUMERICOS)

def test_gerar_comprimento_igual_tipos_garantidos():
    config = ConfiguracaoSenha(
        comprimento=4,
        incluir_minusculas=True,
        incluir_maiusculas=True,
        incluir_numeros=True,
        incluir_simbolos=True
    )
    senha = gerar_senha(config)
    assert len(senha) == 4
    assert contem_algum(senha, CARACTERES_MINUSCULOS)
    assert contem_algum(senha, CARACTERES_MAIUSCULOS)
    assert contem_algum(senha, CARACTERES_NUMERICOS)
    assert contem_algum(senha, CARACTERES_SIMBOLOS_PADRAO)
    assert len(set(senha)) <= 4

def test_gerar_senha_com_todas_opcoes_e_simbolos_personalizados():
    simbolos_pers = "~^"
    config = ConfiguracaoSenha(
        comprimento=20,
        incluir_minusculas=True,
        incluir_maiusculas=True,
        incluir_numeros=True,
        incluir_simbolos=True,
        simbolos_personalizados=simbolos_pers
    )
    senha = gerar_senha(config)
    assert len(senha) == config.comprimento
    assert contem_algum(senha, CARACTERES_MINUSCULOS)
    assert contem_algum(senha, CARACTERES_MAIUSCULOS)
    assert contem_algum(senha, CARACTERES_NUMERICOS)
    assert contem_algum(senha, simbolos_pers)
    assert not contem_algum(senha, CARACTERES_SIMBOLOS_PADRAO.replace("~","").replace("^",""))

@pytest.mark.parametrize("inc_min, inc_mai, inc_num, inc_simb, esp_min, esp_mai, esp_num, esp_simb", [
    (True, False, False, False, True, False, False, False),
    (False, True, False, False, False, True, False, False),
    (False, False, True, False, False, False, True, False),
    (False, False, False, True, False, False, False, True),
    (True, True, False, False, True, True, False, False),
    (True, True, True, True, True, True, True, True),
])
def test_presenca_caracteres_garantidos(inc_min, inc_mai, inc_num, inc_simb, esp_min, esp_mai, esp_num, esp_simb):
    comprimento = 10
    num_garantidos_esperados = sum([esp_min, esp_mai, esp_num, esp_simb])
    if num_garantidos_esperados == 0:
        pytest.skip("Pulando teste onde nenhum tipo de caractere é selecionado, pois a validação da config trata isso")
        return
    
    comprimento_teste = max(comprimento, num_garantidos_esperados)

    config = ConfiguracaoSenha(
        comprimento=comprimento_teste,
        incluir_minusculas=inc_min,
        incluir_maiusculas=inc_mai,
        incluir_numeros=inc_num,
        incluir_simbolos=inc_simb
    )
    
    senha_ok = False
    for _ in range(5):
        senha = gerar_senha(config)
        min_presente = contem_algum(senha, CARACTERES_MINUSCULOS) if esp_min else True
        mai_presente = contem_algum(senha, CARACTERES_MAIUSCULOS) if esp_mai else True
        num_presente = contem_algum(senha, CARACTERES_NUMERICOS) if esp_num else True
        simb_presente = contem_algum(senha, CARACTERES_SIMBOLOS_PADRAO) if esp_simb else True
        
        if min_presente and mai_presente and num_presente and simb_presente:
            senha_ok = True
            break
            
    assert senha_ok, f"A senha falhou em incluir todos os tipos de caracteres requeridos após múltiplas tentativas com config: {config.__dict__}"

def test_gerar_senha_conjunto_caracteres_vazio_durante_preenchimento():
    config_simbolos_apenas_pers_vazio = ConfiguracaoSenha(comprimento=5, incluir_simbolos=True, simbolos_personalizados="")
    with pytest.raises(ValueError, match="O conjunto de caracteres permitidos está vazio"):
         gerar_senha(config_simbolos_apenas_pers_vazio)

def test_comprimento_minimo_um_tipo():
    config = ConfiguracaoSenha(comprimento=1, incluir_numeros=True)
    senha = gerar_senha(config)
    assert len(senha) == 1
    assert contem_apenas(senha, CARACTERES_NUMERICOS)

def test_comprimento_minimo_dois_tipos():
    config = ConfiguracaoSenha(comprimento=2, incluir_numeros=True, incluir_minusculas=True)
    senha = gerar_senha(config)
    assert len(senha) == 2
    assert contem_algum(senha, CARACTERES_NUMERICOS)
    assert contem_algum(senha, CARACTERES_MINUSCULOS)
    assert contem_apenas(senha, CARACTERES_NUMERICOS + CARACTERES_MINUSCULOS)

def test_simbolos_personalizados_subconjunto_do_padrao():
    simbolos_pers = "!@"
    config = ConfiguracaoSenha(comprimento=10, incluir_simbolos=True, simbolos_personalizados=simbolos_pers, incluir_minusculas=True)
    senha = gerar_senha(config)
    assert contem_algum(senha, simbolos_pers)
    assert not contem_algum(senha, CARACTERES_SIMBOLOS_PADRAO.replace("!", "").replace("@", ""))

def test_comprimento_igual_numero_tipos_distintos_garantidos():
    config = ConfiguracaoSenha(comprimento=3, incluir_maiusculas=True, incluir_numeros=True, incluir_simbolos=True)
    senha = gerar_senha(config)
    assert len(senha) == 3
    assert contem_algum(senha, CARACTERES_MAIUSCULOS)
    assert contem_algum(senha, CARACTERES_NUMERICOS)
    assert contem_algum(senha, CARACTERES_SIMBOLOS_PADRAO)
    assert len(set(senha)) <= 3

def test_efetividade_embaralhamento_indiretamente():
    config = ConfiguracaoSenha(comprimento=10, incluir_minusculas=True, incluir_maiusculas=True, incluir_numeros=True, incluir_simbolos=True)
    
    primeiro_min = CARACTERES_MINUSCULOS[0]
    primeiro_mai = CARACTERES_MAIUSCULOS[0]
    primeiro_num = CARACTERES_NUMERICOS[0]
    primeiro_simb = CARACTERES_SIMBOLOS_PADRAO[0]
    
    padrao_inicial = f"{primeiro_min}{primeiro_mai}{primeiro_num}{primeiro_simb}"
    
    sempre_inicia_com_padrao = True
    for _ in range(20):
        senha = gerar_senha(config)
        if not senha.startswith(padrao_inicial[:4]):
            sempre_inicia_com_padrao = False
            break
            
    assert not sempre_inicia_com_padrao, "As senhas parecem sempre começar com o mesmo padrão de caracteres garantidos; o embaralhamento pode não estar eficaz."

def test_integracao_api_seed():
    #usa api random number para obter um inteiro x e gerar uma senha com o comprimento x
    response = requests.get("https://www.randomnumberapi.com/api/v1.0/random?min=12&max=32&count=1")
    assert response.status_code == 200

    comprimento = response.json()[0]
    config = ConfiguracaoSenha(
        comprimento=comprimento,
        incluir_minusculas=True,
        incluir_maiusculas=True,
        incluir_numeros=True
    )
    senha = gerar_senha(config)

    assert len(senha) == comprimento, f"A senha deve ter {comprimento} caracteres, mas teve {len(senha)}"


def test_integracao_zxcvbn_analise_forca():
    #usa zxcvbn para medir se a senha gerada possui força razoavel
    config = ConfiguracaoSenha(comprimento=20, incluir_minusculas=True, incluir_maiusculas=True, incluir_numeros=True, incluir_simbolos=True)
    senha = gerar_senha(config)

    resultado = zxcvbn(senha)
    score = resultado['score']

    assert score >= 3, f"A senha gerada deve ter uma força razoável (score >= 3). Score atual: {score}"

def test_cli_integracao_argumentos():
    #testa a integracao com argparse, i.e., passagem de parametros via linha de comando
    comando = [
        sys.executable, "main.py",
        "-c", "16",
        "--minusculas",
        "--maiusculas",
        "--numeros",
        "--simbolos"
    ]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    
    assert resultado.returncode == 0
    assert "Senha Gerada:" in resultado.stdout
    senha = resultado.stdout.strip().split(":")[-1].strip()
    assert len(senha) == 16

def test_integracao_arquivo_simbolos_personalizados():
    #testa integracao com filesystem, fazendo leitura de um arquivo com simbolos
    with tempfile.NamedTemporaryFile(mode='w+', delete=True) as temp_file:
        temp_file.write("★✪♛♜")
        temp_file.seek(0)
        simbolos = temp_file.read()

        config = ConfiguracaoSenha(comprimento=12, incluir_simbolos=True, simbolos_personalizados=simbolos)
        senha = gerar_senha(config)

        assert all(c in simbolos for c in senha)

def test_integracao_configuracao_por_json():
    #verifica integracao de parsing, validacao e geracao, atraves de especificacoes em um json
    dados_json = """
    {
        "comprimento": 14,
        "incluir_maiusculas": true,
        "incluir_minusculas": true,
        "incluir_numeros": false,
        "incluir_simbolos": true,
        "simbolos_personalizados": "#$&"
    }
    """
    config_dict = json.loads(dados_json)
    config = ConfiguracaoSenha(**config_dict)
    senha = gerar_senha(config)

    assert len(senha) == 14
    assert all(c in (config.simbolos_personalizados + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
               for c in senha)