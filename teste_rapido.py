#!/usr/bin/env python3
"""
Script de teste rápido - 30 segundos
Use para verificar se tudo está funcionando
"""
import json
import sys
from executar_otimizacao import main
from config_manager import ConfigManager

# Cria configuração de teste rápido
config_teste = {
    "modelo": {
        "executavel": "./modelo10.exe",
        "timeout": 10
    },
    "parametros": [
        {
            "nome": "x1",
            "tipo": "categorico",
            "opcoes": ["baixo", "medio", "alto"],
            "descricao": "Parâmetro categórico"
        }
    ] + [
        {
            "nome": f"x{i}",
            "tipo": "numerico",
            "min": 1,
            "max": 100,
            "descricao": f"Parâmetro numérico {i}"
        }
        for i in range(2, 11)
    ],
    "otimizacao": {
        "fases": {
            "exploracao_bordas": {
                "ativo": True,
                "tempo_max": 10,
                "configuracoes_teste": [[100, 100], [1, 1], [50, 50]]
            },
            "pso": {
                "ativo": True,
                "tempo_max": 15,
                "num_particulas": 5,
                "inercia": 0.7,
                "c1": 1.5,
                "c2": 1.5,
                "probabilidade_mutacao": 0.15
            },
            "busca_local": {
                "ativo": True,
                "tempo_max": 5,
                "deltas": [-5, -2, 0, 2, 5]
            }
        },
        "tempo_total_max": 30
    }
}

# Salva configuração de teste
with open('config_teste.json', 'w') as f:
    json.dump(config_teste, f, indent=2)

print("=" * 60)
print("   TESTE RÁPIDO - 30 SEGUNDOS")
print("=" * 60)
print("Configuração salva em: config_teste.json")
print("Executando teste...\n")

# Executa com configuração de teste
sys.argv = ['teste_rapido.py', 'config_teste.json']
main()
