# config.py

# --- CONFIGURAÇÕES DE CONEXÃO ---
# Substitua com suas credenciais da conta MT5 (pode ser a demo)
MT5_LOGIN = 512345678
MT5_PASSWORD = "Sua Senha"
MT5_SERVER = "NomeDoServidor-Demo"

# --- CONFIGURAÇÕES DO ATIVO ---
# Ativo que o robô vai operar
# Para mini-índice, o código muda todo bimestre (ex: WINZ25, WING26). 
# Para minidólar, muda todo mês (ex: WDOZ25, WDOF26).
# ATENÇÃO: Use o código do contrato VIGENTE!
ATIVO = "WINV25" # Verifique se este é o código atual do mini-índice

# Timeframe que o robô vai analisar
TIMEFRAME = "M5" # M1 = 1 minuto, M5 = 5 minutos, etc.

# --- CONFIGURAÇÕES DA ESTRATÉGIA ---
MEDIA_CURTA = 21
MEDIA_LONGA = 55

# --- CONFIGURAÇÕES DE RISCO ---
RISK_POINTS_STOP_LOSS = 100
RISK_POINTS_TAKE_PROFIT = 200
VOLUME = 1.0