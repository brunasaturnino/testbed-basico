import os
import sys
import json
from datetime import datetime
from strategy.DefenceStrategyImplementation import DefenceStrategyImplementation

# Caminho para o arquivo de log gerado pelo honeypot
LOG_FILE = "honeypot.log"

# Diretório de execução recebido como argumento
if len(sys.argv) < 2:
    print("Erro: Diretório de execução não especificado.")
    sys.exit(1)

dir = sys.argv[1]

# Inicializar debug log
debug_path = os.path.join(dir, 'debug')
try:
    with open(debug_path, 'a') as log:
        log.write(f"Run started at {datetime.utcnow()}\n")
except Exception as e:
    print(f"Erro ao criar arquivo de depuração: {e}")
    sys.exit(1)

# Função para processar o arquivo de log do honeypot
def process_log_line(line):
    """
    Processa uma linha do log para extrair dados relevantes.
    Exemplo: "2024-11-26 22:34:14,420 - Connection from 192.168.0.1"
    """
    try:
        parts = line.strip().split(" - ")
        timestamp = parts[0]
        message = parts[1]
        if "Connection from" in message:
            ip = message.split("Connection from ")[1]
            return {"timestamp": timestamp, "ip": ip}
        elif "Username" in message and "Password" in message:
            username = message.split("Username: ")[1].split(",")[0]
            password = message.split("Password: ")[1]
            return {"timestamp": timestamp, "username": username, "password": password, "ip": "127.0.0.1"}  # Fallback IP
    except Exception as e:
        print(f"Erro ao processar linha do log: {e}")
    return None


# Ler eventos do arquivo de log do honeypot
events = []
try:
    print(f"Lendo eventos do arquivo: {LOG_FILE}")
    with open(LOG_FILE, 'r') as log_file:
        for line in log_file:
            event = process_log_line(line)
            if event:
                events.append(event)
    print(f"Eventos capturados: {events}")  # Mensagem de depuração
except FileNotFoundError:
    print(f"Erro: Arquivo de log {LOG_FILE} não encontrado.")
    with open(debug_path, 'a') as log:
        log.write(f"Log file not found: {LOG_FILE}\n")
    sys.exit(1)
except Exception as e:
    print(f"Erro ao ler o arquivo de log: {e}")
    sys.exit(1)

# Processar eventos com a estratégia
strategy = DefenceStrategyImplementation(dir)
try:
    metrics = strategy.defend(events)
    print(f"Métricas processadas: {metrics}")  # Mensagem de depuração
except Exception as e:
    print(f"Erro ao processar eventos com a estratégia: {e}")
    with open(debug_path, 'a') as log:
        log.write(f"Erro ao executar a estratégia: {e}\n")
    sys.exit(1)

# Salvar métricas no arquivo info
info_path = os.path.join(dir, 'info')
try:
    with open(info_path, 'w') as info:
        info.write(json.dumps({
            "start": datetime.utcnow().isoformat(),
            "events_processed": len(events),
            "metrics": metrics,
            "end": datetime.utcnow().isoformat()
        }, indent=4) + "\n")
    print(f"Métricas salvas em: {info_path}")
except Exception as e:
    print(f"Erro ao salvar métricas no arquivo info: {e}")
    with open(debug_path, 'a') as log:
        log.write(f"Erro ao salvar métricas: {e}\n")
    sys.exit(1)

# Finalizar execução com sucesso
with open(debug_path, 'a') as log:
    log.write(f"Run completed successfully at {datetime.utcnow()}\n")
