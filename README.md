# Robô Trader Pessoal para MetaTrader 5

Este projeto é um sistema completo para automação de trades no mercado financeiro brasileiro (B3), utilizando a plataforma MetaTrader 5. O sistema é composto por um robô que opera ao vivo, um backtester para validar estratégias e uma interface gráfica (GUI) para fácil operação.

Este projeto foi desenvolvido com o auxílio do Gemini, IA do Google.

## Funcionalidades Principais

* **Interface Gráfica:** Software com interface amigável para inserir credenciais, iniciar e parar o robô, e acompanhar os logs em tempo real.
* **Robô de Trade (Live):** Conecta-se à conta MetaTrader 5 e executa uma estratégia de cruzamento de médias móveis, enviando ordens de compra e venda com stop loss e take profit definidos.
* **Backtester Profissional:** Utiliza a biblioteca `backtesting.py` para simular e validar a performance da estratégia em dados históricos, gerando estatísticas detalhadas e um gráfico interativo de resultados.
* **Código Modularizado:** O projeto é dividido em módulos claros para conexão, estratégia, execução, gerenciamento de risco e interface, facilitando a manutenção e a adição de novas funcionalidades.

## Tecnologias Utilizadas

* **Python 3**
* **MetaTrader 5**
* **Tkinter** para a Interface Gráfica
* Bibliotecas Python:
    * `MetaTrader5`
    * `pandas` e `pandas_ta`
    * `schedule`
    * `backtesting.py`

## Configuração do Ambiente

Siga os passos abaixo para configurar o ambiente e executar o projeto.

1.  **Pré-requisitos:**
    * Python 3.9+ instalado.
    * Plataforma MetaTrader 5 instalada e com uma conta (demo ou real).
    * Git instalado.

2.  **Clonar o Repositório:**
    ```bash
    git clone [https://github.com/angelo-gatti-neto/robo-trader-python.git](https://github.com/angelo-gatti-neto/robo-trader-python.git)
    cd robo-trader-python
    ```

3.  **Criar e Ativar Ambiente Virtual:**
    ```bash
    # Criar
    py -m venv .venv
    # Ativar (Windows)
    .\.venv\Scripts\activate
    ```

4.  **Instalar as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuração do Robô

Antes de executar, você precisa configurar suas credenciais e parâmetros.

1.  No projeto, você encontrará um arquivo chamado `config.example.py`.
2.  Faça uma cópia deste arquivo e renomeie a cópia para `config.py`.
3.  Abra o `config.py` e preencha com suas credenciais do MetaTrader 5 e os parâmetros da estratégia que deseja usar. O arquivo `config.py` é ignorado pelo Git para proteger suas informações.

## Como Usar

### Executando o Robô com Interface Gráfica (Live Trading)
Para operar em tempo real (em conta demo ou real), execute o software principal:
```bash
python app.py