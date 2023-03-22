# wanki
Wanki (imagen en quechua) es una aplicación para explorar y transformar, de manera interactiva, datos provenientes de proyectos en Wildlife Insights.

## Instalación
Para instalar y utilizar Wanki, es necesario tener `conda`, un gestor de entornos virtuales y paquetes, instalado en su computador. Si no tiene instalado `conda`, puede instalarlo a través de la última versión de [Miniconda](https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links).

Una vez tenga `conda`, la instalación de Wanki se hace de la siguiente manera:

1. Descargar y descomprimir la última versión de Wanki.
```shell
git clone https://github.com/PEM-Humboldt/wanki
```
2. Navegar a la raíz del directorio donde está descomprimida la última instalación de Wanki. Por ejemplo:
```shell
cd wanki
```
3. Ejecutar los siguientes tres comandos:
```shell
conda env create -f environment.yml
conda activate wanki_env
pip install --upgrade https://github.com/PEM-Humboldt/wiutils/tarball/master

```

Una vez realizados estos pasos, se creará un entorno virtual con todas las dependencias necesarias para poder usar Wanki. Siga a la sección de ejecución para conocer cómo usar la aplicación.

## Ejecución
Cada vez que vaya a usar Wanki, debe seguir los siguientes pasos:

1. Abrir Anaconda Prompt.  Navegar a la raíz del directorio donde está descomprimida la última instalación de Wanki. Por ejemplo:
```shell
cd wanki
```
2. Activar el entorno virtual creado para la aplicación:
```shell
conda activate wanki_env
```
3. Abrir la aplicación
```shell
python run.py
```

Una vez realizados estos pasos, Wanki se abrirá en su navegador por defecto (e.g. Google Chrome o Mozilla Firefox).

## Cómo contribuir
1. Clone este repositorio en su máquina:
```shell
git clone https://github.com/PEM-Humboldt/wanki.git
```
2. Siga los pasos de instalación utilizando el repositorio recién clonado en vez de la descarga de la última versión de Wanki.
3. Agregue sus cambios en una nueva rama.
4. Abra un Pull Request para incorporar los cambios.

## Autores
* Angélica Diaz-Pulido - [AngelicaDiazPulido](https://github.com/marcelovilla)
* Marcelo Villa-Piñeros - [marcelovilla](https://github.com/marcelovilla)

## Licencia
Este paquete tiene una licencia MIT. [LICENSE.txt](LICENSE.txt) para más información.
