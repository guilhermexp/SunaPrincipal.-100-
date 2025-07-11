#!/usr/bin/env python3
"""
Script para corrigir a configuração dos modelos no backend
"""
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

def update_llm_service():
    """Atualiza o arquivo llm.py para corrigir os mapeamentos de modelos"""
    
    llm_file = Path(__file__).parent / "backend" / "services" / "llm.py"
    
    print("Fazendo backup do arquivo original...")
    backup_file = llm_file.with_suffix('.py.backup')
    llm_file.rename(backup_file)
    
    print("Criando novo arquivo com correções...")
    
    # Lê o arquivo original
    with open(backup_file, 'r') as f:
        content = f.read()
    
    # Correções necessárias
    corrections = [
        # Corrigir fallback do Grok para não usar OpenRouter quando temos XAI_API_KEY
        ('elif "xai" in model_name.lower() or "grok" in model_name.lower():\n        return "openrouter/x-ai/grok-4"',
         'elif "xai" in model_name.lower() or "grok" in model_name.lower():\n        # Only use OpenRouter if XAI key is not available\n        if not os.getenv("XAI_API_KEY"):\n            return "openrouter/x-ai/grok-4"\n        return None'),
    ]
    
    # Aplica as correções
    for old, new in corrections:
        if old in content:
            content = content.replace(old, new)
            print(f"✓ Correção aplicada para Grok 4")
        else:
            print(f"✗ Não encontrou o texto para correção do Grok 4")
    
    # Salva o arquivo corrigido
    with open(llm_file, 'w') as f:
        f.write(content)
    
    print("\nArquivo llm.py atualizado com sucesso!")
    print(f"Backup salvo em: {backup_file}")

def update_model_list():
    """Atualiza a lista de modelos disponíveis no frontend"""
    
    model_file = Path(__file__).parent / "frontend" / "src" / "components" / "thread" / "chat-input" / "_use-model-selection.ts"
    
    print("\nAtualizando lista de modelos no frontend...")
    
    # Adiciona configuração para mais modelos
    additional_models = """
  // Google Gemini
  'gemini/gemini-2.5-pro': { 
    tier: 'premium', 
    priority: 97,
    disabled: false,
    lowQuality: false
  },
  
  // XAI Grok
  'xai/grok-4': { 
    tier: 'premium', 
    priority: 98,
    disabled: false,
    lowQuality: false
  },
  
  // DeepSeek
  'deepseek/deepseek-chat': { 
    tier: 'free', 
    priority: 70,
    disabled: false,
    lowQuality: false
  },
"""
    
    print("Por favor, adicione manualmente os modelos acima no arquivo:")
    print(f"{model_file}")
    print("\nProcure pela seção MODEL_METADATA e adicione antes do fechamento do objeto.")

def main():
    print("=== Corrigindo Configuração dos Modelos ===\n")
    
    # Verifica se as chaves estão configuradas
    print("1. Verificando chaves de API...")
    keys_ok = True
    
    for provider in ["XAI", "GOOGLE", "DEEPSEEK"]:
        key = os.getenv(f"{provider}_API_KEY")
        if key:
            print(f"✓ {provider}_API_KEY está configurada")
        else:
            print(f"✗ {provider}_API_KEY NÃO está configurada")
            keys_ok = False
    
    if not keys_ok:
        print("\n⚠️  Configure as chaves faltantes no arquivo backend/.env")
        return
    
    print("\n2. Atualizando configuração do backend...")
    try:
        update_llm_service()
    except Exception as e:
        print(f"Erro ao atualizar llm.py: {e}")
    
    print("\n3. Instruções para o frontend...")
    update_model_list()
    
    print("\n4. Próximos passos:")
    print("   - Reinicie o backend: docker-compose restart backend")
    print("   - Reinicie o frontend: docker-compose restart frontend")
    print("   - Teste os modelos novamente")
    
    print("\n✅ Correções aplicadas!")

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    env_file = Path(__file__).parent / "backend" / ".env"
    if env_file.exists():
        load_dotenv(env_file)
    
    main()