"""
Upload ERNI Gruppe knowledge base to OpenAI Vector Store.

This script uploads the erni_knowledge_base.json file to the specified
OpenAI Vector Store for use with the FAQ Agent.
"""

import os
import sys
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
VECTOR_STORE_ID = "vs_68e14a087e3c8191b4b7483ba3cb8d2a"
KNOWLEDGE_BASE_FILE = "data/erni_knowledge_base.json"

def main():
    """Upload knowledge base to OpenAI Vector Store."""
    
    print("="*80)
    print("ERNI Gruppe Knowledge Base Upload")
    print("="*80)
    print()
    
    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        sys.exit(1)
    
    client = OpenAI(api_key=api_key)
    print(f"✓ OpenAI client initialized")
    
    # Check if knowledge base file exists
    kb_path = Path(__file__).parent / KNOWLEDGE_BASE_FILE
    if not kb_path.exists():
        print(f"❌ Error: Knowledge base file not found: {kb_path}")
        sys.exit(1)
    
    print(f"✓ Knowledge base file found: {kb_path}")
    print(f"  File size: {kb_path.stat().st_size:,} bytes")
    print()
    
    # Upload file to OpenAI
    print("📤 Uploading file to OpenAI...")
    try:
        with open(kb_path, "rb") as f:
            file = client.files.create(
                file=f,
                purpose="assistants"
            )
        print(f"✓ File uploaded successfully")
        print(f"  File ID: {file.id}")
        print(f"  Filename: {file.filename}")
        print(f"  Status: {file.status}")
        print()
    except Exception as e:
        print(f"❌ Error uploading file: {e}")
        sys.exit(1)
    
    # Add file to vector store
    print(f"📥 Adding file to Vector Store {VECTOR_STORE_ID}...")
    try:
        vector_store_file = client.beta.vector_stores.files.create(
            vector_store_id=VECTOR_STORE_ID,
            file_id=file.id
        )
        print(f"✓ File added to vector store successfully")
        print(f"  Vector Store File ID: {vector_store_file.id}")
        print(f"  Status: {vector_store_file.status}")
        print()
    except Exception as e:
        print(f"❌ Error adding file to vector store: {e}")
        sys.exit(1)
    
    # Verify vector store contents
    print("🔍 Verifying vector store contents...")
    try:
        vector_store = client.beta.vector_stores.retrieve(VECTOR_STORE_ID)
        print(f"✓ Vector Store verified")
        print(f"  Name: {vector_store.name if hasattr(vector_store, 'name') else 'N/A'}")
        print(f"  File counts: {vector_store.file_counts}")
        print()
    except Exception as e:
        print(f"⚠️  Warning: Could not verify vector store: {e}")
        print()
    
    # List all files in vector store
    print("📋 Files in vector store:")
    try:
        files = client.beta.vector_stores.files.list(
            vector_store_id=VECTOR_STORE_ID
        )
        for idx, vs_file in enumerate(files.data, 1):
            print(f"  {idx}. File ID: {vs_file.id}")
            print(f"     Status: {vs_file.status}")
            if hasattr(vs_file, 'created_at'):
                from datetime import datetime
                created = datetime.fromtimestamp(vs_file.created_at)
                print(f"     Created: {created.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    except Exception as e:
        print(f"⚠️  Warning: Could not list files: {e}")
        print()
    
    print("="*80)
    print("✅ Knowledge Base Upload Complete!")
    print("="*80)
    print()
    print("Next steps:")
    print("1. Update FAQ Agent in main.py to use vector store")
    print("2. Test FAQ Agent with real queries")
    print("3. Run E2E tests to verify integration")
    print()
    print(f"Vector Store ID: {VECTOR_STORE_ID}")
    print(f"File ID: {file.id}")
    print()

if __name__ == "__main__":
    main()

