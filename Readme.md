# Document reader

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

La idea de este projecto es usar un LM para ayudarme a buscar en la documentacion de Zig,
de esa forma, si necesito hacer una busqueda rapida puedo preguntarle, si ud desea
agregar documentacion especifica o puede cambiar los datos en la **linea 76**, donde 
llamamos la funcion `vectorize`, el primer campo es el path de nuestro documento
y el segundo es el nombre con el que queremos guardar el documento, de ahi. Una vez
vectorizado el documento, simplemente digale al LM que debe apoyarse de la base de 
datos vectorial para su respuesta para que use la herramienta de busqueda.

