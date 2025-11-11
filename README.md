# Otimização Híbrida - Pesquisa Operacional

## 📝 Descrição da Tarefa

Encontrar o **maior valor** possível de um programa (`modelo10.exe`) que simula um modelo matemático com 10 parâmetros de entrada:

- **Parâmetro 1**: valor textual (baixo, medio, alto)
- **Parâmetros 2-10**: valores inteiros de 1 a 100

**Tempo disponível**: 1 hora (19:30h - 20:30h)

## 🎯 Estratégia Utilizada

### Abordagem Híbrida em 3 Fases

#### **FASE 1: Exploração de Bordas** (5 minutos)

- Testa combinações nos extremos do espaço de busca
- Identifica regiões promissoras
- Combina os 3 valores categóricos com configurações de bordas

#### **FASE 2: Particle Swarm Optimization - PSO** (50 minutos)

- 30 partículas exploram o espaço simultaneamente
- Cada partícula aprende com sua melhor posição e a melhor global
- Mutação aleatória para o parâmetro categórico (15% de chance)
- Convergência inteligente para regiões ótimas

#### **FASE 3: Busca Local Refinada** (5 minutos)

- Refina a melhor solução encontrada
- Testa variações pequenas em cada parâmetro
- Garante que chegamos no melhor local possível

## 🧪 Como Testar

### 1. Verificar se o modelo funciona

```bash
python verificar_modelo.py
```

Este script:

- ✓ Verifica se modelo10.exe existe
- ✓ Testa 3 configurações diferentes
- ✓ Valida as saídas do modelo

### 2. Teste rápido (30 segundos)

```bash
python teste_rapido.py
```

Executa otimização reduzida para verificar se tudo está funcionando.

### 3. Teste manual do modelo

```bash
./modelo10.exe baixo 50 50 50 50 50 50 50 50 50
```

Testa diretamente o executável.

### 4. Execução completa

```bash
python executar_otimizacao.py
```

Executa a otimização completa de 1 hora.

## 📋 Checklist Antes de Executar

- [ ] `modelo10.exe` está no diretório
- [ ] `modelo10.exe` tem permissão de execução
- [ ] `config.json` está configurado corretamente
- [ ] Testou com `verificar_modelo.py`
- [ ] Testou com `teste_rapido.py`
- [ ] Está pronto para a execução completa

## 🚀 Como Executar

### Requisitos

- Python 3.x
- Arquivo `modelo10.exe` no diretório do projeto

### Execução

```bash
python executar_otimizacao.py
```

### Execução com configuração customizada

```bash
python executar_otimizacao.py minha_config.json
```

## 📊 Arquivos Gerados

Após a execução, o sistema gera:

1. **`relatorio_otimizacao.txt`**

   - Estratégia utilizada
   - Tempo total de execução
   - Número de tentativas
   - Melhor valor encontrado
   - Sequência de parâmetros
   - Comando para reproduzir o resultado

2. **`historico_otimizacao.json`**
   - Histórico completo de todas as tentativas
   - Útil para análise posterior

## 📁 Estrutura do Projeto

```
pesquisa_operacional/
├── modelo10.exe              # Modelo fornecido (caixa-preta)
├── config.json               # Configuração de parâmetros
├── config_manager.py         # Gerenciador de configuração
├── otimizador.py            # Motor de otimização
├── executar_otimizacao.py   # Script principal
├── README.md                # Esta documentação
├── relatorio_otimizacao.txt # Relatório gerado
└── historico_otimizacao.json # Histórico gerado
```

## ⚙️ Configuração

O arquivo `config.json` permite ajustar:

- Parâmetros e seus limites
- Tempo de cada fase
- Número de partículas do PSO
- Coeficientes de aprendizado
- Probabilidade de mutação
- Ativar/desativar fases

## 🔧 Personalização

### Ajustar tempos das fases

Edite `config.json`:

```json
"fases": {
  "exploracao_bordas": {
    "tempo_max": 300  // 5 minutos
  },
  "pso": {
    "tempo_max": 3000  // 50 minutos
  },
  "busca_local": {
    "tempo_max": 300  // 5 minutos
  }
}
```

### Desativar uma fase

```json
"exploracao_bordas": {
  "ativo": false
}
```

## 📈 Exemplo de Resultado

```
═══════════════════════════════════════════════════════════════
                    RELATÓRIO DE OTIMIZAÇÃO
═══════════════════════════════════════════════════════════════

MELHOR RESULTADO ENCONTRADO:
-----------------------------
Valor: 9876.543210

Parâmetros:
  x1   (categorico): alto
  x2   (1-100)     : 87
  x3   (1-100)     : 45
  x4   (1-100)     : 92
  x5   (1-100)     : 33
  x6   (1-100)     : 67
  x7   (1-100)     : 54
  x8   (1-100)     : 78
  x9   (1-100)     : 21
  x10  (1-100)     : 99

Comando para reproduzir:
./modelo10.exe alto 87 45 92 33 67 54 78 21 99
```

## 🎓 Vantagens da Estratégia

1. **Exploração Global**: PSO evita mínimos locais
2. **Refinamento Local**: Busca local garante otimalidade
3. **Configurável**: Fácil ajustar sem mudar código
4. **Auditável**: Histórico completo de tentativas
5. **Reproduzível**: Comando exato para reproduzir resultado
6. **Eficiente**: Aproveita todo o tempo disponível
