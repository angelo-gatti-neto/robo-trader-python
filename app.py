# app.py (VERSÃO DE SEGURANÇA - usa apenas o TK básico)

import tkinter as tk
from tkinter import scrolledtext # scrolledtext é geralmente seguro
import threading
from datetime import datetime
import time
import schedule
import sys
from queue import Queue
import MetaTrader5 as mt5

# Importamos a lógica do nosso robô que já existe
import connection
import strategy
import risk_manager
import execution
import config

# Classe para redirecionar o 'print' para a nossa caixa de log
class QueueHandler:
    def __init__(self, queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)
    
    def flush(self):
        pass

# --- ESTRUTURA DA APLICAÇÃO GUI ---

class TradingBotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Robô Trader Pessoal (Modo de Segurança)")
        self.geometry("600x450")

        self.robot_thread = None
        self.stop_robot = False
        
        self.log_queue = Queue()

        self.create_widgets()
        self.process_log_queue()

    def create_widgets(self):
        # Frame principal para organizar tudo
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        # Frame para as credenciais (usando tk.LabelFrame)
        credentials_frame = tk.LabelFrame(main_frame, text="Credenciais MT5", padx=10, pady=10)
        credentials_frame.pack(fill="x", anchor="n")

        tk.Label(credentials_frame, text="Login:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.login_entry = tk.Entry(credentials_frame, width=35)
        self.login_entry.insert(0, str(config.MT5_LOGIN))
        self.login_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(credentials_frame, text="Senha:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.password_entry = tk.Entry(credentials_frame, show="*", width=35)
        self.password_entry.insert(0, config.MT5_PASSWORD)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(credentials_frame, text="Servidor:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.server_entry = tk.Entry(credentials_frame, width=35)
        self.server_entry.insert(0, config.MT5_SERVER)
        self.server_entry.grid(row=2, column=1, padx=5, pady=5)

        # Frame para os controles (usando tk.Frame)
        controls_frame = tk.Frame(main_frame)
        controls_frame.pack(pady=10, fill="x")

        self.start_button = tk.Button(controls_frame, text="INICIAR ROBÔ", command=self.start_robot_thread, width=15)
        self.start_button.pack(side="left", padx=5)

        self.stop_button = tk.Button(controls_frame, text="PARAR ROBÔ", state="disabled", command=self.stop_robot_thread, width=15)
        self.stop_button.pack(side="left", padx=5)
        
        # Frame para o Log (usando tk.LabelFrame)
        log_frame = tk.LabelFrame(main_frame, text="Log de Operações", padx=10, pady=10)
        log_frame.pack(fill="both", expand=True)

        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state="disabled", height=10)
        self.log_area.pack(fill="both", expand=True)

    # O resto do código (lógica dos botões e da thread) é exatamente o mesmo
    def log(self, message):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, message)
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")

    def process_log_queue(self):
        try:
            message = self.log_queue.get_nowait()
            self.log(message)
        except:
            pass
        self.after(100, self.process_log_queue)

    def start_robot_thread(self):
        self.stop_robot = False
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.log("Iniciando o robô...\n")
        
        self.robot_thread = threading.Thread(target=self.run_robot_logic, daemon=True)
        self.robot_thread.start()

    def stop_robot_thread(self):
        self.log("Sinal de parada enviado... Aguardando a próxima verificação para parar.\n")
        self.stop_robot = True
        self.stop_button.config(state="disabled")
        
    def run_robot_logic(self):
        sys.stdout = QueueHandler(self.log_queue)
        login = int(self.login_entry.get())
        password = self.password_entry.get()
        server = self.server_entry.get()

        if connection.initialize_mt5(login, password, server):
            def job():
                print("-" * 50 + "\n")
                print(f"Executando verificação... Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                positions = mt5.positions_get(symbol=config.ATIVO)
                if positions and len(positions) > 0:
                    print(f"Posição aberta encontrada: {len(positions)}. Aguardando.\n")
                    return
                dados = strategy.get_market_data(config.ATIVO, config.TIMEFRAME)
                if dados is not None:
                    dados_com_indicadores = strategy.calculate_indicators(dados)
                    sinal = strategy.check_signal(dados_com_indicadores)
                    print(f"Sinal identificado: {sinal}\n")
                    if sinal == "COMPRAR" or sinal == "VENDER":
                        print("Oportunidade encontrada! Enviando ordem...\n")
                        sl, tp = risk_manager.calculate_stops(config.ATIVO, sinal)
                        if sl is not None and tp is not None:
                            execution.send_order(config.ATIVO, config.VOLUME, sinal, sl, tp)
            
            schedule.every().minute.at(":01").do(job)
            while not self.stop_robot:
                schedule.run_pending()
                time.sleep(1)

            connection.shutdown_mt5()
            print("\nRobô parado com sucesso.\n")
            self.start_button.config(state="normal")
        else:
            print("\n!!! Falha na conexão. Verifique as credenciais. !!!\n")
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
        
        sys.stdout = sys.__stdout__

if __name__ == "__main__":
    app = TradingBotApp()
    def on_closing():
        app.stop_robot = True
        app.destroy()
    
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()