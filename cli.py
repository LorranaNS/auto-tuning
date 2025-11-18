import questionary
from questionary import Style
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box
import json
import os
from config_manager import ConfigManager

console = Console()

# Estilo personalizado para questionary
custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),       # Ícone de pergunta (?)
    ('question', 'bold'),                # Texto da pergunta
    ('answer', 'fg:#f44336 bold'),      # Resposta selecionada
    ('pointer', 'fg:#673ab7 bold'),     # Ponteiro (seta)
    ('highlighted', 'fg:#673ab7 bold'), # Item destacado
    ('selected', 'fg:#cc5454'),         # Item selecionado (checkboxes)
    ('separator', 'fg:#cc5454'),        # Separador
    ('instruction', ''),                # Instruções
    ('text', ''),                       # Texto normal
    ('disabled', 'fg:#858585 italic')   # Texto desabilitado
])

# Configuração de ponteiros personalizados
custom_pointer = '➤'  # Opções: ➤, ▶, →, ►, ❯, »
# Outras opções de setas: '▸', '▶', '➜', '⟩', '❱', '▻'

def print_banner():
    """Exibe banner inicial"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🚀  OTIMIZAÇÃO HÍBRIDA - PESQUISA OPERACIONAL  🚀      ║
    ║                                                           ║
    ║           Sistema de Otimização com PSO Híbrido           ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")

def print_section_header(title):
    """Exibe cabeçalho de seção"""
    console.print(f"\n[bold yellow]{'='*60}[/bold yellow]")
    console.print(f"[bold yellow]{title.center(60)}[/bold yellow]")
    console.print(f"[bold yellow]{'='*60}[/bold yellow]\n")

def configurar_parametros():
    """Configuração interativa de parâmetros"""
    print_section_header("CONFIGURAÇÃO DE PARÂMETROS")
    
    # Pergunta quantidade de parâmetros
    num_params = questionary.text(
        "Quantos parâmetros o modelo possui?",
        default="10",
        validate=lambda x: x.isdigit() and int(x) > 0,
        style=custom_style
    ).ask()
    
    if num_params is None:
        return None
    
    num_params = int(num_params)
    parametros = []
    
    console.print(f"\n[green]✓[/green] Configurando {num_params} parâmetros...\n")
    
    for i in range(num_params):
        console.print(f"[bold cyan]Parâmetro {i+1}:[/bold cyan]")
        
        # Nome do parâmetro
        nome = questionary.text(
            f"  Nome:",
            default=f"x{i+1}",
            style=custom_style
        ).ask()
        
        if nome is None:
            return None
        
        # Tipo do parâmetro
        tipo = questionary.select(
            f"  Tipo do parâmetro '{nome}':",
            choices=[
                questionary.Choice("Numérico (inteiro com limites)", value="numerico"),
                questionary.Choice("Categórico (texto com opções)", value="categorico")
            ],
            style=custom_style,
            pointer=custom_pointer
        ).ask()
        
        if tipo is None:
            return None
        
        param_config = {
            "nome": nome,
            "tipo": tipo
        }
        
        if tipo == "numerico":
            # Configuração numérica
            min_val = questionary.text(
                f"  Valor mínimo:",
                default="1",
                validate=lambda x: x.lstrip('-').isdigit(),
                style=custom_style
            ).ask()
            
            if min_val is None:
                return None
            
            max_val = questionary.text(
                f"  Valor máximo:",
                default="100",
                validate=lambda x: x.lstrip('-').isdigit() and int(x) >= int(min_val),
                style=custom_style
            ).ask()
            
            if max_val is None:
                return None
            
            param_config["min"] = int(min_val)
            param_config["max"] = int(max_val)
            param_config["descricao"] = f"Parâmetro numérico {i+1}"
            
        else:  # categorico
            # Configuração categórica
            console.print(f"  [yellow]Digite as opções separadas por vírgula (ex: baixo,medio,alto):[/yellow]")
            opcoes_str = questionary.text(
                f"  Opções:",
                default="baixo,medio,alto",
                style=custom_style
            ).ask()
            
            if opcoes_str is None:
                return None
            
            opcoes = [opt.strip() for opt in opcoes_str.split(',')]
            param_config["opcoes"] = opcoes
            param_config["descricao"] = f"Parâmetro categórico {i+1}"
        
        parametros.append(param_config)
        console.print(f"[green]  ✓ Parâmetro '{nome}' configurado![/green]\n")
    
    return parametros

def configurar_fases():
    """Configuração interativa das fases de otimização"""
    print_section_header("CONFIGURAÇÃO DAS FASES")
    
    fases = {}
    
    # FASE 1: Exploração de Bordas
    console.print("[bold cyan]FASE 1: Exploração de Bordas[/bold cyan]")
    fase1_ativa = questionary.confirm(
        "Ativar Fase 1 (Exploração de Bordas)?",
        default=True,
        style=custom_style
    ).ask()
    
    if fase1_ativa is None:
        return None
    
    tempo1 = 300
    if fase1_ativa:
        tempo1_input = questionary.text(
            "Tempo máximo em segundos:",
            default="300",
            validate=lambda x: x.isdigit() and int(x) > 0,
            style=custom_style
        ).ask()
        
        if tempo1_input is None:
            return None
        tempo1 = int(tempo1_input)
    
    fases["exploracao_bordas"] = {
        "ativo": fase1_ativa,
        "tempo_max": tempo1,
        "configuracoes_teste": [[100, 100], [1, 1], [100, 1], [1, 100], [50, 50]]
    }
    
    # FASE 2: PSO Global
    console.print("\n[bold cyan]FASE 2: PSO Global[/bold cyan]")
    fase2_ativa = questionary.confirm(
        "Ativar Fase 2 (PSO Global)?",
        default=True,
        style=custom_style
    ).ask()
    
    if fase2_ativa is None:
        return None
    
    tempo2 = 2700
    num_particulas = 30
    if fase2_ativa:
        tempo2_input = questionary.text(
            "Tempo máximo em segundos:",
            default="2700",
            validate=lambda x: x.isdigit() and int(x) > 0,
            style=custom_style
        ).ask()
        
        if tempo2_input is None:
            return None
        tempo2 = int(tempo2_input)
        
        num_particulas_input = questionary.text(
            "Número de partículas:",
            default="30",
            validate=lambda x: x.isdigit() and int(x) > 0,
            style=custom_style
        ).ask()
        
        if num_particulas_input is None:
            return None
        num_particulas = int(num_particulas_input)
    
    fases["pso"] = {
        "ativo": fase2_ativa,
        "tempo_max": tempo2,
        "num_particulas": num_particulas,
        "inercia": 0.7,
        "c1": 1.5,
        "c2": 1.5,
        "probabilidade_mutacao": 0.15
    }
    
    # FASE 3: PSO Focado em Bordas
    console.print("\n[bold cyan]FASE 3: PSO Focado em Bordas[/bold cyan]")
    fase3_ativa = questionary.confirm(
        "Ativar Fase 3 (PSO Focado em Bordas)?",
        default=True,
        style=custom_style
    ).ask()
    
    if fase3_ativa is None:
        return None
    
    tempo3 = 600
    if fase3_ativa:
        tempo3_input = questionary.text(
            "Tempo máximo em segundos:",
            default="600",
            validate=lambda x: x.isdigit() and int(x) > 0,
            style=custom_style
        ).ask()
        
        if tempo3_input is None:
            return None
        tempo3 = int(tempo3_input)
    
    fases["pso_bordas"] = {
        "ativo": fase3_ativa,
        "tempo_max": tempo3,
        "num_particulas": 15,
        "inercia": 0.4,
        "c1": 2.0,
        "c2": 1.0,
        "probabilidade_mutacao": 0.2
    }
    
    console.print(f"\n[green]✓ Fases configuradas![/green]")
    return fases

def criar_config_completa(parametros, fases, objetivo, executavel):
    """Cria configuração completa"""
    config = {
        "objetivo": objetivo,
        "modelo": {
            "executavel": executavel,
            "timeout": 10
        },
        "parametros": parametros,
        "otimizacao": {
            "fases": fases,
            "tempo_total_max": sum(f.get("tempo_max", 0) for f in fases.values())
        }
    }
    return config

def mostrar_resumo_config(config):
    """Mostra resumo da configuração"""
    print_section_header("RESUMO DA CONFIGURAÇÃO")
    
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("Item", style="cyan", width=30)
    table.add_column("Valor", style="green")
    
    table.add_row("Objetivo", config.get("objetivo", "maximizar").upper())
    table.add_row("Executável", config["modelo"]["executavel"])
    table.add_row("Número de parâmetros", str(len(config["parametros"])))
    
    # Parâmetros
    categoricos = sum(1 for p in config["parametros"] if p["tipo"] == "categorico")
    numericos = sum(1 for p in config["parametros"] if p["tipo"] == "numerico")
    table.add_row("  - Categóricos", str(categoricos))
    table.add_row("  - Numéricos", str(numericos))
    
    # Fases
    fases = config["otimizacao"]["fases"]
    for nome_fase, conf in fases.items():
        nome_display = nome_fase.replace('_', ' ').title()
        status = "✓ Ativa" if conf.get("ativo", False) else "✗ Desativada"
        tempo = f"{conf.get('tempo_max', 0)/60:.1f} min" if conf.get("ativo", False) else "-"
        table.add_row(f"{nome_display}", f"{status} ({tempo})")
    
    tempo_total = config["otimizacao"]["tempo_total_max"]
    table.add_row("Tempo total estimado", f"{tempo_total/60:.1f} minutos")
    
    console.print(table)
    console.print()

def run_cli():
    """Função principal da CLI"""
    print_banner()
    
    # Menu principal
    modo = questionary.select(
        "Como deseja configurar a otimização?",
        choices=[
            questionary.Choice("📁 Usar configuração do arquivo (config.json)", value="arquivo"),
            questionary.Choice("⚙️  Definir parâmetros manualmente agora", value="manual"),
            questionary.Choice("🚪 Sair", value="sair")
        ],
        style=custom_style,
        pointer=custom_pointer
    ).ask()
    
    if modo is None or modo == "sair":
        console.print("\n[yellow]Operação cancelada.[/yellow]")
        return None
    
    config = None
    
    if modo == "arquivo":
        # Carregar do arquivo
        arquivo = questionary.text(
            "Caminho do arquivo de configuração:",
            default="config.json",
            style=custom_style
        ).ask()
        
        if arquivo is None:
            return None
        
        if not os.path.exists(arquivo):
            console.print(f"\n[red]✗ Arquivo '{arquivo}' não encontrado![/red]")
            return None
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                config = json.load(f)
            console.print(f"\n[green]✓ Configuração carregada de '{arquivo}'[/green]")
        except Exception as e:
            console.print(f"\n[red]✗ Erro ao carregar arquivo: {e}[/red]")
            return None
    
    else:  # manual
        # Objetivo
        objetivo = questionary.select(
            "\nQual o objetivo da otimização?",
            choices=[
                questionary.Choice("📈 Maximizar (buscar o maior valor)", value="maximizar"),
                questionary.Choice("📉 Minimizar (buscar o menor valor)", value="minimizar")
            ],
            style=custom_style,
            pointer=custom_pointer
        ).ask()
        
        if objetivo is None:
            return None
        
        # Caminho do executável
        executavel = questionary.text(
            "Caminho do executável do modelo:",
            default="./modelo10.exe",
            style=custom_style
        ).ask()
        
        if executavel is None:
            return None
        
        # Configurar parâmetros
        parametros = configurar_parametros()
        if parametros is None:
            return None
        
        # Configurar fases
        fases = configurar_fases()
        if fases is None:
            return None
        
        # Criar config
        config = criar_config_completa(parametros, fases, objetivo, executavel)
        
        # Salvar configuração
        salvar = questionary.confirm(
            "\nDeseja salvar esta configuração em um arquivo?",
            default=True,
            style=custom_style
        ).ask()
        
        if salvar:
            nome_arquivo = questionary.text(
                "Nome do arquivo:",
                default="config_custom.json",
                style=custom_style
            ).ask()
            
            if nome_arquivo:
                try:
                    with open(nome_arquivo, 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=2, ensure_ascii=False)
                    console.print(f"\n[green]✓ Configuração salva em '{nome_arquivo}'[/green]")
                except Exception as e:
                    console.print(f"\n[yellow]⚠ Não foi possível salvar: {e}[/yellow]")
    
    # Mostrar resumo
    mostrar_resumo_config(config)
    
    # Confirmação final
    confirmar = questionary.confirm(
        "Deseja iniciar a otimização com esta configuração?",
        default=True,
        style=custom_style
    ).ask()
    
    if not confirmar:
        console.print("\n[yellow]Operação cancelada.[/yellow]")
        return None
    
    console.print("\n[bold green]🚀 Iniciando otimização...[/bold green]\n")
    return config

if __name__ == "__main__":
    config = run_cli()
    if config:
        console.print("[bold]Configuração pronta para uso![/bold]")
