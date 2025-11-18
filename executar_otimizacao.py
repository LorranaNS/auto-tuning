"""
Script principal para executar a otimização híbrida
Carrega configurações do arquivo config.json e executa o otimizador
Compatível com Windows e Linux
"""
from datetime import datetime
from cli import run_cli, console, print_banner
from otimizador import HybridOptimizer
import sys
import json
import time
import os
import importlib

# Força recarregar o módulo CLI para evitar cache
if 'cli' in sys.modules:
    importlib.reload(sys.modules['cli'])
    from cli import run_cli

def main():
    # Executa CLI interativa
    config = run_cli()
    
    if config is None:
        console.print("\n[yellow]Programa encerrado.[/yellow]")
        return
    
    # Salva configuração temporária
    temp_config = "temp_config.json"
    with open(temp_config, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    try:
        # Inicializa otimizador
        optimizer = HybridOptimizer(temp_config)
        
        # Fase 1: Exploração de bordas
        optimizer.explore_edges()
        
        # Fase 2: PSO
        optimizer.pso_optimize()
        
        # Fase 3: PSO Focado em Bordas (substituiu busca local)
        optimizer.pso_bordas()
        
        # Gera relatório final
        optimizer.generate_report()
        
        console.print("\n[bold green]✓ Otimização concluída com sucesso![/bold green]")
        
        # Remove arquivo temporário
        try:
            if os.path.exists(temp_config):
                os.remove(temp_config)
        except:
            pass
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠ Otimização interrompida pelo usuário.[/yellow]")
        if hasattr(optimizer, 'best_params') and optimizer.best_params:
            console.print("\n[cyan]Gerando relatório parcial...[/cyan]")
            optimizer.generate_report()
    
    except Exception as e:
        console.print(f"\n[red]✗ Erro durante a otimização: {e}[/red]")
        import traceback
        traceback.print_exc()
    
    finally:
        # Limpeza final
        try:
            if os.path.exists(temp_config):
                os.remove(temp_config)
        except:
            pass

if __name__ == "__main__":
    main()
