# Otimização Híbrida - Pesquisa Operacional

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.x instalado
- Arquivo `modelo10.exe` no diretório raiz do projeto

### Instalação

**Windows:**

```powershell
# Navegue até o diretório
cd C:\caminho\para\pesquisa_operacional

# Instale as dependências
pip install -r requirements.txt
```

**Linux/Mac:**

```bash
# Navegue até o diretório
cd /caminho/para/pesquisa_operacional

# Instale as dependências
pip install -r requirements.txt

# Dê permissão de execução ao modelo (apenas Linux/Mac)
chmod +x modelo10.exe
```

### Passos para executar

1. **Execute a CLI interativa:**

   **Windows:**

   ```powershell
   python executar_otimizacao.py
   ```

   **Linux/Mac:**

   ```bash
   python3 executar_otimizacao.py
   ```

2. **Siga o menu interativo:**

   - Escolha usar configuração de arquivo ou definir manualmente
   - Configure parâmetros, fases e objetivos
   - Confirme e inicie a otimização

3. **Alternativa - Teste rápido (30 segundos):**

   ```bash
   python teste_rapido.py
   ```

### Resultados

Após a execução, verifique a pasta `resultados\tentativa_DD-MM-AAAA_HHMM\` (Windows) ou `resultados/tentativa_DD-MM-AAAA_HHMM/` (Linux):

- `relatorio_otimizacao.txt` - relatório com melhor resultado
- `historico_otimizacao.json` - histórico completo de tentativas
- `config_utilizada.json` - configuração usada nesta execução
- `resumo.txt` - resumo rápido do melhor resultado

---

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

#### **FASE 2: Particle Swarm Optimization - PSO Global** (45 minutos)

- 30 partículas exploram o espaço simultaneamente
- Cada partícula aprende com sua melhor posição e a melhor global
- Mutação aleatória para o parâmetro categórico (15% de chance)
- Convergência inteligente para regiões ótimas

#### **FASE 3: PSO Focado em Bordas** (10 minutos)

- Combina PSO com exploração intensiva de bordas
- Partículas iniciam nas melhores regiões de borda encontradas
- PSO refinado com menor inércia para busca local mais agressiva
- Explora variações próximas aos extremos promissores

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

**Windows:**

```powershell
.\modelo10.exe baixo 50 50 50 50 50 50 50 50 50
```

**Linux/Mac:**

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

- [ ] Python 3.x instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] `modelo10.exe` está no diretório
- [ ] ~~`modelo10.exe` tem permissão de execução (apenas Linux/Mac)~~
- [ ] Pronto para executar `python executar_otimizacao.py`

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

- **Objetivo**: maximizar ou minimizar o resultado
- Parâmetros e seus limites
- Tempo de cada fase
- Número de partículas do PSO
- Coeficientes de aprendizado
- Probabilidade de mutação
- Ativar/desativar fases

### Configuração do Objetivo

Por padrão, o sistema **maximiza** o valor de retorno do modelo. Para **minimizar**, altere:

```json
{
  "objetivo": "minimizar"
}
```

Opções disponíveis:

- `"maximizar"` (padrão) - busca o maior valor possível
- `"minimizar"` - busca o menor valor possível

## 🔧 Personalização

### Alterar objetivo (maximizar/minimizar)

Edite `config.json`:

```json
{
  "objetivo": "minimizar",
  "parametros": {
    // ...
  }
}
```

### Ajustar tempos das fases

Edite `config.json`:

```json
"fases": {
  "exploracao_bordas": {
    "tempo_max": 300  // 5 minutos
  },
  "pso": {
    "tempo_max": 2700  // 45 minutos
  },
  "pso_bordas": {
    "tempo_max": 600  // 10 minutos
  }
}
```

### Desativar uma fase

```json
"pso_bordas": {
  "ativo": false
}
```

## 📈 Exemplo de Resultado

### Maximização (padrão) Ajustar tempos das fases

````
═══════════════════════════════════════════════════════════════
                    RELATÓRIO DE OTIMIZAÇÃO```json
═══════════════════════════════════════════════════════════════

OBJETIVO: MAXIMIZAR00  // 5 minutos
  },
MELHOR RESULTADO ENCONTRADO:
----------------------------- 50 minutos
Valor: 9876.543210

Parâmetros:/ 5 minutos
  x1   (categorico): alto
  x2   (1-100)     : 87
  x3   (1-100)     : 45
  x4   (1-100)     : 92
  x5   (1-100)     : 33
  x6   (1-100)     : 67
  x7   (1-100)     : 54```json
  x8   (1-100)     : 78
  x9   (1-100)     : 21
  x10  (1-100)     : 99
````

Comando para reproduzir:
./modelo10.exe alto 87 45 92 33 67 54 78 21 99## 📈 Exemplo de Resultado

````

### Minimização════════════

```═══
════════

























6. **Eficiente**: Aproveita todo o tempo disponível5. **Reproduzível**: Comando exato para reproduzir resultado4. **Auditável**: Histórico completo de tentativas3. **Configurável**: Fácil ajustar sem mudar código2. **Refinamento Local**: Busca local garante otimalidade1. **Exploração Global**: PSO evita mínimos locais## 🎓 Vantagens da Estratégia```./modelo10.exe baixo 23 15 7 3 1 6 2 9 4Comando para reproduzir:  x10  (1-100)     : 4  x9   (1-100)     : 9  x8   (1-100)     : 2  x7   (1-100)     : 6  x6   (1-100)     : 1  x5   (1-100)     : 3  x4   (1-100)     : 7  x3   (1-100)     : 15  x2   (1-100)     : 23  x1   (categorico): baixoParâmetros:Valor: 12.345678-----------------------------MELHOR RESULTADO ENCONTRADO:OBJETIVO: MINIMIZAR═══════════════════════════════════════════════════════════════-----------------------------
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
````

## 🎓 Vantagens da Estratégia

1. **Exploração Global**: PSO evita mínimos locais
2. **Foco em Bordas**: Fase 3 intensifica busca em regiões extremas promissoras
3. **Configurável**: Fácil ajustar sem mudar código
4. **Auditável**: Histórico completo de tentativas
5. **Reproduzível**: Comando exato para reproduzir resultado
6. **Eficiente**: Aproveita todo o tempo disponível
7. **Híbrido Inteligente**: Combina exploração global com refinamento focado

## 💡 Dicas para Windows

### Limpando cache Python no Windows

```powershell
# PowerShell
Get-ChildItem -Path . -Include __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Include *.pyc -Recurse -File | Remove-Item -Force
```

### Executando sem cache

```powershell
python -B executar_otimizacao.py
```

### Verificando versão do Python

```powershell
python --version
```
