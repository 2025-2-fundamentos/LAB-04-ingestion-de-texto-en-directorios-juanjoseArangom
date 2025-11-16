"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

import zipfile
import pandas as pd
from pathlib import Path


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:

    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```

    """

    zip_file_path = Path('files/input.zip')
    extract_path = Path('.')
    input_dir = Path('files/input')
    output_dir = Path('files/output')

    if zip_file_path.exists():
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    else:
        print(f"Error: No se encontró el archivo {zip_file_path}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    for data_type in ['train', 'test']:
        data = []
        source_dir = input_dir / data_type

        try:
            for txt_file in source_dir.glob('**/*.txt'):
                sentiment = txt_file.parent.name
                try:
                    phrase = txt_file.read_text(encoding='utf-8').strip()
                    if phrase:
                        data.append({
                            'phrase': phrase,
                            'target': sentiment
                        })
                except Exception as e:
                    print(f"Error leyendo el archivo {txt_file}: {e}")

        except FileNotFoundError:
            print(f"Error: Directorio no encontrado {source_dir}. "
                  "¿Se descomprimió correctamente el .zip?")
            continue

        if data:
            df = pd.DataFrame(data)
            output_file_path = output_dir / f"{data_type}_dataset.csv"
            df.to_csv(output_file_path, index=False)


if __name__ == "__main__":
    if not Path('files/input.zip').exists():
        Path('files').mkdir(exist_ok=True)
        (Path('input') / 'train' / 'positive').mkdir(parents=True, exist_ok=True)
        (Path('input') / 'train' / 'negative').mkdir(parents=True, exist_ok=True)
        (Path('input') / 'test' / 'neutral').mkdir(parents=True, exist_ok=True)

        (Path('input') / 'train' / 'positive' / '0000.txt').write_text('This is great!', encoding='utf-8')
        (Path('input') / 'train' / 'negative' / '0000.txt').write_text('This is bad.', encoding='utf-8')
        (Path('input') / 'test' / 'neutral' / '0000.txt').write_text('This is a file.', encoding='utf-8')

        with zipfile.ZipFile('files/input.zip', 'w') as zf:
            for f in Path('input').glob('**/*.*'):
                zf.write(f, f.relative_to(Path('.')))

pregunta_01()



