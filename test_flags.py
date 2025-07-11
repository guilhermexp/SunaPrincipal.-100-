#!/usr/bin/env python3
"""
Script para testar se as feature flags estão funcionando corretamente
"""
import asyncio
import sys
import os

# Adiciona o diretório backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_flags():
    try:
        from flags import is_enabled
        
        print("=== TESTE DE FEATURE FLAGS ===")
        
        # Testa a flag custom_agents
        custom_agents_enabled = await is_enabled('custom_agents')
        print(f"custom_agents: {custom_agents_enabled}")
        
        # Testa outras flags importantes
        flags_to_test = [
            'agentPlaygroundEnabled',
            'marketplaceEnabled', 
            'agent_marketplace',
            'knowledge_base'
        ]
        
        for flag in flags_to_test:
            enabled = await is_enabled(flag)
            print(f"{flag}: {enabled}")
            
        print("\n=== RESULTADO ===")
        if custom_agents_enabled:
            print("✅ Custom Agents está HABILITADO")
        else:
            print("❌ Custom Agents está DESABILITADO")
            
        print("=== FIM DO TESTE ===")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_flags()) 