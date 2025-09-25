# backtester_pro.py (Versão Corrigida)

from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import MetaTrader5 as mt5
from datetime import datetime, timedelta
import pandas as pd
import config
import connection
import strategy as strat

# Classe da Estratégia EmaCross (continua a mesma)
class EmaCross(Strategy):
    n1 = config.MEDIA_CURTA
    n2 = config.MEDIA_LONGA
    n_tendencia = 200
    stop_loss_points = config.RISK_POINTS_STOP_LOSS
    take_profit_points = config.RISK_POINTS_TAKE_PROFIT

    def init(self):
        close = self.data.Close
        self.ema1 = self.I(lambda x, n: pd.Series(x).ewm(span=n, adjust=False).mean(), close, self.n1)
        self.ema2 = self.I(lambda x, n: pd.Series(x).ewm(span=n, adjust=False).mean(), close, self.n2)
        self.ema_tendencia = self.I(lambda x, n: pd.Series(x).ewm(span=n, adjust=False).mean(), close, self.n_tendencia)

    def next(self):
        price = self.data.Close[-1]
        
        if crossover(self.ema1, self.ema2) and price > self.ema_tendencia[-1]:
            self.buy(sl=price - self.stop_loss_points, tp=price + self.take_profit_points, size=1)

        elif crossover(self.ema2, self.ema1) and price < self.ema_tendencia[-1]:
            self.sell(sl=price + self.stop_loss_points, tp=price - self.take_profit_points, size=1)


if __name__ == "__main__":
    # --- CORREÇÃO APLICADA AQUI ---
    # Agora passamos as credenciais do config para a função de inicialização
    if connection.initialize_mt5(config.MT5_LOGIN, config.MT5_PASSWORD, config.MT5_SERVER):
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        
        rates = mt5.copy_rates_range(config.ATIVO, strat.TIMEFRAME_MAP[config.TIMEFRAME], start_date, end_date)
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        
        df.rename(columns={
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'tick_volume': 'Volume'
        }, inplace=True)

        bt = Backtest(df, EmaCross, cash=200_000, commission=0)
        stats = bt.run()
        
        print("\n--- RESULTADOS DO BACKTEST PROFISSIONAL ---")
        print(stats)
        print("-------------------------------------------\n")

        bt.plot()
        
        connection.shutdown_mt5()