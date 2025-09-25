# backtester.py (VERSÃO FINAL CORRIGIDA)

from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5
import config
import strategy

def run_backtest(ativo, timeframe, start_date, end_date):
    print(f"Iniciando backtest para {ativo} de {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}...")

    rates = mt5.copy_rates_range(ativo, strategy.TIMEFRAME_MAP[timeframe], start_date, end_date)
    if rates is None or len(rates) == 0:
        print("Não foi possível obter dados para o período.")
        return None
    
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df = strategy.calculate_indicators(df)
    
    trades = []
    position = None
    pnl_points = 0.0

    symbol_info = mt5.symbol_info(ativo)
    point = symbol_info.point

    media_curta_col = f'EMA_{config.MEDIA_CURTA}'
    media_longa_col = f'EMA_{config.MEDIA_LONGA}'

    for i in range(config.MEDIA_LONGA + 2, len(df)):
        current_candle = df.iloc[i]
        
        # --- LÓGICA DE SAÍDA ---
        if position is not None:
            exit_reason, exit_price = None, 0
            
            if position['type'] == 'BUY':
                if current_candle['low'] <= position['stop_loss']:
                    exit_reason, exit_price = "Stop Loss", position['stop_loss']
                elif current_candle['high'] >= position['take_profit']:
                    exit_reason, exit_price = "Take Profit", position['take_profit']
            
            elif position['type'] == 'SELL':
                if current_candle['high'] >= position['stop_loss']:
                    exit_reason, exit_price = "Stop Loss", position['stop_loss']
                elif current_candle['low'] <= position['take_profit']:
                    exit_reason, exit_price = "Take Profit", position['take_profit']
            
            if exit_reason:
                pnl = (exit_price - position['entry_price']) / point if position['type'] == 'BUY' else (position['entry_price'] - exit_price) / point
                pnl_points += pnl
                trades.append({'exit_time': current_candle['time'], 'exit_price': exit_price, 'pnl_points': pnl, 'reason': exit_reason})
                position = None

        # --- LÓGICA DE ENTRADA ---
        if position is None:
            # Comparamos as médias nos candles i-1 (último fechado) e i-2 (anterior)
            if df[media_curta_col][i-1] > df[media_longa_col][i-1] and df[media_curta_col][i-2] <= df[media_longa_col][i-2]:
                sinal = "COMPRAR"
            elif df[media_curta_col][i-1] < df[media_longa_col][i-1] and df[media_curta_col][i-2] >= df[media_longa_col][i-2]:
                sinal = "VENDER"
            else:
                sinal = "AGUARDAR"

            if sinal != "AGUARDAR":
                entry_price = df['open'][i]
                sl, tp = 0, 0
                if sinal == "COMPRAR":
                    sl = entry_price - (config.RISK_POINTS_STOP_LOSS * point)
                    tp = entry_price + (config.RISK_POINTS_TAKE_PROFIT * point)
                elif sinal == "VENDER":
                    sl = entry_price + (config.RISK_POINTS_STOP_LOSS * point)
                    tp = entry_price - (config.RISK_POINTS_TAKE_PROFIT * point)
                position = {'type': sinal, 'entry_time': df['time'][i], 'entry_price': entry_price, 'stop_loss': sl, 'take_profit': tp}

    # Contabiliza a última operação se ela ficou aberta
    if position is not None:
        last_candle = df.iloc[-1]
        pnl = (last_candle['close'] - position['entry_price']) / point if position['type'] == 'BUY' else (position['entry_price'] - last_candle['close']) / point
        pnl_points += pnl
        trades.append({'exit_time': last_candle['time'], 'exit_price': last_candle['close'], 'pnl_points': pnl, 'reason': 'Fim do Backtest'})

    total_trades = len(trades)
    wins = len([t for t in trades if t['pnl_points'] > 0])
    losses = total_trades - wins
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    
    return {"total_trades": total_trades, "wins": wins, "losses": losses, "win_rate_percent": win_rate, "total_pnl_points": pnl_points}