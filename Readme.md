# Document reader

Requisitos para correr este programa:
- Python  
- Docker/Postgres (con la extensión de pgvector)

Este es un pequeño programa hecho con el propósito de demostrar las capacidades  
de LangChain, un framework de Python pensado para trabajar con *language models*.  
Para que esta app funcione, se necesitan agregar algunas librerías primero:

```bash
pip install langchain langchain_openai langchain_ollama pypdf psycopg2 langchain-text-splitters sentence_transformers
```

> [!NOTE]
> La librería de `sentence-transformers` puede llegar a tirar algún error relacionado al  
> espacio. De ser el caso, simplemente googlee.

Una vez contemos con todas las librerías necesarias, tendremos que conseguir la extensión  
para convertir Postgres en una base de datos vectorial: [pgvector](https://github.com/pgvector/pgvector). En el caso de tener  
Docker, podemos usar el *compose* de este mismo repo simplemente usando el siguiente  
comando en nuestra terminal:
```bash
docker compose -f docker-compose.yml up -d
```

> [!IMPORTANT]
> En caso de no tener Docker instalado, visite la [get docker page](https://docs.docker.com/get-started/get-docker/) y descargue la versión  
> para su sistema operativo.

Una vez con todo instalado, simplemente use el siguiente comando:
```bash
python docReaderChat.py
```

## Agregar más archivos

Como tal, este proyecto está pensado para ayudarme a buscar en la documentación de Zig,  
pero, si usted desea darle más documentos, puede simplemente cambiar las variables de:  
- `path`  
- `docName`  
al inicio de la aplicación. Ponga la dirección del documento que desea vectorizar  
y el nombre con el que lo desea guardar en Postgres, respectivamente.

Por defecto, el agente siempre buscará en la base de datos vectorial si el prompt  
está relacionado con Zig, pero es tan fácil como decirle al agente algo como:  
`With use of the vector database, ...` y este usará la herramienta de búsqueda.

