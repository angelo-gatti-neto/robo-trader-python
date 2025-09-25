# connection.py

import MetaTrader5 as mt5
import config

def initialize_mt5():
    """Tenta conectar ao MetaTrader 5."""
    print("Iniciando conexão com o MetaTrader 5...")
    if not mt5.initialize(login=config.MT5_LOGIN, password=config.MT5_PASSWORD, server=config.MT5_SERVER):
        print(f"Falha na inicialização do MT5, erro: {mt5.last_error()}")
        mt5.shutdown()
        return False
    
    print("Conexão com o MetaTrader 5 estabelecida com sucesso!")
    return True

def shutdown_mt5():
    """Encerra a conexão com o MetaTrader 5."""
    print("Encerrando conexão com o MetaTrader 5.")
    mt5.shutdown()