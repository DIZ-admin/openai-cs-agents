"""
Dependency Security Scanner for ERNI Gruppe Building Agents.

This script scans Python and npm dependencies for known vulnerabilities.

Requirements:
    pip install pip-audit safety

Usage:
    python security_audit/dependency_scan.py
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


class DependencyScanner:
    """Scans dependencies for security vulnerabilities."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.python_backend = project_root / "python-backend"
        self.frontend = project_root / "ui"
        self.results = {
            "scan_date": datetime.now().isoformat(),
            "python_vulnerabilities": [],
            "npm_vulnerabilities": [],
            "summary": {}
        }
    
    def run_full_scan(self) -> Dict:
        """Run complete dependency security scan."""
        print("="*80)
        print("DEPENDENCY SECURITY SCAN")
        print("="*80)
        print(f"Project: ERNI Gruppe Building Agents")
        print(f"Scan Date: {self.results['scan_date']}")
        print("="*80 + "\n")
        
        # Scan Python dependencies
        print("📦 Scanning Python dependencies...")
        self.scan_python_dependencies()
        
        # Scan npm dependencies
        print("\n📦 Scanning npm dependencies...")
        self.scan_npm_dependencies()
        
        # Generate summary
        self.generate_summary()
        
        # Save results
        self.save_results()
        
        # Print summary
        self.print_summary()
        
        return self.results
    
    def scan_python_dependencies(self):
        """Scan Python dependencies using pip-audit."""
        try:
            # Run pip-audit
            result = subprocess.run(
                ["pip-audit", "--format=json", "-r", "requirements.txt"],
                cwd=self.python_backend,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                # No vulnerabilities found
                print("  ✅ No vulnerabilities found in Python dependencies")
                self.results["python_vulnerabilities"] = []
            else:
                # Parse vulnerabilities
                try:
                    vulnerabilities = json.loads(result.stdout)
                    self.results["python_vulnerabilities"] = vulnerabilities.get("dependencies", [])
                    
                    vuln_count = len(self.results["python_vulnerabilities"])
                    print(f"  ⚠️  Found {vuln_count} vulnerable Python packages")
                    
                    for vuln in self.results["python_vulnerabilities"]:
                        package = vuln.get("name", "unknown")
                        version = vuln.get("version", "unknown")
                        vulns = vuln.get("vulns", [])
                        
                        print(f"\n  Package: {package} ({version})")
                        for v in vulns:
                            vuln_id = v.get("id", "N/A")
                            description = v.get("description", "No description")
                            fix_versions = v.get("fix_versions", [])
                            
                            print(f"    - {vuln_id}: {description[:80]}...")
                            if fix_versions:
                                print(f"      Fix: Upgrade to {', '.join(fix_versions)}")
                
                except json.JSONDecodeError:
                    print(f"  ❌ Error parsing pip-audit output")
                    self.results["python_vulnerabilities"] = [
                        {"error": "Failed to parse pip-audit output", "raw": result.stdout}
                    ]
        
        except FileNotFoundError:
            print("  ⚠️  pip-audit not installed. Install with: pip install pip-audit")
            self.results["python_vulnerabilities"] = [
                {"error": "pip-audit not installed"}
            ]
        
        except subprocess.TimeoutExpired:
            print("  ❌ pip-audit scan timed out")
            self.results["python_vulnerabilities"] = [
                {"error": "Scan timed out"}
            ]
        
        except Exception as e:
            print(f"  ❌ Error scanning Python dependencies: {e}")
            self.results["python_vulnerabilities"] = [
                {"error": str(e)}
            ]
    
    def scan_npm_dependencies(self):
        """Scan npm dependencies using npm audit."""
        if not self.frontend.exists():
            print("  ⚠️  Frontend directory not found, skipping npm scan")
            return
        
        try:
            # Run npm audit
            result = subprocess.run(
                ["npm", "audit", "--json"],
                cwd=self.frontend,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            try:
                audit_data = json.loads(result.stdout)
                
                # Extract vulnerabilities
                vulnerabilities = audit_data.get("vulnerabilities", {})
                
                if not vulnerabilities:
                    print("  ✅ No vulnerabilities found in npm dependencies")
                    self.results["npm_vulnerabilities"] = []
                else:
                    # Parse vulnerabilities
                    vuln_list = []
                    
                    for package, vuln_data in vulnerabilities.items():
                        severity = vuln_data.get("severity", "unknown")
                        via = vuln_data.get("via", [])
                        
                        vuln_list.append({
                            "package": package,
                            "severity": severity,
                            "via": via
                        })
                    
                    self.results["npm_vulnerabilities"] = vuln_list
                    
                    # Count by severity
                    severity_counts = {}
                    for v in vuln_list:
                        sev = v["severity"]
                        severity_counts[sev] = severity_counts.get(sev, 0) + 1
                    
                    print(f"  ⚠️  Found {len(vuln_list)} vulnerable npm packages:")
                    for severity, count in severity_counts.items():
                        print(f"    - {severity.upper()}: {count}")
            
            except json.JSONDecodeError:
                print(f"  ❌ Error parsing npm audit output")
                self.results["npm_vulnerabilities"] = [
                    {"error": "Failed to parse npm audit output"}
                ]
        
        except FileNotFoundError:
            print("  ⚠️  npm not found. Make sure Node.js is installed")
            self.results["npm_vulnerabilities"] = [
                {"error": "npm not found"}
            ]
        
        except subprocess.TimeoutExpired:
            print("  ❌ npm audit timed out")
            self.results["npm_vulnerabilities"] = [
                {"error": "Scan timed out"}
            ]
        
        except Exception as e:
            print(f"  ❌ Error scanning npm dependencies: {e}")
            self.results["npm_vulnerabilities"] = [
                {"error": str(e)}
            ]
    
    def generate_summary(self):
        """Generate summary of scan results."""
        python_count = len([v for v in self.results["python_vulnerabilities"] if "error" not in v])
        npm_count = len([v for v in self.results["npm_vulnerabilities"] if "error" not in v])
        
        self.results["summary"] = {
            "total_vulnerabilities": python_count + npm_count,
            "python_vulnerabilities": python_count,
            "npm_vulnerabilities": npm_count,
            "scan_successful": True
        }
    
    def save_results(self):
        """Save scan results to JSON file."""
        output_dir = self.project_root / "python-backend" / "security_audit"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"dependency_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")
    
    def print_summary(self):
        """Print summary of scan results."""
        print("\n" + "="*80)
        print("SCAN SUMMARY")
        print("="*80)
        
        summary = self.results["summary"]
        
        print(f"Total Vulnerabilities: {summary['total_vulnerabilities']}")
        print(f"  - Python: {summary['python_vulnerabilities']}")
        print(f"  - npm: {summary['npm_vulnerabilities']}")
        
        if summary['total_vulnerabilities'] == 0:
            print("\n✅ No vulnerabilities found!")
        else:
            print(f"\n⚠️  {summary['total_vulnerabilities']} vulnerabilities require attention")
        
        print("="*80 + "\n")


def main():
    """Main entry point."""
    # Get project root (parent of python-backend)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    
    # Run scan
    scanner = DependencyScanner(project_root)
    results = scanner.run_full_scan()
    
    # Exit with error code if vulnerabilities found
    if results["summary"]["total_vulnerabilities"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

