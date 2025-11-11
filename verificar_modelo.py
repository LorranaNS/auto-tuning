#!/usr/bin/env python3
"""
Verifica se o modelo10.exe está funcionando corretamente
"""
import subprocess
import os

def testar_modelo():
    print("=" * 60)
    print("   VERIFICAÇÃO DO MODELO10.EXE")
    print("=" * 60)
    
    # Verifica se arquivo existe
    if not os.path.exists('./modelo10.exe'):
        print("❌ ERRO: modelo10.exe não encontrado!")
        print("   Certifique-se que o arquivo está no diretório atual")
        return False
    
    print("✓ Arquivo modelo10.exe encontrado\n")
    
    # Verifica se é executável
    if not os.access('./modelo10.exe', os.X_OK):
        print("⚠️  Arquivo não é executável. Tornando executável...")
        os.chmod('./modelo10.exe', 0o755)
        print("✓ Permissões ajustadas\n")
    
    # Testa execuções
    print("Testando execuções do modelo:\n")
    
    testes = [
        ["baixo", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
        ["medio", "50", "50", "50", "50", "50", "50", "50", "50", "50"],
        ["alto", "100", "100", "100", "100", "100", "100", "100", "100", "100"],
    ]
    
    sucesso = 0
    for i, params in enumerate(testes, 1):
        try:
            cmd = ["./modelo10.exe"] + params
            print(f"Teste {i}: {' '.join(params)}")
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                print(f"  ✓ Saída: {output}")
                
                # Tenta extrair valor numérico
                try:
                    valor = float(output.split()[-1])
                    print(f"  ✓ Valor extraído: {valor}")
                    sucesso += 1
                except:
                    print(f"  ⚠️  Não foi possível extrair valor numérico")
            else:
                print(f"  ❌ Código de retorno: {result.returncode}")
                if result.stderr:
                    print(f"  Erro: {result.stderr}")
            
            print()
            
        except subprocess.TimeoutExpired:
            print(f"  ❌ Timeout (mais de 10 segundos)")
            print()
        except Exception as e:
            print(f"  ❌ Erro: {e}")
            print()
    
    print("=" * 60)
    print(f"Resultado: {sucesso}/{len(testes)} testes bem-sucedidos")
    print("=" * 60)
    
    if sucesso == len(testes):
        print("\n✅ TUDO OK! O modelo está funcionando corretamente.")
        print("   Você pode executar: python executar_otimizacao.py")
        return True
    else:
        print("\n⚠️  Alguns testes falharam. Verifique o modelo.")
        return False

if __name__ == "__main__":
    testar_modelo()
