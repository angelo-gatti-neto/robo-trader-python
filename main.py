# main.py

import schedule
import time
from datetime import datetime
import MetaTrader5 as mt5
import config
import connection
import strategy
import risk_manager
import execution

def job():
    """Função principal que o robô executará a cada minuto."""
    print("-" * 50)
    print(f"Executando verificação... Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 1. Verifica se já existe uma posição aberta
    positions = mt5.positions_get(symbol=config.ATIVO)
    if positions and len(positions) > 0:
        print("Já existe uma posição aberta. Aguardando a próxima oportunidade.")
        return # Sai da função job se já houver uma posição

    # 2. Obter dados de mercado
    dados = strategy.get_market_data(config.ATIVO, config.TIMEFRAME)

    if dados is not None:
        # 3. Calcular indicadores
        dados_com_indicadores = strategy.calculate_indicators(dados)
        
        # 4. Verificar sinal de trade
        sinal = strategy.check_signal(dados_com_indicadores)
        
        print(f"Sinal identificado: {sinal}")

        # 5. Se houver sinal, calcular risco e enviar ordem
        if sinal == "COMPRAR" or sinal == "VENDER":
            print("Oportunidade encontrada! Calculando risco e enviando ordem...")

            # 5.1. Calcular Stop Loss e Take Profit
            sl, tp = risk_manager.calculate_stops(config.ATIVO, sinal)

            if sl is not None and tp is not None:
                # 5.2. Enviar a ordem
                execution.send_order(config.ATIVO, config.VOLUME, sinal, sl, tp)

# --- Bloco Principal de Execução ---
if __name__ == "__main__":
    if connection.initialize_mt5():
        
        schedule.every().minute.at(":01").do(job)

        print("Robô em execução. Pressione CTRL+C para parar.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nParando o robô...")
        finally:
            connection.shutdown_mt5()