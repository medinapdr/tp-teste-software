import argparse
from gerador_senha import ConfiguracaoSenha, gerar_senha

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Gerador de Senhas Seguras")
    parser.add_argument("-c", "--comprimento", type=int, default=12, help="Comprimento da senha (padrão: 12)")
    parser.add_argument("--maiusculas", action="store_true", help="Incluir letras maiúsculas")
    parser.add_argument("--minusculas", action="store_true", help="Incluir letras minúsculas")
    parser.add_argument("--numeros", action="store_true", help="Incluir números")
    parser.add_argument("--simbolos", action="store_true", help="Incluir símbolos padrão")
    parser.add_argument("--simbolos_custom", type=str, help="String de símbolos personalizados para usar")
    parser.add_argument("--texto_necessario", type=str, help="String de texto que deve estar na senha")

    args = parser.parse_args()

    if not (args.maiusculas or args.minusculas or args.numeros or args.simbolos):
        print("Aviso: Nenhum tipo de caractere foi explicitamente solicitado. Usando minúsculas por padrão.")
        if not args.maiusculas and not args.minusculas and not args.numeros and not args.simbolos:
            args.minusculas = True
    try:
        config = ConfiguracaoSenha(
            comprimento=args.comprimento,
            incluir_maiusculas=args.maiusculas,
            incluir_minusculas=args.minusculas,
            incluir_numeros=args.numeros,
            incluir_simbolos=args.simbolos,
            simbolos_personalizados=args.simbolos_custom,
            texto_necessario=args.texto_necessario
        )
        senha_gerada = gerar_senha(config)
        print("Senha Gerada:", senha_gerada)
    except ValueError as e:
        print(f"Erro ao gerar senha: {e}")
        exit(1)