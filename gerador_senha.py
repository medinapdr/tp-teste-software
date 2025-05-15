import secrets
import string
import random

class ConfiguracaoSenha:
    def __init__(self,
                 comprimento: int,
                 incluir_maiusculas: bool = False,
                 incluir_minusculas: bool = False,
                 incluir_numeros: bool = False,
                 incluir_simbolos: bool = False,
                 simbolos_personalizados: str | None = None):
        self.comprimento = comprimento
        self.incluir_maiusculas = incluir_maiusculas
        self.incluir_minusculas = incluir_minusculas
        self.incluir_numeros = incluir_numeros
        self.incluir_simbolos = incluir_simbolos
        self.simbolos_personalizados = simbolos_personalizados

        if self.comprimento <= 0:
            raise ValueError("O comprimento da senha deve ser positivo.")

        if not (self.incluir_maiusculas or self.incluir_minusculas or \
                self.incluir_numeros or self.incluir_simbolos):
            raise ValueError("Pelo menos um tipo de caractere deve ser selecionado.")

CARACTERES_MINUSCULOS = string.ascii_lowercase
CARACTERES_MAIUSCULOS = string.ascii_uppercase
CARACTERES_NUMERICOS = string.digits
CARACTERES_SIMBOLOS_PADRAO = "!@#$%^&*()-_=+[]{}|;:,.<>/?"

def gerar_senha(config: ConfiguracaoSenha) -> str:
    conjunto_caracteres_permitidos = []
    caracteres_garantidos = []

    if config.incluir_minusculas:
        conjunto_caracteres_permitidos.extend(list(CARACTERES_MINUSCULOS))
        caracteres_garantidos.append(secrets.choice(CARACTERES_MINUSCULOS))

    if config.incluir_maiusculas:
        conjunto_caracteres_permitidos.extend(list(CARACTERES_MAIUSCULOS))
        caracteres_garantidos.append(secrets.choice(CARACTERES_MAIUSCULOS))

    if config.incluir_numeros:
        conjunto_caracteres_permitidos.extend(list(CARACTERES_NUMERICOS))
        caracteres_garantidos.append(secrets.choice(CARACTERES_NUMERICOS))

    simbolos_a_usar = CARACTERES_SIMBOLOS_PADRAO
    if config.simbolos_personalizados is not None:
        simbolos_a_usar = config.simbolos_personalizados
    
    if config.incluir_simbolos:
        if not simbolos_a_usar:
             pass
        else:
            conjunto_caracteres_permitidos.extend(list(simbolos_a_usar))
            caracteres_garantidos.append(secrets.choice(simbolos_a_usar))
            
    if not conjunto_caracteres_permitidos:
        raise ValueError("O conjunto de caracteres permitidos está vazio. Certifique-se de que pelo menos um tipo de caractere está selecionado e o conjunto de símbolos é válido.")

    if len(caracteres_garantidos) > config.comprimento:
        raise ValueError(
            f"Não é possível garantir todos os tipos de caracteres selecionados com o comprimento fornecido. "
            f"São necessários pelo menos {len(caracteres_garantidos)} caracteres, mas o comprimento é {config.comprimento}."
        )

    comprimento_restante = config.comprimento - len(caracteres_garantidos)
    
    if not conjunto_caracteres_permitidos and comprimento_restante > 0 :
         raise ValueError("O conjunto de caracteres permitidos está vazio, não é possível preencher o restante do comprimento da senha.")

    caracteres_senha = list(caracteres_garantidos)
    if conjunto_caracteres_permitidos:
        for _ in range(comprimento_restante):
            caracteres_senha.append(secrets.choice(conjunto_caracteres_permitidos))
    elif comprimento_restante > 0:
        raise ValueError("Não é possível gerar a senha: o conjunto de caracteres permitidos ficou vazio enquanto caracteres ainda eram necessários.")

    random.shuffle(caracteres_senha)

    return "".join(caracteres_senha)