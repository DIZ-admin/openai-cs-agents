#!/usr/bin/env python3
"""
Analyze duplicate files with ' 2' suffix in the repository.
Compare original files with their ' 2' versions and determine the best action.
"""

import os
import subprocess
import hashlib
from pathlib import Path
from typing import List, Tuple, Dict

def get_git_tracked_duplicates() -> List[str]:
    """Get list of all ' 2' files tracked by Git."""
    result = subprocess.run(
        ['git', 'ls-files'],
        capture_output=True,
        text=True,
        check=True
    )
    files = result.stdout.strip().split('\n')
    return [f for f in files if ' 2.' in f or f.endswith(' 2')]

def get_original_path(duplicate_path: str) -> str:
    """Get the original file path from a duplicate path."""
    # Remove ' 2' before the extension
    if ' 2.' in duplicate_path:
        return duplicate_path.replace(' 2.', '.')
    elif duplicate_path.endswith(' 2'):
        return duplicate_path[:-2]
    return duplicate_path

def file_hash(filepath: str) -> str:
    """Calculate MD5 hash of a file."""
    if not os.path.exists(filepath):
        return None
    
    md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            md5.update(chunk)
    return md5.hexdigest()

def get_file_info(filepath: str) -> Dict:
    """Get file information (size, mtime, hash)."""
    if not os.path.exists(filepath):
        return None
    
    stat = os.stat(filepath)
    return {
        'path': filepath,
        'size': stat.st_size,
        'mtime': stat.st_mtime,
        'hash': file_hash(filepath),
        'exists': True
    }

def compare_files(original: str, duplicate: str) -> Dict:
    """Compare original and duplicate files."""
    orig_info = get_file_info(original)
    dup_info = get_file_info(duplicate)
    
    result = {
        'original': original,
        'duplicate': duplicate,
        'original_info': orig_info,
        'duplicate_info': dup_info,
        'action': None,
        'reason': None
    }
    
    # Case 1: Original doesn't exist
    if orig_info is None:
        result['action'] = 'RENAME'
        result['reason'] = 'Original file does not exist, rename duplicate to original'
        return result
    
    # Case 2: Duplicate doesn't exist (shouldn't happen with git ls-files)
    if dup_info is None:
        result['action'] = 'SKIP'
        result['reason'] = 'Duplicate file does not exist'
        return result
    
    # Case 3: Files are identical (same hash)
    if orig_info['hash'] == dup_info['hash']:
        result['action'] = 'DELETE'
        result['reason'] = 'Files are identical (same hash)'
        return result
    
    # Case 4: Files are different
    # Check which is newer
    if dup_info['mtime'] > orig_info['mtime']:
        result['action'] = 'REPLACE'
        result['reason'] = f'Duplicate is newer ({dup_info["mtime"]} > {orig_info["mtime"]})'
    else:
        result['action'] = 'DELETE'
        result['reason'] = f'Original is newer or same age ({orig_info["mtime"]} >= {dup_info["mtime"]})'
    
    # Add size difference info
    size_diff = dup_info['size'] - orig_info['size']
    result['size_diff'] = size_diff
    
    return result

def main():
    """Main function to analyze all duplicates."""
    print("🔍 Analyzing duplicate files with ' 2' suffix...\n")
    
    duplicates = get_git_tracked_duplicates()
    print(f"Found {len(duplicates)} duplicate files tracked by Git\n")
    
    results = []
    
    for dup_path in duplicates:
        orig_path = get_original_path(dup_path)
        comparison = compare_files(orig_path, dup_path)
        results.append(comparison)
    
    # Group by action
    actions = {}
    for result in results:
        action = result['action']
        if action not in actions:
            actions[action] = []
        actions[action].append(result)
    
    # Print summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    for action, items in sorted(actions.items()):
        print(f"\n{action}: {len(items)} files")
        for item in items[:5]:  # Show first 5 examples
            print(f"  - {item['duplicate']}")
            print(f"    → {item['reason']}")
        if len(items) > 5:
            print(f"  ... and {len(items) - 5} more")
    
    print("\n" + "=" * 80)
    print(f"TOTAL: {len(results)} duplicate files")
    print("=" * 80)
    
    # Save detailed report
    with open('DUPLICATE_FILES_ANALYSIS.txt', 'w') as f:
        f.write("DUPLICATE FILES ANALYSIS REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        for action in sorted(actions.keys()):
            f.write(f"\n{action} ({len(actions[action])} files)\n")
            f.write("-" * 80 + "\n")
            
            for item in actions[action]:
                f.write(f"\nDuplicate: {item['duplicate']}\n")
                f.write(f"Original:  {item['original']}\n")
                f.write(f"Action:    {item['action']}\n")
                f.write(f"Reason:    {item['reason']}\n")
                
                if item['original_info']:
                    f.write(f"Original:  {item['original_info']['size']} bytes, "
                           f"hash={item['original_info']['hash'][:8]}...\n")
                else:
                    f.write(f"Original:  DOES NOT EXIST\n")
                
                if item['duplicate_info']:
                    f.write(f"Duplicate: {item['duplicate_info']['size']} bytes, "
                           f"hash={item['duplicate_info']['hash'][:8]}...\n")
                else:
                    f.write(f"Duplicate: DOES NOT EXIST\n")
                
                if 'size_diff' in item:
                    f.write(f"Size diff: {item['size_diff']:+d} bytes\n")
                
                f.write("\n")
    
    print("\n✅ Detailed report saved to: DUPLICATE_FILES_ANALYSIS.txt")
    
    return results, actions

if __name__ == '__main__':
    results, actions = main()

