# backtester_pro.py (VERSÃO FINAL CORRIGIDA E PROFISSIONAL)

from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import MetaTrader5 as mt5
from datetime import datetime, timedelta
import pandas as pd
import config
import connection
import strategy as strat # Usaremos o strategy.py para pegar o timeframe

# Passo 1: Definir a Estratégia no formato que a biblioteca entende
class EmaCross(Strategy):
    # Parâmetros da estratégia que lemos do config.py
    n1 = config.MEDIA_CURTA
    n2 = config.MEDIA_LONGA
    n_tendencia = 200
    stop_loss_points = config.RISK_POINTS_STOP_LOSS
    take_profit_points = config.RISK_POINTS_TAKE_PROFIT

    def init(self):
        # Preparar os indicadores
        close = self.data.Close
        # A biblioteca `backtesting.py` tem sua própria forma de calcular indicadores
        # self.I() é a função para isso.
        self.ema1 = self.I(lambda x, n: pd.Series(x).ewm(span=n, adjust=False).mean(), close, self.n1)
        self.ema2 = self.I(lambda x, n: pd.Series(x).ewm(span=n, adjust=False).mean(), close, self.n2)
        self.ema_tendencia = self.I(lambda x, n: pd.Series(x).ewm(span=n, adjust=False).mean(), close, self.n_tendencia)

    def next(self):
        # Esta função roda a cada candle
        price = self.data.Close[-1]
        
        # Lógica de Compra: se a ema1 cruzar para cima da ema2
        # A função 'crossover' da biblioteca é robusta para detectar cruzamentos
        if crossover(self.ema1, self.ema2) and price > self.ema_tendencia[-1]:
            # Como point=1 para o mini-índice, o cálculo é direto
            sl = price - self.stop_loss_points
            tp = price + self.take_profit_points
            self.buy(sl=sl, tp=tp, size=1) # size=1 significa 1 contrato

        # Lógica de Venda: se a ema2 cruzar para cima da ema1
        elif crossover(self.ema2, self.ema1) and price < self.ema_tendencia[-1]:
            # Como point=1 para o mini-índice, o cálculo é direto
            sl = price + self.stop_loss_points
            tp = price - self.take_profit_points
            self.sell(sl=sl, tp=tp, size=1) # size=1 significa 1 contrato


if __name__ == "__main__":
    if connection.initialize_mt5():
        
        # Puxa os dados históricos
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        
        rates = mt5.copy_rates_range(config.ATIVO, strat.TIMEFRAME_MAP[config.TIMEFRAME], start_date, end_date)
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        
        # Renomeia as colunas para o padrão da biblioteca
        df.rename(columns={
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'tick_volume': 'Volume'
        }, inplace=True)

        # Configura e executa o backtest
        # Aumentamos o cash para um valor maior que o preço do ativo para resolver o aviso
        bt = Backtest(df, EmaCross, cash=200_000, commission=0)
        stats = bt.run()
        
        print("\n--- RESULTADOS DO BACKTEST PROFISSIONAL ---")
        print(stats)
        print("-------------------------------------------\n")

        # Plota um gráfico interativo com os resultados!
        bt.plot()
        
        connection.shutdown_mt5()