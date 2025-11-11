#!/usr/bin/env python3
"""
Script principal para executar a otimização híbrida
Carrega configurações do arquivo config.json e executa o otimizador
"""
from datetime import datetime
from otimizador import HybridOptimizer
from config_manager import ConfigManager
import sys
import time
import os

def main():
    # Permite passar arquivo de configuração como argumento
    config_file = sys.argv[1] if len(sys.argv) > 1 else "config.json"
    
    print("═" * 60)
    print("     OTIMIZAÇÃO HÍBRIDA - PESQUISA OPERACIONAL")
    print("     Tarefa: Maximizar saída do modelo10.exe")
    print("═" * 60)
    print(f"Arquivo de configuração: {config_file}")
    print(f"Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    # Carrega e exibe resumo da configuração
    config_manager = ConfigManager(config_file)
    modelo_config = config_manager.get_modelo_config()
    
    print("CONFIGURAÇÃO CARREGADA:")
    print(f"  Modelo: {modelo_config['executavel']}")
    print(f"  Timeout por execução: {modelo_config['timeout']}s")
    print(f"  Parâmetros: {config_manager.get_num_params()}")
    print(f"    - Categóricos: {len(config_manager.get_categorico_params())}")
    print(f"    - Numéricos: {len(config_manager.get_numerico_params())}")
    
    # Exibe detalhes dos parâmetros
    print(f"\n  Detalhes dos Parâmetros:")
    for param in config_manager.config['parametros']:
        if param['tipo'] == 'categorico':
            print(f"    {param['nome']}: {param['opcoes']}")
        else:
            print(f"    {param['nome']}: [{param['min']} - {param['max']}]")
    
    otim_config = config_manager.get_otimizacao_config()
    tempo_total = otim_config.get('tempo_total_max', 3600)
    
    print(f"\nTEMPO TOTAL: {tempo_total/60:.0f} minutos")
    print(f"\nFASES ATIVAS:")
    for fase_nome, fase_config in otim_config['fases'].items():
        status = "✓" if fase_config.get('ativo', True) else "✗"
        tempo = fase_config.get('tempo_max', 0)
        print(f"  {status} {fase_nome.replace('_', ' ').title()}: {tempo/60:.1f} min")
    
    print("\n" + "─" * 60)
    print("INICIANDO OTIMIZAÇÃO...")
    print("─" * 60 + "\n")
    
    # Cria e executa o otimizador
    optimizer = HybridOptimizer(config_file)
    
    # Executa as fases configuradas
    optimizer.explore_edges()
    optimizer.pso_optimize()
    optimizer.local_search()
    
    # Gera relatório final
    print("\n" + "─" * 60)
    print("GERANDO RELATÓRIO FINAL...")
    print("─" * 60 + "\n")
    
    optimizer.generate_report()
    
    print("\n" + "═" * 60)
    print("          OTIMIZAÇÃO CONCLUÍDA COM SUCESSO!")
    print("═" * 60)
    print(f"Fim: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    tempo_total = time.time() - optimizer.start_time
    print(f"Tempo total: {tempo_total/60:.2f} minutos")
    print(f"Tentativas: {optimizer.attempts}")
    print(f"Melhor valor: {optimizer.best_value:.6f}")
    print(f"\n📁 Pasta de resultados: {optimizer.resultado_dir}/")
    print("═" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Otimização interrompida pelo usuário!")
    except Exception as e:
        print(f"\n\n❌ Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()
