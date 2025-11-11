#!/usr/bin/env python3
"""
Compara resultados de múltiplas otimizações
"""
import os
import json
from datetime import datetime

def comparar_resultados():
    print("═" * 80)
    print("        COMPARAÇÃO DE RESULTADOS")
    print("═" * 80)
    
    base_dir = 'resultados'
    
    if not os.path.exists(base_dir):
        print(f"\n❌ Pasta '{base_dir}' não encontrada.")
        return
    
    # Coleta dados de todas as tentativas
    dados = []
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path) and item.startswith('tentativa_'):
            resumo_path = os.path.join(item_path, 'resumo.txt')
            historico_path = os.path.join(item_path, 'historico_otimizacao.json')
            
            if os.path.exists(resumo_path):
                try:
                    with open(resumo_path, 'r') as f:
                        linhas = f.readlines()
                        melhor_valor = float(linhas[0].split(':')[1].strip())
                        tentativas = int(linhas[1].split(':')[1].strip())
                        tempo_str = linhas[2].split(':')[1].strip().replace(' min', '')
                        tempo = float(tempo_str)
                        
                        # Data da tentativa (formato: tentativa_21-01-2025_1930)
                        data_str = item.replace('tentativa_', '')
                        data = datetime.strptime(data_str, '%d-%m-%Y_%H%M')
                        
                        dados.append({
                            'pasta': item,
                            'data': data,
                            'valor': melhor_valor,
                            'tentativas': tentativas,
                            'tempo': tempo
                        })
                except Exception as e:
                    print(f"⚠️  Erro ao ler {item}: {e}")
    
    if not dados:
        print("\n❌ Nenhum resultado válido encontrado.")
        return
    
    # Ordena por valor (melhor primeiro)
    dados.sort(key=lambda x: x['valor'], reverse=True)
    
    print(f"\nTotal de execuções: {len(dados)}\n")
    
    # Estatísticas
    valores = [d['valor'] for d in dados]
    tentativas_totais = [d['tentativas'] for d in dados]
    tempos = [d['tempo'] for d in dados]
    
    print("ESTATÍSTICAS GERAIS:")
    print("─" * 80)
    print(f"Melhor valor encontrado:  {max(valores):.6f}")
    print(f"Pior valor encontrado:    {min(valores):.6f}")
    print(f"Média dos valores:        {sum(valores)/len(valores):.6f}")
    print(f"Média de tentativas:      {sum(tentativas_totais)/len(tentativas_totais):.0f}")
    print(f"Média de tempo:           {sum(tempos)/len(tempos):.2f} min")
    print()
    
    # Top 5
    print("TOP 5 MELHORES RESULTADOS:")
    print("─" * 80)
    print(f"{'#':<4} {'Data/Hora':<20} {'Valor':<15} {'Tentativas':<12} {'Tempo (min)':<12}")
    print("─" * 80)
    
    for idx, d in enumerate(dados[:5], 1):
        data_formatada = d['data'].strftime('%d/%m/%Y %H:%M:%S')
        print(f"{idx:<4} {data_formatada:<20} {d['valor']:<15.6f} {d['tentativas']:<12} {d['tempo']:<12.2f}")
    
    print("─" * 80)
    
    # Melhor resultado
    melhor = dados[0]
    print(f"\n🏆 MELHOR RESULTADO:")
    print(f"   Pasta: {melhor['pasta']}")
    print(f"   Valor: {melhor['valor']:.6f}")
    print(f"   Data:  {melhor['data'].strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"\n   Ver detalhes: cat resultados/{melhor['pasta']}/relatorio_otimizacao.txt")
    
    print("═" * 80)

if __name__ == "__main__":
    comparar_resultados()
