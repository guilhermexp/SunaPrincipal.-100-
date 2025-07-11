#!/usr/bin/env python3
"""
Script para ativar todas as feature flags do Suna
"""

import os
import sys
import redis
from datetime import datetime

# Adiciona o diretório backend ao path para importar os módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.flags.flags import FeatureFlagManager
from backend.utils.config import config

def activate_all_flags():
    """Ativa todas as feature flags conhecidas do sistema"""
    
    # Inicializa o gerenciador de flags
    flag_manager = FeatureFlagManager()
    
    # Lista de todas as flags conhecidas do sistema
    # Estas são as flags que encontramos no código frontend
    known_flags = [
        {
            "name": "custom_agents",
            "description": "Habilita agentes customizados (PRINCIPAL FLAG)"
        },
        {
            "name": "agentPlaygroundFlagFrontend",
            "description": "Habilita o playground de agentes no frontend"
        },
        {
            "name": "marketplaceFlagFrontend", 
            "description": "Habilita o marketplace no frontend"
        },
        {
            "name": "agentPlaygroundEnabled",
            "description": "Habilita funcionalidade do playground de agentes"
        },
        {
            "name": "marketplaceEnabled",
            "description": "Habilita funcionalidade do marketplace"
        },
        {
            "name": "maintenance-notice",
            "description": "Exibe aviso de manutenção"
        }
    ]
    
    print("🚀 Ativando todas as feature flags do Suna...")
    print("-" * 50)
    
    # Ativa cada flag
    for flag in known_flags:
        try:
            flag_manager.set_flag(
                flag_name=flag["name"],
                enabled=True,
                description=flag["description"]
            )
            print(f"✅ Flag '{flag['name']}' ativada com sucesso")
        except Exception as e:
            print(f"❌ Erro ao ativar flag '{flag['name']}': {str(e)}")
    
    print("-" * 50)
    
    # Lista todas as flags ativas
    print("\n📋 Flags atualmente ativas:")
    print("-" * 50)
    
    try:
        all_flags = flag_manager.list_flags()
        for flag_name, flag_data in all_flags.items():
            status = "✅ Ativa" if flag_data.get("enabled") else "❌ Inativa"
            print(f"{status} - {flag_name}: {flag_data.get('description', 'Sem descrição')}")
    except Exception as e:
        print(f"❌ Erro ao listar flags: {str(e)}")
    
    print("\n✨ Processo concluído!")

def check_redis_connection():
    """Verifica se o Redis está disponível"""
    try:
        r = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            decode_responses=True
        )
        r.ping()
        print("✅ Conexão com Redis estabelecida")
        return True
    except Exception as e:
        print(f"❌ Erro ao conectar com Redis: {str(e)}")
        print("\n⚠️  Certifique-se de que o Redis está rodando:")
        print("   - No macOS: brew services start redis")
        print("   - No Linux: sudo systemctl start redis")
        print("   - No Docker: docker run -d -p 6379:6379 redis")
        return False

def main():
    print("=" * 50)
    print("🎯 ATIVADOR DE FLAGS DO SUNA")
    print("=" * 50)
    
    # Verifica conexão com Redis
    if not check_redis_connection():
        print("\n❌ Não foi possível continuar sem conexão com o Redis")
        sys.exit(1)
    
    print()
    
    # Ativa todas as flags
    activate_all_flags()
    
    print("\n💡 Dicas:")
    print("   - As flags do frontend precisam de refresh da página para surtirem efeito")
    print("   - Certifique-se de que o backend está rodando para que as flags sejam lidas")
    print("   - Use o endpoint GET /feature-flags para verificar as flags via API")

if __name__ == "__main__":
    main()