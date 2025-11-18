#!/usr/bin/env python3
"""
Script principal para executar a otimização híbrida
Carrega configurações do arquivo config.json e executa o otimizador
"""
from datetime import datetime
from cli import run_cli, console, print_banner
from otimizador import HybridOptimizer
import sys
import json
import time
import os

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
        
        # Executa as fases
        optimizer.explore_edges()
        optimizer.pso_optimize()
        optimizer.local_search()
        
        # Gera relatório
        optimizer.generate_report()
        
        console.print("\n[bold green]✓ Otimização concluída com sucesso![/bold green]")
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠ Otimização interrompida pelo usuário.[/yellow]")
        if optimizer.best_params:
            console.print("\n[cyan]Gerando relatório parcial...[/cyan]")
            optimizer.generate_report()
    
    except Exception as e:
        console.print(f"\n[red]✗ Erro durante a otimização: {e}[/red]")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
