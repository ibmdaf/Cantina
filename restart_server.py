#!/usr/bin/env python
"""
Script para reiniciar o servidor Django
Execute: python restart_server.py
"""
import os
import signal
import subprocess
import sys

def find_django_process():
    """Encontra o processo do servidor Django"""
    try:
        # Procura por processos python rodando manage.py
        result = subprocess.run(
            ['ps', 'aux'],
            capture_output=True,
            text=True
        )
        
        for line in result.stdout.split('\n'):
            if 'manage.py runserver' in line and 'python' in line:
                # Extrai o PID (segunda coluna)
                pid = int(line.split()[1])
                return pid
        return None
    except Exception as e:
        print(f"Erro ao procurar processo: {e}")
        return None

def main():
    print("🔍 Procurando servidor Django...")
    pid = find_django_process()
    
    if pid:
        print(f"✅ Servidor encontrado (PID: {pid})")
        print("🛑 Parando servidor...")
        try:
            os.kill(pid, signal.SIGTERM)
            print("✅ Servidor parado!")
        except Exception as e:
            print(f"❌ Erro ao parar servidor: {e}")
            return
    else:
        print("ℹ️  Nenhum servidor Django rodando")
    
    print("\n🚀 Iniciando novo servidor...")
    print("=" * 50)
    
    # Inicia o servidor
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver'])
    except KeyboardInterrupt:
        print("\n\n👋 Servidor parado pelo usuário")

if __name__ == '__main__':
    main()
