# infrastructure/open_csv.py
from core.result import Result

def open_csv_file(path: str, encoding: str = "utf-8") -> Result:
    """
    Abre un archivo CSV de forma segura.
    Devuelve Result.success(list_of_lines) o Result.failure(error_message).
    """
    try:
        with open(path, "r", encoding=encoding) as file:
            return Result.success(list(file.readlines()))
    except FileNotFoundError:
        return Result.failure(f"Archivo '{path}' no encontrado")
    except PermissionError:
        return Result.failure(f"Sin permisos para leer '{path}'")
    except UnicodeDecodeError:
        return Result.failure(f"Error de codificación en '{path}'")
    except Exception as e:
        return Result.failure(f"Error inesperado: {str(e)}")
