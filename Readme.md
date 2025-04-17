# Document reader

> [!INFO]
> Requisitos para correr este programa:
> - python
> - docker/postgres (con la extension de pgvector)

Este es un pequeño programa hecho con el proposito de demostrar las capacidades
de langchain, un framework de python pensado para trabajar con _language models_.
Para que esta app funcione se necesitan agregar algunas librerias primero:

```bash
pip install langchain langchain_openai langchain_ollama pypdf psycopg2 langchain-text-splitters sentence_transformers
```

> [!NOTE]
> La libreria de sentence-transformers puede llegar a tirar algun error relacionado al
> espacio, de ser el caso, simplemente googlee.

Una vez contemos con todas las librerias necesarias tendremos que conseguir la extension
para convertir Postgres en una base de datos vectorial, [pgvector](https://github.com/pgvector/pgvector). En el caso de tener
docker, podemos usar el compose de este mismo repo simplemente usando el siguiente 
comando en nuestra terminal:
```bash
docker compose -f docker-compose.yml up -d
```

> [!IMPORTANT]
> En caso de no tener docker instalado, visite la [get docker page](https://docs.docker.com/get-started/get-docker/) y descargue la version 
> para su sistema operativo.

Una vez con todo instalado, simplemente use el siguiente comando:
```bash
python docReaderChat.py
```

## Add custom files

Como tal, este projecto esta pensado para ayudarme a buscar en la documentacion de Zig,
pero, si ud desea darle mas documentos puede simplemente cambiar las variables de:
- path
- docName
al inicio de la aplicacion, ponga la direccion del documento que desea vectorizar
y el nombre con el que lo desea guardar en postgres respectivamente.

Por defecto el agente siempre buscara en la base de datos vectorial si el prompt
esta relacionado con Zig, pero es tan facil como decirle al agente algo como:
`With use of the vector database, ...` y este usara la herramienta de busqueda.

