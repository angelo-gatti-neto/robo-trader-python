# risk_manager.py

import MetaTrader5 as mt5
import config

def calculate_stops(ativo, signal):
    """Calcula os preços de Stop Loss e Take Profit."""
    
    symbol_info = mt5.symbol_info(ativo)
    if symbol_info is None:
        print(f"Não foi possível encontrar informações para o ativo {ativo}")
        return None, None
        
    # O valor de 1 ponto para o ativo. Essencial para o cálculo.
    point = symbol_info.point
    
    # Pega o preço atual para definir os stops
    tick = mt5.symbol_info_tick(ativo)
    if tick is None:
        print(f"Não foi possível obter o tick atual para {ativo}")
        return None, None

    price = tick.ask if signal == "COMPRAR" else tick.bid
    
    stop_loss = 0
    take_profit = 0

    if signal == "COMPRAR":
        stop_loss = price - (config.RISK_POINTS_STOP_LOSS * point)
        take_profit = price + (config.RISK_POINTS_TAKE_PROFIT * point)
    elif signal == "VENDER":
        stop_loss = price + (config.RISK_POINTS_STOP_LOSS * point)
        take_profit = price - (config.RISK_POINTS_TAKE_PROFIT * point)
    
    print(f"Preços Calculados -> SL: {stop_loss:.2f}, TP: {take_profit:.2f}")
    return stop_loss, take_profit