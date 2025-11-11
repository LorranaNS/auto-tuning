#!/usr/bin/env python3
"""
Lista todos os resultados de otimizações anteriores
"""
import os
import json
from datetime import datetime

def listar_resultados():
    print("═" * 70)
    print("        HISTÓRICO DE OTIMIZAÇÕES")
    print("═" * 70)
    
    base_dir = 'resultados'
    
    if not os.path.exists(base_dir):
        print(f"\n❌ Pasta '{base_dir}' não encontrada.")
        print("   Nenhuma otimização foi executada ainda.")
        return
    
    # Lista todas as pastas de tentativas
    tentativas = []
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path) and item.startswith('tentativa_'):
            tentativas.append(item)
    
    if not tentativas:
        print(f"\n❌ Nenhuma tentativa encontrada em '{base_dir}'")
        return
    
    # Ordena por data (mais recente primeiro)
    tentativas.sort(reverse=True)
    
    print(f"\nTotal de tentativas encontradas: {len(tentativas)}\n")
    print(f"{'#':<4} {'Data/Hora':<20} {'Melhor Valor':<15} {'Tentativas':<12} {'Tempo':<10}")
    print("─" * 70)
    
    for idx, tentativa in enumerate(tentativas, 1):
        tentativa_path = os.path.join(base_dir, tentativa)
        resumo_path = os.path.join(tentativa_path, 'resumo.txt')
        
        # Extrai data/hora do nome da pasta
        try:
            # tentativa_21-01-2025_1930 -> 21/01/2025 19:30
            data_str = tentativa.replace('tentativa_', '')
            data_formatada = datetime.strptime(data_str, '%d-%m-%Y_%H%M').strftime('%d/%m/%Y %H:%M')
        except:
            data_formatada = tentativa.replace('tentativa_', '')
        
        # Lê resumo se existir
        if os.path.exists(resumo_path):
            try:
                with open(resumo_path, 'r') as f:
                    linhas = f.readlines()
                    melhor_valor = linhas[0].split(':')[1].strip() if len(linhas) > 0 else 'N/A'
                    num_tentativas = linhas[1].split(':')[1].strip() if len(linhas) > 1 else 'N/A'
                    tempo = linhas[2].split(':')[1].strip() if len(linhas) > 2 else 'N/A'
            except:
                melhor_valor = num_tentativas = tempo = 'N/A'
        else:
            melhor_valor = num_tentativas = tempo = 'N/A'
        
        print(f"{idx:<4} {data_formatada:<20} {melhor_valor:<15} {num_tentativas:<12} {tempo:<10}")
    
    print("─" * 70)
    print(f"\n💡 Para ver detalhes de uma tentativa:")
    print(f"   cat resultados/tentativa_YYYYMMDD_HHMMSS/relatorio_otimizacao.txt")
    print(f"\n💡 Para comparar tentativas:")
    print(f"   python comparar_resultados.py")
    print("═" * 70)

if __name__ == "__main__":
    listar_resultados()
