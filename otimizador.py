import subprocess
import time
import random
import json
from datetime import datetime
import numpy as np
from config_manager import ConfigManager
import os

class HybridOptimizer:
    def __init__(self, config_path="config.json"):
        self.config_manager = ConfigManager(config_path)
        self.exe_path = self.config_manager.get_modelo_config()['executavel']
        self.timeout = self.config_manager.get_modelo_config()['timeout']
        
        # Inicializa best_value baseado no objetivo
        objetivo = self.config_manager.config.get('objetivo', 'maximizar').lower()
        if objetivo == 'minimizar':
            self.best_value = float('inf')
            self.is_maximizing = False
        else:
            self.best_value = float('-inf')
            self.is_maximizing = True
            
        self.best_params = None
        self.attempts = 0
        self.start_time = time.time()
        self.history = []
        
        # Cria pasta de resultados com data/hora
        self.resultado_dir = self._criar_pasta_resultado()
        
    def _criar_pasta_resultado(self):
        """Cria pasta para salvar resultados da execução"""
        # Cria pasta base 'resultados' se não existir
        base_dir = 'resultados'
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        
        # Cria subpasta com data/hora (formato: tentativa_21-01-2025_1930)
        timestamp = datetime.now().strftime('tentativa_%d-%m-%Y_%H%M')
        resultado_dir = os.path.join(base_dir, timestamp)
        os.makedirs(resultado_dir, exist_ok=True)
        
        print(f"📁 Resultados serão salvos em: {resultado_dir}\n")
        return resultado_dir
        
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
                value = float(output.split()[-1]) if output else (float('inf') if not self.is_maximizing else float('-inf'))
            except:
                value = float('inf') if not self.is_maximizing else float('-inf')
            
            # Verifica se é melhor baseado no objetivo
            is_better = (value > self.best_value) if self.is_maximizing else (value < self.best_value)
            
            if is_better:
                self.best_value = value
                self.best_params = tuple(validated_params)
                objetivo_str = "MAXIMIZAR" if self.is_maximizing else "MINIMIZAR"
                print(f"NOVO MELHOR ({objetivo_str}): {value:.2f} | {self.best_params}")
            
            self.history.append({
                'attempt': self.attempts,
                'params': tuple(validated_params),
                'value': value,
                'time': time.time() - self.start_time
            })
            
            return value
        except Exception as e:
            print(f"Erro na execução: {e}")
            return float('inf') if not self.is_maximizing else float('-inf')
    
    def explore_edges(self):
        """Fase 1: Exploração de bordas"""
        config = self.config_manager.get_fase_config('exploracao_bordas')
        if not config.get('ativo', True):
            print("FASE 1: Exploração de bordas desativada")
            return
        
        print("FASE 1: Explorando bordas...")
        max_time = config.get('tempo_max', 300)
        phase_start = time.time()
        
        # Obtém configurações de teste do config
        edge_configs = config.get('configuracoes_teste', [
            [100, 100, 100, 100, 100],
            [1, 1, 1, 1, 1],
            [100, 1, 100, 1, 100],
            [1, 100, 1, 100, 1],
            [50, 50, 50, 50, 50]
        ])
        
        num_params = len(self.config_manager.config['parametros'])
        
        # Ajusta todas as configurações antecipadamente
        adjusted_configs = []
        for edge_config in edge_configs:
            config_copy = list(edge_config)
            if len(config_copy) < num_params:
                config_copy = config_copy + [50] * (num_params - len(config_copy))
            elif len(config_copy) > num_params:
                config_copy = config_copy[:num_params]
            adjusted_configs.append(config_copy)
        
        # Executa configurações repetidamente até o tempo máximo
        iteration = 0
        while time.time() - phase_start < max_time:
            for edge_config in adjusted_configs:
                if time.time() - phase_start >= max_time:
                    break
                
                # Avalia esta configuração
                self.evaluate(*edge_config)
                iteration += 1
            
            # Log de progresso a cada 10 iterações
            if iteration % 10 == 0:
                elapsed = time.time() - phase_start
                print(f"Explorando bordas - Iteração {iteration} | "
                      f"Tempo: {elapsed:.0f}s/{max_time}s | "
                      f"Melhor: {self.best_value:.2f}")
        
        elapsed = time.time() - phase_start
        print(f"Fase 1 concluída - {iteration} avaliações em {elapsed:.1f}s")
    
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
        phase_start = time.time()
        
        while time.time() - phase_start < max_time:
            iteration += 1
            
            for i in range(n_particles):
                if time.time() - phase_start > max_time:
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
                
                # Verifica se é melhor baseado no objetivo
                is_better = (value > personal_best_values[i]) if self.is_maximizing else (value < personal_best_values[i])
                if is_better:
                    personal_best[i] = particles[i][:]
                    personal_best_values[i] = value
            
            if iteration % 5 == 0:
                elapsed = time.time() - phase_start
                print(f"Iteração {iteration} | Tentativas: {self.attempts} | "
                      f"Tempo: {elapsed:.0f}s | Melhor: {self.best_value:.2f}")
    
    def pso_bordas(self):
        """Fase 3: PSO Focado em Bordas - Híbrido"""
        config = self.config_manager.get_fase_config('pso_bordas')
        if not config.get('ativo', True):
            print("\nFASE 3: PSO Focado em Bordas desativada")
            return
        
        print("\nFASE 3: PSO Focado em Bordas (Híbrido)...")
        
        max_time = config.get('tempo_max', 600)
        n_particles = config.get('num_particulas', 15)
        w = config.get('inercia', 0.4)  # Menor inércia para busca mais local
        c1 = config.get('c1', 2.0)  # Maior componente cognitivo
        c2 = config.get('c2', 1.0)  # Menor componente social
        prob_mutacao = config.get('probabilidade_mutacao', 0.2)
        
        # Identifica regiões de borda promissoras baseadas no melhor resultado
        edge_regions = []
        if self.best_params:
            # Cria variações nas bordas do melhor resultado
            for _ in range(n_particles):
                particle = list(self.best_params)
                # Para cada parâmetro numérico, probabilidade de ir para borda
                for j, param in enumerate(self.config_manager.config['parametros']):
                    if param['tipo'] == 'numerico':
                        if random.random() < 0.4:  # 40% chance de ir para borda
                            particle[j] = random.choice([param['min'], param['max']])
                        else:
                            # Perturbação pequena
                            particle[j] = self.config_manager.clamp_value(
                                param['nome'],
                                particle[j] + random.randint(-10, 10)
                            )
                edge_regions.append(particle)
        else:
            # Se não há melhor resultado, inicializa aleatoriamente em bordas
            for _ in range(n_particles):
                particle = []
                for param in self.config_manager.config['parametros']:
                    if param['tipo'] == 'numerico':
                        # Favorece bordas: 60% min ou max, 40% aleatório
                        if random.random() < 0.6:
                            particle.append(random.choice([param['min'], param['max']]))
                        else:
                            particle.append(random.randint(param['min'], param['max']))
                    else:
                        particle.append(random.choice(param['opcoes']))
                edge_regions.append(particle)
        
        particles = edge_regions
        velocities = []
        personal_best = []
        personal_best_values = []
        
        # Inicializa velocidades e avalia partículas
        for particle in particles:
            velocity = []
            for param in self.config_manager.config['parametros']:
                if param['tipo'] == 'numerico':
                    velocity.append(random.uniform(-5, 5))  # Velocidade menor
                else:
                    velocity.append(0)
            velocities.append(velocity)
            
            value = self.evaluate(*particle)
            personal_best.append(particle[:])
            personal_best_values.append(value)
        
        iteration = 0
        phase_start = time.time()
        
        while time.time() - phase_start < max_time:
            iteration += 1
            
            for i in range(n_particles):
                if time.time() - phase_start > max_time:
                    break
                
                # Atualiza partículas numéricas com PSO
                for j, param in enumerate(self.config_manager.config['parametros']):
                    if param['tipo'] == 'numerico':
                        r1, r2 = random.random(), random.random()
                        velocities[i][j] = (w * velocities[i][j] + 
                                           c1 * r1 * (personal_best[i][j] - particles[i][j]) +
                                           c2 * r2 * (self.best_params[j] - particles[i][j]))
                        
                        new_pos = int(particles[i][j] + velocities[i][j])
                        particles[i][j] = self.config_manager.clamp_value(param['nome'], new_pos)
                        
                        # Ocasionalmente força para bordas
                        if random.random() < 0.15:
                            particles[i][j] = random.choice([param['min'], param['max']])
                
                # Mutação para parâmetros categóricos
                for j, param in enumerate(self.config_manager.config['parametros']):
                    if param['tipo'] == 'categorico' and random.random() < prob_mutacao:
                        particles[i][j] = self.config_manager.get_random_value(param['nome'])
                
                value = self.evaluate(*particles[i])
                
                if value > personal_best_values[i]:
                    personal_best[i] = particles[i][:]
                    personal_best_values[i] = value
            
            if iteration % 3 == 0:
                elapsed = time.time() - phase_start
                print(f"Iteração {iteration} | Tentativas fase: {self.attempts - sum(1 for h in self.history if h['time'] < self.history[-1]['time'] - elapsed)} | "
                      f"Tempo fase: {elapsed:.0f}s | Melhor global: {self.best_value:.2f}")
    
    def generate_report(self):
        elapsed_time = time.time() - self.start_time
        
        # Gera informações sobre parâmetros
        params_info = ""
        for i, (param, value) in enumerate(zip(self.config_manager.config['parametros'], self.best_params)):
            tipo_desc = f"({param['tipo']})"
            if param['tipo'] == 'numerico':
                tipo_desc = f"({param['min']}-{param['max']})"
            params_info += f"  {param['nome']:4} {tipo_desc:12}: {value}\n"
        
        objetivo_str = "MAXIMIZAR" if self.is_maximizing else "MINIMIZAR"
        
        report = f"""
═══════════════════════════════════════════════════════════════
                    RELATÓRIO DE OTIMIZAÇÃO
═══════════════════════════════════════════════════════════════

PASTA DE RESULTADOS: {self.resultado_dir}

OBJETIVO: {objetivo_str}

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
2. PSO GLOBAL: {self.config_manager.get_fase_config('pso').get('tempo_max', 0)/60:.1f} min
3. PSO FOCADO EM BORDAS: {self.config_manager.get_fase_config('pso_bordas').get('tempo_max', 0)/60:.1f} min

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
        
        # Salva arquivos na pasta de resultados
        relatorio_path = os.path.join(self.resultado_dir, 'relatorio_otimizacao.txt')
        historico_path = os.path.join(self.resultado_dir, 'historico_otimizacao.json')
        config_path = os.path.join(self.resultado_dir, 'config_utilizada.json')
        
        with open(relatorio_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        with open(historico_path, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2)
        
        # Salva cópia da configuração utilizada
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config_manager.config, f, indent=2, ensure_ascii=False)
        
        # Cria arquivo resumo com melhor resultado
        resumo_path = os.path.join(self.resultado_dir, 'resumo.txt')
        with open(resumo_path, 'w', encoding='utf-8') as f:
            f.write(f"MELHOR VALOR: {self.best_value:.6f}\n")
            f.write(f"TENTATIVAS: {self.attempts}\n")
            f.write(f"TEMPO: {elapsed_time/60:.2f} min\n")
            f.write(f"COMANDO: {self.exe_path} {' '.join(str(p) for p in self.best_params)}\n")
        
        print(f"\n📄 Arquivos salvos em: {self.resultado_dir}/")
        print(f"  ✓ relatorio_otimizacao.txt")
        print(f"  ✓ historico_otimizacao.json")
        print(f"  ✓ config_utilizada.json")
        print(f"  ✓ resumo.txt")
        
        return report