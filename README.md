# Gerador de Senhas em Python

Este projeto consiste em um gerador de senhas desenvolvido em Python como parte do Trabalho Prático da disciplina de Teste de Software. O objetivo é criar uma ferramenta robusta e configurável para a geração de senhas seguras, com foco em boas práticas de desenvolvimento, testes automatizados e integração contínua.

## 1. Membros do Grupo

* Pedro Medina
* Fábio Marra
* Gustavo Cunha

## 2. Explicação do Sistema

O sistema é um gerador de senhas que permite ao usuário criar senhas complexas com base em um conjunto de critérios personalizáveis. As principais funcionalidades incluem:

* **Geração Configurável:** Permite especificar o comprimento desejado para a senha.
* **Seleção de Tipos de Caracteres:** O usuário pode escolher incluir:
    * Letras minúsculas (`a-z`)
    * Letras maiúsculas (`A-Z`)
    * Números (`0-9`)
    * Símbolos (conjunto padrão como `!@#$%^&*()` ou um conjunto personalizado fornecido pelo usuário).
* **Garantia de Complexidade:** A lógica de geração assegura que, se um tipo de caractere for solicitado, pelo menos um caractere desse tipo estará presente na senha final (desde que o comprimento da senha permita).
* **Segurança:** Utiliza o módulo `secrets` do Python para a geração de caracteres aleatórios, que é adequado para fins criptográficos, tornando as senhas menos previsíveis.
* **Modularidade:** O código foi estruturado pensando em futuras expansões, como a integração com APIs externas (ex: `zxcvbn` para análise de força da senha) ou a implementação de regras de complexidade mais avançadas (ex: número mínimo de cada tipo de caractere).
* **Foco em Testes:** O projeto possui uma suíte de testes unitários abrangente para garantir a corretude das funcionalidades e alta cobertura de código.

## 3. Tecnologias Utilizadas

Para o desenvolvimento e a manutenção deste projeto, foram empregadas as seguintes tecnologias e ferramentas:

* **Linguagem de Programação:**
    * **Python:** Versão 3.9 ou superior. A linguagem foi escolhida por sua clareza, vasta biblioteca padrão e forte ecossistema para desenvolvimento e testes.

* **Módulos Python Principais:**
    * **`secrets`**: Utilizado para a geração de números e escolhas aleatórias criptograficamente seguras, essencial para a criação de senhas robustas.
    * **`string`**: Fornece constantes úteis com conjuntos de caracteres comuns (letras minúsculas, maiúsculas, dígitos).
    * **`random`**: Especificamente a função `shuffle` para embaralhar os caracteres da senha gerada, aumentando sua aleatoriedade.

* **Testes Automatizados:**
    * **`pytest`**: Framework de testes utilizado para escrever e executar os testes unitários de forma eficiente e expressiva.
    * **`pytest-cov`**: Plugin do `pytest` para medir a cobertura de código dos testes, ajudando a identificar partes do código não testadas.

* **Integração Contínua e Cobertura de Código Online:**
    * **GitHub Actions**: Plataforma de CI/CD utilizada para automatizar a execução dos testes e o processo de verificação de cobertura a cada push ou pull request.
    * **Codecov**: Ferramenta integrada ao workflow do GitHub Actions para analisar, visualizar e acompanhar a cobertura de código do projeto ao longo do tempo.

* **Gerenciamento de Dependências:**
    * **PIP**: O instalador de pacotes padrão do Python.
    * **`requirements.txt`**: Arquivo utilizado para listar as dependências do projeto (neste caso, `pytest` e `pytest-cov` para o ambiente de desenvolvimento e teste).
