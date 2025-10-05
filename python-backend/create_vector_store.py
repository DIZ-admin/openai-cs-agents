"""
Create a new OpenAI Vector Store and upload ERNI Gruppe knowledge base.

This script:
1. Creates a new Vector Store
2. Uploads erni_knowledge_base.json and erni_sitemap.json
3. Outputs the new Vector Store ID for .env configuration
"""

import os
import sys
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    """Create Vector Store and upload knowledge base."""

    print("=" * 80)
    print("ERNI Gruppe Vector Store Creation")
    print("=" * 80)
    print()

    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    print("✓ OpenAI client initialized")
    print()

    # Check if knowledge base files exist
    kb_file = Path(__file__).parent / "data" / "erni_knowledge_base.json"
    sitemap_file = Path(__file__).parent / "data" / "erni_sitemap.json"

    if not kb_file.exists():
        print(f"❌ Error: Knowledge base file not found: {kb_file}")
        sys.exit(1)

    if not sitemap_file.exists():
        print(f"❌ Error: Sitemap file not found: {sitemap_file}")
        sys.exit(1)

    print(f"✓ Knowledge base file found: {kb_file}")
    print(f"  File size: {kb_file.stat().st_size:,} bytes")
    print(f"✓ Sitemap file found: {sitemap_file}")
    print(f"  File size: {sitemap_file.stat().st_size:,} bytes")
    print()

    # Create new Vector Store
    print("🔨 Creating new Vector Store...")
    try:
        # Note: In OpenAI SDK 1.109.1, vector_stores is at client.vector_stores, not client.beta.vector_stores
        vector_store = client.vector_stores.create(
            name="ERNI Gruppe Knowledge Base"
        )
        print("✓ Vector Store created successfully")
        print(f"  Vector Store ID: {vector_store.id}")
        print(f"  Name: {vector_store.name}")
        print()
    except Exception as e:
        print(f"❌ Error creating vector store: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Upload knowledge base file
    print("📤 Uploading knowledge base file...")
    try:
        with open(kb_file, "rb") as f:
            kb_file_obj = client.files.create(file=f, purpose="assistants")
        print("✓ Knowledge base file uploaded")
        print(f"  File ID: {kb_file_obj.id}")
        print()
    except Exception as e:
        print(f"❌ Error uploading knowledge base: {e}")
        sys.exit(1)

    # Upload sitemap file
    print("📤 Uploading sitemap file...")
    try:
        with open(sitemap_file, "rb") as f:
            sitemap_file_obj = client.files.create(file=f, purpose="assistants")
        print("✓ Sitemap file uploaded")
        print(f"  File ID: {sitemap_file_obj.id}")
        print()
    except Exception as e:
        print(f"❌ Error uploading sitemap: {e}")
        sys.exit(1)

    # Add files to vector store
    print(f"📥 Adding files to Vector Store {vector_store.id}...")
    try:
        # Add knowledge base
        vs_file_kb = client.vector_stores.files.create(
            vector_store_id=vector_store.id, file_id=kb_file_obj.id
        )
        print(f"✓ Knowledge base added (status: {vs_file_kb.status})")

        # Add sitemap
        vs_file_sitemap = client.vector_stores.files.create(
            vector_store_id=vector_store.id, file_id=sitemap_file_obj.id
        )
        print(f"✓ Sitemap added (status: {vs_file_sitemap.status})")
        print()
    except Exception as e:
        print(f"❌ Error adding files to vector store: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Wait for processing
    print("⏳ Waiting for files to be processed...")
    import time

    max_wait = 60  # seconds
    elapsed = 0
    while elapsed < max_wait:
        try:
            vs = client.vector_stores.retrieve(vector_store.id)
            if vs.file_counts.completed == 2:
                print("✓ All files processed successfully")
                break
            elif vs.file_counts.failed > 0:
                print(f"⚠️  Warning: {vs.file_counts.failed} file(s) failed to process")
                break
            else:
                print(
                    f"  Processing... ({vs.file_counts.in_progress} in progress, {vs.file_counts.completed} completed)"
                )
                time.sleep(5)
                elapsed += 5
        except Exception as e:
            print(f"⚠️  Warning: Could not check status: {e}")
            break

    print()

    # Verify vector store
    print("🔍 Verifying vector store...")
    try:
        vs = client.beta.vector_stores.retrieve(vector_store.id)
        print("✓ Vector Store verified")
        print(f"  Name: {vs.name}")
        print(f"  File counts: {vs.file_counts}")
        print()
    except Exception as e:
        print(f"⚠️  Warning: Could not verify vector store: {e}")
        print()

    # Success message
    print("=" * 80)
    print("✅ Vector Store Creation Complete!")
    print("=" * 80)
    print()
    print("📝 Next steps:")
    print()
    print("1. Update your .env file with the new Vector Store ID:")
    print(f"   OPENAI_VECTOR_STORE_ID={vector_store.id}")
    print()
    print("2. Restart the backend server:")
    print("   cd python-backend")
    print("   source .venv/bin/activate")
    print("   uvicorn api:app --host 0.0.0.0 --port 8000 --env-file .env")
    print()
    print("3. Run tests to verify:")
    print("   python -m pytest tests/e2e/test_e2e_full_stack.py::TestFAQAgentVectorStore -v")
    print()
    print(f"🔑 Vector Store ID: {vector_store.id}")
    print()


if __name__ == "__main__":
    main()

