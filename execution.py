# execution.py

import MetaTrader5 as mt5
import config

def send_order(ativo, volume, signal, stop_loss, take_profit):
    """Monta e envia uma ordem de mercado."""

    order_type = mt5.ORDER_TYPE_BUY if signal == "COMPRAR" else mt5.ORDER_TYPE_SELL
    
    price = mt5.symbol_info_tick(ativo).ask if signal == "COMPRAR" else mt5.symbol_info_tick(ativo).bid

    # Dicionário da requisição de ordem
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": ativo,
        "volume": volume,
        "type": order_type,
        "price": price,
        "sl": stop_loss,
        "tp": take_profit,
        "magic": 202409,  # Número mágico para identificar as ordens do nosso robô
        "comment": "Ordem enviada pelo Robô Cohen",
        "type_time": mt5.ORDER_TIME_GTC, # A ordem fica válida até ser cancelada
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }

    # Envia a ordem para a corretora
    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"!!! Falha ao enviar ordem: retcode={result.retcode}, comment={result.comment}")
        return False
    
    print(f"+++ Ordem enviada com sucesso: Ticket #{result.order}")
    return True