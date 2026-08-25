from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

ALL_DIRECTORIES = [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR]


def init_directories() -> list[Path]:
    list_dir = []
    for directory in ALL_DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)
        list_dir.append(directory)
    return list_dir


if __name__ == "__main__":
    dirs = init_directories()
    print("Diretórios verificados e criados com sucesso.")
    for d in dirs:
        print(f" Diretório: {d}")
