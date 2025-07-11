#!/usr/bin/env python3
"""
Script de inicialização automática de flags
Este script é executado ao iniciar o backend para garantir que as flags essenciais estejam ativas
"""

import asyncio
import json
import os
from datetime import datetime
import sys

# Adiciona o diretório backend ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flags.flags import set_flag, list_flags, get_flag_details
from services import redis

# Configuração de flags padrão
DEFAULT_FLAGS = {
    'custom_agents': {
        'enabled': True,
        'description': 'Habilita agentes customizados'
    },
    'agentPlaygroundFlagFrontend': {
        'enabled': True,
        'description': 'Habilita o playground de agentes no frontend'
    },
    'marketplaceFlagFrontend': {
        'enabled': True,
        'description': 'Habilita o marketplace no frontend'
    },
    'agentPlaygroundEnabled': {
        'enabled': True,
        'description': 'Habilita funcionalidade do playground de agentes'
    },
    'marketplaceEnabled': {
        'enabled': True,
        'description': 'Habilita funcionalidade do marketplace'
    }
}

# Arquivo de persistência local
PERSISTENCE_FILE = os.path.join(os.path.dirname(__file__), 'data', 'feature_flags.json')

def ensure_data_directory():
    """Garante que o diretório de dados existe"""
    data_dir = os.path.dirname(PERSISTENCE_FILE)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

def save_flags_to_file(flags):
    """Salva as flags em um arquivo JSON para persistência"""
    ensure_data_directory()
    try:
        with open(PERSISTENCE_FILE, 'w') as f:
            json.dump(flags, f, indent=2)
        print(f"✅ Flags salvas em {PERSISTENCE_FILE}")
    except Exception as e:
        print(f"❌ Erro ao salvar flags: {e}")

def load_flags_from_file():
    """Carrega flags do arquivo de persistência"""
    if os.path.exists(PERSISTENCE_FILE):
        try:
            with open(PERSISTENCE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Erro ao carregar flags do arquivo: {e}")
    return None

async def initialize_flags():
    """Inicializa as flags no Redis com valores persistidos ou padrão"""
    print("🚀 Inicializando feature flags...")
    
    # Tenta carregar flags persistidas
    persisted_flags = load_flags_from_file()
    
    if persisted_flags:
        print("📂 Carregando flags do arquivo de persistência...")
        flags_to_set = persisted_flags
    else:
        print("🆕 Usando configuração padrão de flags...")
        flags_to_set = DEFAULT_FLAGS
    
    # Define cada flag no Redis
    for flag_name, flag_config in flags_to_set.items():
        try:
            await set_flag(
                flag_name,
                flag_config['enabled'],
                flag_config.get('description', '')
            )
            print(f"✅ Flag '{flag_name}' configurada: {flag_config['enabled']}")
        except Exception as e:
            print(f"❌ Erro ao configurar flag '{flag_name}': {e}")
    
    # Salva estado atual para persistência
    current_flags = {}
    all_flags = await list_flags()
    
    for flag_name, enabled in all_flags.items():
        details = await get_flag_details(flag_name)
        if details:
            current_flags[flag_name] = {
                'enabled': enabled,
                'description': details.get('description', ''),
                'updated_at': details.get('updated_at', datetime.utcnow().isoformat())
            }
    
    save_flags_to_file(current_flags)
    
    print("\n📋 Status final das flags:")
    for flag_name, enabled in all_flags.items():
        status = "✅ Ativa" if enabled else "❌ Inativa"
        print(f"   {status} - {flag_name}")

async def main():
    """Função principal"""
    print("=" * 50)
    print("🎯 INICIALIZADOR DE FLAGS DO SUNA")
    print("=" * 50)
    
    # Aguarda um pouco para garantir que o Redis está pronto
    print("\n⏳ Aguardando Redis inicializar...")
    await asyncio.sleep(2)
    
    try:
        # Testa conexão com Redis
        redis_client = await redis.get_client()
        await redis_client.ping()
        print("✅ Redis conectado!")
        
        # Inicializa as flags
        await initialize_flags()
        
        print("\n✨ Inicialização concluída!")
        
    except Exception as e:
        print(f"\n❌ Erro durante inicialização: {e}")
        print("⚠️  As flags serão inicializadas quando o Redis estiver disponível")
        
    finally:
        # Fecha conexão Redis
        redis_client = await redis.get_client()
        await redis_client.close()

if __name__ == "__main__":
    asyncio.run(main())