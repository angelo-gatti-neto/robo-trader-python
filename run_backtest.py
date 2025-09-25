# run_backtest.py (VERSÃO CORRETA E DINÂMICA)

from datetime import datetime, timedelta
import connection
import backtester
import config

if __name__ == "__main__":
    if connection.initialize_mt5():
        
        # Define o período do backtest para os últimos 30 dias a partir de HOJE
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Executa o backtest
        results = backtester.run_backtest(
            config.ATIVO,
            config.TIMEFRAME,
            start_date,
            end_date
        )
        
        # Imprime os resultados
        if results:
            print("\n--- RESULTADOS DO BACKTEST ---")
            print(f"Período Analisado: {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}")
            print(f"Total de Trades: {results['total_trades']}")
            print(f"Trades Vencedores: {results['wins']}")
            print(f"Trades Perdedores: {results['losses']}")
            print(f"Taxa de Acerto: {results['win_rate_percent']:.2f}%")
            print(f"Resultado Total (Pontos): {results['total_pnl_points']:.2f} pontos")
            print("------------------------------\n")
            
        connection.shutdown_mt5()