#!/bin/bash

echo "════════════════════════════════════════════════════════════"
echo "  EXEMPLOS DE USO - OTIMIZADOR HÍBRIDO"
echo "════════════════════════════════════════════════════════════"
echo ""

# Torna scripts executáveis
chmod +x modelo10.exe 2>/dev/null
chmod +x *.py

echo "1️⃣  VERIFICAR SE O MODELO FUNCIONA"
echo "   python verificar_modelo.py"
echo ""

echo "2️⃣  TESTE RÁPIDO (30 segundos)"
echo "   python teste_rapido.py"
echo ""

echo "3️⃣  EXECUÇÃO COMPLETA (1 hora)"
echo "   python executar_otimizacao.py"
echo ""

echo "4️⃣  EXECUÇÃO COM CONFIG CUSTOMIZADA"
echo "   python executar_otimizacao.py minha_config.json"
echo ""

echo "5️⃣  TESTAR MANUALMENTE O MODELO"
echo "   ./modelo10.exe baixo 50 50 50 50 50 50 50 50 50"
echo ""

echo "════════════════════════════════════════════════════════════"
echo ""

read -p "Deseja executar a verificação do modelo agora? (s/n): " resposta

if [ "$resposta" = "s" ] || [ "$resposta" = "S" ]; then
    echo ""
    python3 verificar_modelo.py
fi
