"""
OPTIPICK - Script de vérification de l'environnement
═══════════════════════════════════════════════════════════════════════════════

Vérifie que tous les composants sont correctement installés et configurés.

Usage :
    python verify_environment.py
"""

import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Affiche un en-tête formaté."""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80)


def check_python_version():
    """Vérifie la version Python."""
    print_header("✓ VÉRIFICATION PYTHON")
    
    version = sys.version_info
    print(f"  Python version : {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("  Status : ✅ OK (3.8 ou supérieur)")
        return True
    else:
        print("  Status : ❌ ERREUR (Python 3.8+ requis)")
        return False


def check_package(package_name, import_name=None):
    """Vérifie si un package est installé."""
    if import_name is None:
        import_name = package_name
    
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'N/A')
        print(f"  ✅ {package_name:20} → {version}")
        return True
    except ImportError:
        print(f"  ❌ {package_name:20} → NOT INSTALLED")
        return False


def check_required_packages():
    """Vérifie les packages Python requis."""
    print_header("✓ VÉRIFICATION PACKAGES PYTHON")
    
    packages = [
        ('streamlit', 'streamlit'),
        ('matplotlib', 'matplotlib'),
        ('numpy', 'numpy'),
        ('pandas', 'pandas'),
    ]
    
    all_ok = True
    for package, import_name in packages:
        if not check_package(package, import_name):
            all_ok = False
    
    return all_ok


def check_data_files():
    """Vérifie que les fichiers JSON sont présents."""
    print_header("✓ VÉRIFICATION FICHIERS DE DONNÉES")
    
    data_files = [
        'data/warehouse.json',
        'data/products.json',
        'data/agents.json',
        'data/orders.json'
    ]
    
    all_ok = True
    for file in data_files:
        path = Path(file)
        if path.exists():
            size = path.stat().st_size
            print(f"  ✅ {file:30} ({size:,} bytes)")
        else:
            print(f"  ❌ {file:30} (NOT FOUND)")
            all_ok = False
    
    return all_ok


def check_source_files():
    """Vérifie que les fichiers source sont présents."""
    print_header("✓ VÉRIFICATION FICHIERS SOURCE")
    
    source_files = [
        'src/models.py',
        'src/allocation.py',
        'src/suite.py',
        'src/constraints.py',
        'src/utils.py',
        'app_streamlit.py'
    ]
    
    all_ok = True
    for file in source_files:
        path = Path(file)
        if path.exists():
            try:
                lines = len(path.read_text(encoding='utf-8').split('\n'))
            except UnicodeDecodeError:
                lines = len(path.read_text(encoding='latin-1').split('\n'))
            print(f"  ✅ {file:30} ({lines:,} lines)")
        else:
            print(f"  ❌ {file:30} (NOT FOUND)")
            all_ok = False
    
    return all_ok


def check_streamlit_installation():
    """Vérifie que Streamlit peut être lancé."""
    print_header("✓ VÉRIFICATION STREAMLIT")
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'streamlit', '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            version_info = result.stdout.strip()
            print(f"  ✅ Streamlit executable")
            print(f"     {version_info}")
            return True
        else:
            print(f"  ❌ Erreur Streamlit : {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ Erreur lors du test : {e}")
        return False


def main():
    """Lance tous les tests de vérification."""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  OPTIPICK - Vérification d'environnement".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    results = {
        'Python': check_python_version(),
        'Packages': check_required_packages(),
        'Data files': check_data_files(),
        'Source files': check_source_files(),
        'Streamlit': check_streamlit_installation(),
    }
    
    # Résumé
    print_header("📊 RÉSUMÉ")
    
    for check_name, result in results.items():
        status = "✅ OK" if result else "❌ ERREUR"
        print(f"  {check_name:20} : {status}")
    
    all_ok = all(results.values())
    
    print_header("🎯 CONCLUSION")
    
    if all_ok:
        print("\n  ✅ TOUS LES TESTS RÉUSSIS !")
        print("\n  Vous pouvez lancer l'application :")
        print("  > streamlit run app_streamlit.py")
        print("  ou double-cliquez sur launch_app.bat\n")
        return 0
    else:
        print("\n  ❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("\n  Actions recommandées :")
        print("  1. Installez les dépendances manquantes :")
        print("     > pip install -r requirements_streamlit.txt")
        print("  2. Vérifiez les fichiers JSON dans data/")
        print("  3. Vérifiez les fichiers source dans src/\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
