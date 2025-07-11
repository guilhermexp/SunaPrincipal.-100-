#!/usr/bin/env python3
"""
Script alternativo para ativar flags diretamente no Redis
Este script conecta diretamente ao Redis sem precisar do backend rodando
"""

import redis
import json
from datetime import datetime

def ativar_flags_direto():
    """Ativa as flags diretamente no Redis"""
    
    # Conecta ao Redis
    try:
        r = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True
        )
        r.ping()
        print("✅ Conectado ao Redis com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao conectar ao Redis: {e}")
        print("\nCertifique-se de que o Redis está rodando:")
        print("  brew services start redis")
        return
    
    # Lista de flags importantes
    flags = {
        'custom_agents': {
            'enabled': True,
            'description': 'Habilita agentes customizados (PRINCIPAL FLAG)',
            'updated_at': datetime.utcnow().isoformat()
        },
        'agentPlaygroundFlagFrontend': {
            'enabled': True,
            'description': 'Habilita o playground de agentes no frontend',
            'updated_at': datetime.utcnow().isoformat()
        },
        'marketplaceFlagFrontend': {
            'enabled': True,
            'description': 'Habilita o marketplace no frontend',
            'updated_at': datetime.utcnow().isoformat()
        },
        'agentPlaygroundEnabled': {
            'enabled': True,
            'description': 'Habilita funcionalidade do playground de agentes',
            'updated_at': datetime.utcnow().isoformat()
        },
        'marketplaceEnabled': {
            'enabled': True,
            'description': 'Habilita funcionalidade do marketplace',
            'updated_at': datetime.utcnow().isoformat()
        }
    }
    
    print("\n🚀 Ativando flags diretamente no Redis...")
    print("-" * 50)
    
    # Ativa cada flag
    for flag_name, flag_data in flags.items():
        try:
            # Salva no Redis com o prefixo correto
            key = f"feature_flag:{flag_name}"
            r.set(key, json.dumps(flag_data))
            print(f"✅ Flag '{flag_name}' ativada")
        except Exception as e:
            print(f"❌ Erro ao ativar '{flag_name}': {e}")
    
    print("-" * 50)
    
    # Verifica as flags
    print("\n📋 Verificando flags no Redis:")
    print("-" * 50)
    
    # Lista todas as flags
    for key in r.keys("feature_flag:*"):
        try:
            flag_name = key.replace("feature_flag:", "")
            flag_data = json.loads(r.get(key))
            status = "✅ Ativa" if flag_data.get("enabled") else "❌ Inativa"
            print(f"{status} - {flag_name}: {flag_data.get('description', 'Sem descrição')}")
        except Exception as e:
            print(f"❌ Erro ao ler flag {key}: {e}")
    
    print("\n✨ Processo concluído!")
    print("\n⚠️  IMPORTANTE:")
    print("   1. Reinicie o servidor backend se estiver rodando")
    print("   2. Faça refresh no navegador (Ctrl+F5 ou Cmd+Shift+R)")
    print("   3. Limpe o cache do navegador se necessário")

if __name__ == "__main__":
    ativar_flags_direto()