# strategy.py (versão aprimorada com detecção de cruzamento)

import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ta
import config

TIMEFRAME_MAP = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
}

def get_market_data(ativo, timeframe, n_candles=100):
    mt5_timeframe = TIMEFRAME_MAP.get(timeframe, mt5.TIMEFRAME_M1)
    rates = mt5.copy_rates_from_pos(ativo, mt5_timeframe, 0, n_candles)
    
    if rates is None or len(rates) == 0:
        print(f"Não foi possível obter dados para {ativo}")
        return None
        
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def calculate_indicators(df):
    df.ta.ema(length=config.MEDIA_CURTA, append=True)
    df.ta.ema(length=config.MEDIA_LONGA, append=True)
    return df

def check_signal(df):
    """
    Verifica se houve um CRUZAMENTO de médias no último candle fechado.
    """
    # Precisamos de pelo menos 3 candles para comparar o anterior com o penúltimo
    if df is None or len(df) < config.MEDIA_LONGA + 2:
        return "AGUARDAR"

    # Pega os dois últimos candles fechados para detectar o cruzamento
    ultimo_fechado = df.iloc[-2]
    anterior_ao_ultimo = df.iloc[-3]

    # Nomes das colunas das médias
    media_curta_col = f'EMA_{config.MEDIA_CURTA}'
    media_longa_col = f'EMA_{config.MEDIA_LONGA}'

    # Verifica se as colunas existem e não contêm NaN (Not a Number)
    if media_curta_col not in df.columns or media_longa_col not in df.columns or \
       pd.isna(ultimo_fechado[media_curta_col]) or pd.isna(ultimo_fechado[media_longa_col]) or \
       pd.isna(anterior_ao_ultimo[media_curta_col]) or pd.isna(anterior_ao_ultimo[media_longa_col]):
        return "AGUARDAR"

    # --- LÓGICA DO CRUZAMENTO ---
    # Sinal de COMPRA: A média curta cruzou PARA CIMA da média longa
    if ultimo_fechado[media_curta_col] > ultimo_fechado[media_longa_col] and \
       anterior_ao_ultimo[media_curta_col] <= anterior_ao_ultimo[media_longa_col]:
        print(f"CRUZAMENTO PARA CIMA DETECTADO!")
        return "COMPRAR"

    # Sinal de VENDA: A média curta cruzou PARA BAIXO da média longa
    elif ultimo_fechado[media_curta_col] < ultimo_fechado[media_longa_col] and \
         anterior_ao_ultimo[media_curta_col] >= anterior_ao_ultimo[media_longa_col]:
        print(f"CRUZAMENTO PARA BAIXO DETECTADO!")
        return "VENDER"
        
    else:
        return "AGUARDAR"