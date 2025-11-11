import subprocess
import time
import random
import json
from datetime import datetime
import numpy as np
from config_manager import ConfigManager

class HybridOptimizer:
    def __init__(self, config_path="config.json"):
        self.config_manager = ConfigManager(config_path)
        self.exe_path = self.config_manager.get_modelo_config()['executavel']
        self.timeout = self.config_manager.get_modelo_config()['timeout']
        self.best_value = float('-inf')
        self.best_params = None
        self.attempts = 0
        self.start_time = time.time()
        self.history = []
        
    def evaluate(self, *params):
        """Avalia uma configuração de parâmetros"""
        try:
            # Valida e ajusta os parâmetros
            validated_params = []
            for i, (param_config, value) in enumerate(zip(self.config_manager.config['parametros'], params)):
                validated_params.append(
                    self.config_manager.clamp_value(param_config['nome'], value)
                )
            
            cmd = [self.exe_path] + [str(p) for p in validated_params]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)
            self.attempts += 1
            
            output = result.stdout.strip()
            try:
                value = float(output.split()[-1]) if output else float('-inf')
            except:
                value = float('-inf')
            
            if value > self.best_value:
                self.best_value = value
                self.best_params = tuple(validated_params)
                print(f"NOVO MELHOR: {value:.2f} | {self.best_params}")
            
            self.history.append({
                'attempt': self.attempts,
                'params': tuple(validated_params),
                'value': value,
                'time': time.time() - self.start_time
            })
            
            return value
        except Exception as e:
            print(f"Erro na execução: {e}")
            return float('-inf')
    
    def explore_edges(self):
        """Fase 1: Exploração de bordas"""
        config = self.config_manager.get_fase_config('exploracao_bordas')
        if not config.get('ativo', True):
            print("FASE 1: Exploração de bordas desativada")
            return
        
        print("FASE 1: Explorando bordas...")
        max_time = config.get('tempo_max', 300)
        
        # Obtém opções do primeiro parâmetro categórico
        categoricos = self.config_manager.get_categorico_params()
        x1_options = categoricos[0]['opcoes'] if categoricos else ['baixo']
        
        edge_configs = config.get('configuracoes_teste', [[100, 100], [1, 1]])
        numericos = self.config_manager.get_numerico_params()
        num_params_restantes = len(numericos) - 2  # -2 porque x2 e x3 vêm das edge_configs
        
        for x1 in x1_options:
            for x2, x3 in edge_configs:
                if time.time() - self.start_time > max_time:
                    return
                
                for config_values in [[100]*num_params_restantes, [0]*num_params_restantes, 
                                      [50]*num_params_restantes]:
                    if time.time() - self.start_time > max_time:
                        return
                    self.evaluate(x1, x2, x3, *config_values)
    
    def pso_optimize(self):
        """Fase 2: PSO"""
        config = self.config_manager.get_fase_config('pso')
        if not config.get('ativo', True):
            print("\nFASE 2: PSO desativada")
            return
        
        print("\nFASE 2: PSO...")
        
        max_time = config.get('tempo_max', 1200)
        n_particles = config.get('num_particulas', 20)
        w = config.get('inercia', 0.7)
        c1 = config.get('c1', 1.5)
        c2 = config.get('c2', 1.5)
        prob_mutacao = config.get('probabilidade_mutacao', 0.1)
        
        categoricos = self.config_manager.get_categorico_params()
        numericos = self.config_manager.get_numerico_params()
        
        particles = []
        velocities = []
        personal_best = []
        personal_best_values = []
        
        for _ in range(n_particles):
            particle = []
            velocity = []
            
            # Inicializa partículas baseado na configuração
            for param in self.config_manager.config['parametros']:
                particle.append(self.config_manager.get_random_value(param['nome']))
                if param['tipo'] == 'numerico':
                    velocity.append(random.uniform(-10, 10))
                else:
                    velocity.append(0)
            
            particles.append(particle)
            velocities.append(velocity)
            
            value = self.evaluate(*particle)
            personal_best.append(particle[:])
            personal_best_values.append(value)
        
        iteration = 0
        while time.time() - self.start_time < max_time:
            iteration += 1
            
            for i in range(n_particles):
                if time.time() - self.start_time > max_time:
                    break
                
                # Atualiza partículas numéricas
                for j, param in enumerate(self.config_manager.config['parametros']):
                    if param['tipo'] == 'numerico':
                        r1, r2 = random.random(), random.random()
                        velocities[i][j] = (w * velocities[i][j] + 
                                           c1 * r1 * (personal_best[i][j] - particles[i][j]) +
                                           c2 * r2 * (self.best_params[j] - particles[i][j]))
                        
                        particles[i][j] = self.config_manager.clamp_value(
                            param['nome'], 
                            int(particles[i][j] + velocities[i][j])
                        )
                
                # Mutação para parâmetros categóricos
                for j, param in enumerate(self.config_manager.config['parametros']):
                    if param['tipo'] == 'categorico' and random.random() < prob_mutacao:
                        particles[i][j] = self.config_manager.get_random_value(param['nome'])
                
                value = self.evaluate(*particles[i])
                
                if value > personal_best_values[i]:
                    personal_best[i] = particles[i][:]
                    personal_best_values[i] = value
            
            if iteration % 5 == 0:
                elapsed = time.time() - self.start_time
                print(f"Iteração {iteration} | Tentativas: {self.attempts} | "
                      f"Tempo: {elapsed:.0f}s | Melhor: {self.best_value:.2f}")
    
    def local_search(self):
        """Fase 3: Busca local"""
        config = self.config_manager.get_fase_config('busca_local')
        if not config.get('ativo', True):
            print("\nFASE 3: Busca local desativada")
            return
        
        print("\nFASE 3: Busca local...")
        
        if self.best_params is None:
            return
        
        max_time = config.get('tempo_max', 300)
        deltas = config.get('deltas', [-5, -2, -1, 0, 1, 2, 5])
        
        # Busca local em parâmetros numéricos
        for dx in deltas:
            for i, param in enumerate(self.config_manager.config['parametros']):
                if time.time() - self.start_time > max_time:
                    return
                
                if param['tipo'] == 'numerico':
                    params = list(self.best_params)
                    params[i] = self.config_manager.clamp_value(
                        param['nome'], 
                        params[i] + dx
                    )
                    self.evaluate(*params)
        
        # Testa variações de parâmetros categóricos
        for i, param in enumerate(self.config_manager.config['parametros']):
            if param['tipo'] == 'categorico':
                for opcao in param['opcoes']:
                    if time.time() - self.start_time > max_time:
                        return
                    params = list(self.best_params)
                    params[i] = opcao
                    self.evaluate(*params)
    
    def generate_report(self):
        elapsed_time = time.time() - self.start_time
        
        # Gera informações sobre parâmetros
        params_info = ""
        for i, (param, value) in enumerate(zip(self.config_manager.config['parametros'], self.best_params)):
            tipo_desc = f"({param['tipo']})"
            if param['tipo'] == 'numerico':
                tipo_desc = f"({param['min']}-{param['max']})"
            params_info += f"  {param['nome']:4} {tipo_desc:12}: {value}\n"
        
        report = f"""
═══════════════════════════════════════════════════════════════
                    RELATÓRIO DE OTIMIZAÇÃO
═══════════════════════════════════════════════════════════════

CONFIGURAÇÃO:
-------------
Arquivo de configuração: {self.config_manager.config_path}
Número de parâmetros: {self.config_manager.get_num_params()}
Parâmetros categóricos: {len(self.config_manager.get_categorico_params())}
Parâmetros numéricos: {len(self.config_manager.get_numerico_params())}

ESTRATÉGIA UTILIZADA:
--------------------
Abordagem Híbrida configurável com três fases:

1. EXPLORAÇÃO DE BORDAS: {self.config_manager.get_fase_config('exploracao_bordas').get('tempo_max', 0)/60:.1f} min
2. PARTICLE SWARM OPTIMIZATION (PSO): {self.config_manager.get_fase_config('pso').get('tempo_max', 0)/60:.1f} min
3. BUSCA LOCAL REFINADA: {self.config_manager.get_fase_config('busca_local').get('tempo_max', 0)/60:.1f} min

RESULTADOS:
-----------
Tempo de execução: {elapsed_time/60:.2f} minutos ({elapsed_time:.1f} segundos)
Número de tentativas: {self.attempts}
Taxa de avaliação: {self.attempts/elapsed_time:.2f} tentativas/segundo

MELHOR RESULTADO ENCONTRADO:
-----------------------------
Valor: {self.best_value:.6f}

Parâmetros:
{params_info}
Comando para reproduzir:
{self.exe_path} {' '.join(str(p) for p in self.best_params)}

═══════════════════════════════════════════════════════════════
Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
═══════════════════════════════════════════════════════════════
"""
        
        print(report)
        
        with open('relatorio_otimizacao.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        with open('historico_otimizacao.json', 'w') as f:
            json.dump(self.history, f, indent=2)
        
        return report