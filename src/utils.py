import os
import ast
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class FunctionInfo:
    """Classe pour stocker les informations d'une fonction."""
    name: str
    description: str

@dataclass
class FileInfo:
    """Classe pour stocker les informations d'un fichier."""
    file_name: str
    file_path: str
    functions: List[Dict[str, str]]

class FunctionVisitor(ast.NodeVisitor):
    """Visiteur AST pour extraire les informations des fonctions."""
    
    def __init__(self):
        self.functions = []
        
    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visite chaque définition de fonction dans l'AST."""
        # Extraction de la docstring
        docstring = ast.get_docstring(node) or "Pas de description disponible"
        
        function_info = {
            "function_name": node.name,
            "function_description": docstring.strip()
        }
        
        self.functions.append(function_info)
        
        # Continue la visite pour les fonctions imbriquées
        self.generic_visit(node)

def analyze_python_file(file_path: str) -> List[Dict[str, str]]:
    """Analyse un fichier Python et retourne les informations sur ses fonctions."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Parse le contenu en AST
        tree = ast.parse(content)
        
        # Visite l'AST pour extraire les informations
        visitor = FunctionVisitor()
        visitor.visit(tree)
        
        return visitor.functions
        
    except Exception as e:
        print(f"Erreur lors de l'analyse de {file_path}: {str(e)}")
        return []

def analyze_codebase(directory_path: str) -> List[Dict[str, Any]]:
    """
    Analyse un dossier et retourne les informations sur toutes les fonctions Python.
    
    Args:
        directory_path (str): Chemin vers le dossier à analyser
        
    Returns:
        List[Dict]: Liste de dictionnaires contenant les informations sur les fichiers
                   et leurs fonctions selon la structure demandée
    """
    code_base = []
    
    # Parcours récursif du dossier
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            # Ne traite que les fichiers Python
            if not file_name.endswith('.py'):
                continue
                
            file_path = os.path.join(root, file_name)
            
            # Analyse le fichier
            functions = analyze_python_file(file_path)
            
            # Si des fonctions ont été trouvées, ajoute les informations du fichier
            if functions:
                file_info = {
                    "file_name": file_name,
                    "file_path": file_path,
                    "functions": functions
                }
                code_base.append(file_info)
    
    return code_base

"""results = analyze_codebase("./mon_dossier")
    
# Affichage des résultats
for file_info in results:
    print(f"\nFichier: {file_info['file_name']}")
    print(f"Chemin: {file_info['file_path']}")
    print("Fonctions:")
    for func in file_info['functions']:
        print(f"\t- {func['function_name']}")
        print(f"\t  Description: {func['function_description']}")"""

#tu peux aussi juste afficher results après l'avoir run 
