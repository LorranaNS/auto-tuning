import json
import random

class ConfigManager:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.load_config()
    
    def load_config(self):
        """Carrega a configuração do arquivo JSON"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
    
    def save_config(self):
        """Salva a configuração atual no arquivo JSON"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def get_param_config(self, param_name):
        """Retorna a configuração de um parâmetro específico"""
        for param in self.config['parametros']:
            if param['nome'] == param_name:
                return param
        return None
    
    def get_num_params(self):
        """Retorna o número total de parâmetros"""
        return len(self.config['parametros'])
    
    def get_categorico_params(self):
        """Retorna lista de parâmetros categóricos"""
        return [p for p in self.config['parametros'] if p['tipo'] == 'categorico']
    
    def get_numerico_params(self):
        """Retorna lista de parâmetros numéricos"""
        return [p for p in self.config['parametros'] if p['tipo'] == 'numerico']
    
    def get_random_value(self, param_name):
        """Gera um valor aleatório válido para o parâmetro"""
        param = self.get_param_config(param_name)
        if param is None:
            return None
        
        if param['tipo'] == 'categorico':
            return random.choice(param['opcoes'])
        else:  # numérico
            return random.randint(param['min'], param['max'])
    
    def validate_value(self, param_name, value):
        """Valida se um valor está dentro dos limites do parâmetro"""
        param = self.get_param_config(param_name)
        if param is None:
            return False
        
        if param['tipo'] == 'categorico':
            return value in param['opcoes']
        else:  # numérico
            return param['min'] <= value <= param['max']
    
    def clamp_value(self, param_name, value):
        """Ajusta o valor para ficar dentro dos limites"""
        param = self.get_param_config(param_name)
        if param is None:
            return value
        
        if param['tipo'] == 'categorico':
            if value not in param['opcoes']:
                return param['opcoes'][0]
            return value
        else:  # numérico
            return max(param['min'], min(param['max'], int(value)))
    
    def get_modelo_config(self):
        """Retorna configuração do modelo"""
        return self.config['modelo']
    
    def get_otimizacao_config(self):
        """Retorna configuração de otimização"""
        return self.config['otimizacao']
    
    def get_fase_config(self, fase_nome):
        """Retorna configuração de uma fase específica"""
        return self.config['otimizacao']['fases'].get(fase_nome, {})
