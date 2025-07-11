#!/usr/bin/env python3
"""
Script para testar a configuração de todos os modelos LLM
"""
import os
import sys
import asyncio
from pathlib import Path
import litellm

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Load environment variables
from dotenv import load_dotenv
env_file = Path(__file__).parent / "backend" / ".env"
if env_file.exists():
    load_dotenv(env_file)

async def test_models():
    print("=== Testando Configuração dos Modelos LLM ===\n")
    
    # Lista de modelos para testar
    models_to_test = [
        # Google
        ("google/gemini-2.5-pro", "GOOGLE_API_KEY", "Gemini 2.5 Pro"),
        ("gemini/gemini-2.5-pro", "GOOGLE_API_KEY", "Gemini 2.5 Pro (alternate)"),
        
        # OpenAI
        ("gpt-4o", "OPENAI_API_KEY", "GPT-4o"),
        ("gpt-4o-mini", "OPENAI_API_KEY", "GPT-4o Mini"),
        
        # Anthropic
        ("claude-sonnet-4", "ANTHROPIC_API_KEY", "Claude Sonnet 4"),
        ("anthropic/claude-sonnet-4-20250514", "ANTHROPIC_API_KEY", "Claude Sonnet 4 (full name)"),
        
        # XAI (Grok)
        ("xai/grok-4", "XAI_API_KEY", "Grok 4"),
        ("grok-4", "XAI_API_KEY", "Grok 4 (short)"),
        
        # Groq
        ("groq/llama3-70b-8192", "GROQ_API_KEY", "Groq Llama 3 70B"),
        
        # DeepSeek
        ("deepseek/deepseek-v3", "DEEPSEEK_API_KEY", "DeepSeek V3"),
        
        # Perplexity
        ("perplexity/llama-3.1-sonar-large-128k-chat", "PPLX_API_KEY", "Perplexity Sonar"),
        
        # OpenRouter fallbacks
        ("openrouter/x-ai/grok-4", "OPENROUTER_API_KEY", "Grok 4 via OpenRouter"),
        ("openrouter/google/gemini-2.5-pro", "OPENROUTER_API_KEY", "Gemini 2.5 Pro via OpenRouter"),
    ]
    
    print("1. Verificando chaves de API...\n")
    api_keys = {}
    for provider in ["OPENAI", "ANTHROPIC", "GOOGLE", "XAI", "GROQ", "DEEPSEEK", "PPLX", "OPENROUTER"]:
        key = os.getenv(f"{provider}_API_KEY")
        api_keys[provider] = bool(key)
        if key:
            print(f"✓ {provider}_API_KEY: Configurada ({key[:20]}...)")
        else:
            print(f"✗ {provider}_API_KEY: NÃO configurada")
    
    print("\n2. Testando modelos...\n")
    
    for model_name, required_key, description in models_to_test:
        provider = required_key.replace("_API_KEY", "")
        
        print(f"Testando: {description} ({model_name})")
        
        # Verifica se a chave necessária está configurada
        if not api_keys.get(provider):
            print(f"  ✗ Pulando - {required_key} não está configurada\n")
            continue
        
        try:
            # Testa uma chamada simples
            response = await litellm.acompletion(
                model=model_name,
                messages=[{"role": "user", "content": "Diga apenas 'OK' se você está funcionando."}],
                max_tokens=10,
                temperature=0
            )
            
            if response and response.choices and response.choices[0].message.content:
                print(f"  ✓ FUNCIONANDO! Resposta: {response.choices[0].message.content.strip()}")
                print(f"  ✓ Modelo usado: {response.model}")
            else:
                print(f"  ✗ Resposta vazia ou inválida")
                
        except Exception as e:
            error_msg = str(e)
            if "Invalid API Key" in error_msg:
                print(f"  ✗ ERRO: Chave de API inválida")
            elif "rate limit" in error_msg.lower():
                print(f"  ✗ ERRO: Limite de taxa atingido")
            elif "not found" in error_msg.lower():
                print(f"  ✗ ERRO: Modelo não encontrado")
            else:
                print(f"  ✗ ERRO: {error_msg[:100]}...")
        
        print()
    
    print("\n3. Diagnóstico do Grok 4:")
    print("=" * 50)
    
    # Teste específico para o Grok
    if api_keys.get("XAI"):
        print("Testando Grok 4 diretamente...")
        try:
            # Configura diretamente
            os.environ["XAI_API_KEY"] = os.getenv("XAI_API_KEY")
            
            # Tenta diferentes variações
            for model_variant in ["xai/grok-4", "grok-4", "xai/grok-beta"]:
                print(f"\nTentando: {model_variant}")
                try:
                    response = await litellm.acompletion(
                        model=model_variant,
                        messages=[{"role": "user", "content": "Olá, você é o Grok?"}],
                        max_tokens=50,
                        temperature=0
                    )
                    print(f"✓ SUCESSO com {model_variant}!")
                    print(f"  Resposta: {response.choices[0].message.content}")
                    print(f"  Modelo reportado: {response.model}")
                    break
                except Exception as e:
                    print(f"✗ Falhou: {str(e)[:100]}...")
        except Exception as e:
            print(f"✗ Erro geral ao testar Grok: {e}")
    else:
        print("✗ XAI_API_KEY não está configurada")
    
    print("\n4. Recomendações:")
    print("=" * 50)
    
    if not api_keys.get("XAI"):
        print("• Configure XAI_API_KEY no arquivo .env para usar o Grok 4")
    
    if api_keys.get("XAI") and api_keys.get("OPENROUTER"):
        print("• Grok 4 pode estar sendo redirecionado para OpenRouter")
        print("• Para usar diretamente a API do XAI, pode ser necessário ajustar a configuração")
    
    print("\n• Modelos funcionando corretamente devem aparecer na lista do chat")
    print("• Se um modelo não aparecer, verifique:")
    print("  - A chave de API está correta")
    print("  - O nome do modelo está correto")
    print("  - Não há limites de taxa ou créditos")

if __name__ == "__main__":
    # Configura o LiteLLM para mostrar mais detalhes
    # litellm.set_verbose = True
    
    asyncio.run(test_models())