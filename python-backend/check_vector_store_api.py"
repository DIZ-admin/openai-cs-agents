#!/usr/bin/env python3
"""
Script to check Vector Store API availability in OpenAI SDK.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from openai import OpenAI
import openai

def main():
    """Check Vector Store API availability."""
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        sys.exit(1)
    
    client = OpenAI(api_key=api_key)
    
    print("=" * 80)
    print("OPENAI SDK VECTOR STORE API CHECK")
    print("=" * 80)
    
    print(f"\n📦 OpenAI SDK версия: {openai.__version__}")
    
    print("\n=== Доступные атрибуты в client.beta ===")
    beta_attrs = [attr for attr in dir(client.beta) if not attr.startswith('_')]
    for attr in beta_attrs:
        print(f"  - {attr}")
    
    # Проверяем, есть ли vector_stores
    print("\n=== Проверка Vector Stores API ===")
    if hasattr(client.beta, 'vector_stores'):
        print("✓ client.beta.vector_stores существует!")
        print("\nМетоды vector_stores:")
        vs_methods = [m for m in dir(client.beta.vector_stores) if not m.startswith('_')]
        for method in vs_methods:
            print(f"  - {method}")
        
        # Попробуем создать тестовый Vector Store
        print("\n=== Попытка создать тестовый Vector Store ===")
        try:
            vs = client.beta.vector_stores.create(
                name="ERNI Test Vector Store"
            )
            print(f"✅ Vector Store создан успешно!")
            print(f"   ID: {vs.id}")
            print(f"   Name: {vs.name}")
            print(f"   Status: {vs.status if hasattr(vs, 'status') else 'N/A'}")
            
            # Удаляем тестовый Vector Store
            print("\n=== Удаление тестового Vector Store ===")
            try:
                client.beta.vector_stores.delete(vs.id)
                print("✅ Тестовый Vector Store удален")
            except Exception as e:
                print(f"⚠️  Не удалось удалить: {e}")
                
        except Exception as e:
            print(f"❌ Ошибка создания Vector Store: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("✗ client.beta.vector_stores НЕ существует")
    
    # Проверяем альтернативные пути
    print("\n=== Проверка альтернативных путей ===")
    if hasattr(client, 'vector_stores'):
        print("✓ client.vector_stores существует!")
    else:
        print("✗ client.vector_stores НЕ существует")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()

