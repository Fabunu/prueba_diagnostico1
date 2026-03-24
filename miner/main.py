import socket
import re
import ast
import javalang
import requests
import time
from pydriller import Repository

# el miner emite datos a un socket
host = "0.0.0.0"
port = 5000 # puerto del streaming

def get_top_repositorios(language, limit=5):
    url = f"https://api.github.com/search/repositories?q=language:{language}&sort=stars&order=desc&per_page={limit}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return [item["clone_url"] for item in response.json().get("items", [])]
    except:
        return []
    return []

def tokenize_name(name):
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\b)', name)
    return [w.lower() for w in words if len(w) > 1]

def extract_methods(file):
    names = []
    try:
        if file.filename.endswith(".py"):
            tree = ast.parse(file.source_code)
            names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        elif file.filename.endswith(".java"):
            tree = javalang.parse.parse(file.source_code)
            for _, node in tree.filter(javalang.tree.MethodDeclaration):
                names.append(node.name)
    except:
        pass
    return names

def start_mining():
    # crea el socket para enviar los datos al visualizador
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"esperando conexion del visualizer en el puerto {port}...")

        conn, addr = s.accept()
        with conn:
            print(f"vidualizer conectado desde {addr}")

            languages = ["python", "java"]
            for lang in languages:
                repos = get_top_repositorios(lang, limit=5)
                for url in repos:
                    print(f"procesando repositorio: {url}")
                    for commit in Repository(url, order="reverse").traverse_commits():
                        for m_file in commit.modified_files:
                            try:
                                if m_file.source_code:
                                    for name in extract_methods(m_file):
                                        for token in tokenize_name(name):
                                            #envia la palabra seguido de un salto de linea
                                            conn.sendall(f"{token}\n".encode("utf-8"))
                            except ValueError:
                                #si no resuelve el sha lo ignora
                                pass
                            except Exception as e:
                                #cualquie otro error raro dl pydriller
                                pass
                        print(f"commit {commit.hash[:7]} procesado")

if __name__ == "__main__":
    start_mining()
