# connection.py

import MetaTrader5 as mt5

def initialize_mt5(login, password, server):
    """Tenta conectar ao MetaTrader 5 usando as credenciais fornecidas."""
    print(f"Iniciando conexão com o MetaTrader 5...\n")
    # Usa as variáveis recebidas como argumento
    if not mt5.initialize(login=login, password=password, server=server):
        print(f"Falha na inicialização do MT5, erro: {mt5.last_error()}\n")
        mt5.shutdown()
        return False
    
    print("Conexão com o MetaTrader 5 estabelecida com sucesso!\n")
    return True

def shutdown_mt5():
    """Encerra a conexão com o MetaTrader 5."""
    print("Encerrando conexão com o MetaTrader 5.\n")
    mt5.shutdown()