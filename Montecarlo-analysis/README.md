# **Descripción**
Este modelo utiliza una metolodogía de simulación inversa y analisis de Montecarlo para estimar los flujos de emisión de fuentes contaminantes a través de un software que resuelve la ecuación de difusión-convección mediante técnicas numéricas de elementos finitos. En esta versión la ecuación se ha simplificado de forma que no tiene variabiliad temporal ni un campo de vectores **v** que favorezca el desplazamiento de los contaminantes, es decir solamente tiene en cuenta el término asociado a la difusión del material. 
La arquitectura creada permite estimar los flujos de emisión a través de datos de sensores de calidad del aire y sus respectivas ubicaciones.

# **Requisitos**
- Python3
- Numpy
- Pandas
- Scipy
- Meshio

# **Instalación**

Para el correcto funcionamiento del modelo es necesario instalar la librería de _SfePy_ ejecutando `pip install sfepy` en la terminal. La documentación con todas las funcionalidades se encuentra en la [página oficial](https://sfepy.org/).

Clonamos el repositorio de git en el directorio que queramos `git clone https://gitlab.hopu.eu/data-science/ai-services/montecarlo.git`. EL repositorio viene con un
ejemplo del modelo donde se estima el flujo de emisión de 5 fuentes contaminantes.

# **Datos de entrada:**

El modelo tiene 3 tipos diferentes de datos de entrada

- **Fichero .mesh**

    El fichero .mesh contiene el mallado del dominio y los puntos donde se calcula la solución del problema. Para crearlo se necesita un programa como gmsh (se puede instalar con $`pip install gmsh` y abrirlo desde la terminal con el comando $`gmsh`) donde a través de un fichero
    de configuración se crea el mallado, para ello se puede tomar como ejemplo el dominio cuadrado que se encuentra en geo-files/2d, abrirlo en gmsh y modificar este fichero de configuración con los límites del dominio que interesen. La resolución del mallado y por tanto del modelo de dispersión corresponde con el parámetro `lc` que se encuentra al principio del fichero de configuración .geo anteriormente mencionado. La resolución dependerá del tamaño del dominio. Una vez creado el mallado en gmsh se exporta como extensión .mesh y se debe guardar en el directorio meshes/2D con el nombre 'grid.mesh'.

- **Coordenadas de los puntos de emisión.**

    Las coordenadas de las fuentes de emisión deben incluirse en el fichero sources_coordinates.json que se encuentra en outputs/test donde deben añadirse tanto las coordenadas x como y de cada uno 
    de los puntos siguiendo el formato que tiene el diccionario.

- **Coordenadas de los puntos de observación.**

    Igual que los puntos de emisión, las coordenadas de los sensores o puntos de observación van en el fichero sensor_coordinates.json en el directorio outputs/test siguiendo el mismo formato
    que en el anterior.

- **Datos de sensores de calidad del aire.**

    En esta versión, el modelo estima los flujos de emisión mediante un escenario de contaminación creado a través del propio modelo de dispersión _SfePy_, lo que quiere decir que se ejecuta una simulación
    con los flujos de emisión que se pretenden estimar y sobre este resultado se extraen lo que serían los datos de observación, que en un caso real vendrían dados por sensores. Estos datos se miden y se le
    pasan al modelo en el archivo sensor_data.csv como una fila con cada uno de los valores observados correspondientes a cada fuente de emisión. Para medir estos valores de concentración sobre una simulación
    de _SfePy_ es necesario seguir los siguientes pasos.

    **1.** Cambiar los flujos de emisión en el fichero de configuración main.py. En el apartado materials debemos poner como flujos de emisión  en source_{nº de fuente}: val: {valor que se quiere estimar}, es decir
    el valor que quiere estimarse para ese punto de emisión, y así con los diferentes puntos.

    **2.** Una vez tenemos los flujos de emisión que se quieren estimar es necesario hacer una simulación y medir los resultados. Para ello guardamos los cambios, nos movemos al directorio /montecarlo/ y ejecutamos 
    el comando sfepy-run problem-descriptions/main.py. Ahora que el modelo se ha ejecutado mediremos los datos en los puntos de interés, para ello abrimos el archivo outputs/test/xy_values.py y añadimos las 
    coordenadas de los puntos de los sensores según el modelo del ejemplo, además para medir la concentración hay que utilizar la función iloc[] para cada punto y ponerla en el print() para que la muestre por
    la terminal.

    **3.** Realizado esto nos vemos al directorio outputs/test y ejecutamos python3 xy_values.py. Esto mostrará por la terminal los valores de concentración, que tendrán que añadirse al fichero sensor_data.csv. Una vez 
    realizado esto volvemos a poner como valores de flujo de emisión las distribuciones de probabilidad q1, q2...


# **Configuración del modelo _SfePy_:**

El archivo main.py que se encuentra en el directorio problem-descriptions/2D es el archivo de configuración de _SfePy_ y contiene toda la información sobre la ejecución del modelo, en él hay que 
cambiar algunos parámetros según el caso de uso.

- Las variables nombradas como q1, q2 etc son las distribuciones de probabilidad a priori de cada una de las fuentes, cuyo primer argumento es la media y segundo la desviación. No es obligatorio
    aunque así esté expuesto en el ejemplo que las distribuciones sean totalmente iguales, de hecho en posteriores versiones, cada distribución irá ajustada según un estudio previo, pues esto reduce
    considerablemente el número de simulaciones necesarias para obtener buenos resultados

- En el apartado materials = { } hay que añadir el flujo de emisión que corresponde con el número de la variable aleatoria para que en cada simulación se muestree a partir de estas distribuciones.

- La parte menos automatizada del modelo es la agregación del número de fuentes de emisión, para añadirlas es necesario seguir los siguientes pasos:

    1. En el fichero main.py aparecen unas funciones llamadas get_source_cells_{nº de fuente}, estas funciones son las que seleccionan el espacio del que se emite contaminante. Hay que crear tantas
        de estas funciones como número de fuentes tenga el caso de uso siguiendo la estructura que aparece en el ejemplo. El argumento radius es el radio del círculo de la superficie de la fuente puesto
        que estas se consideran circulares.

    2. En el apartado functions = {} se deben añadir cada una de las funciones anteriores seguiendo el modelo del ejemplo.

    3. En el apartado equations = {} se debe sumar en la parte derecha de la ecuación el término correspondiente con cada una de las fuentes siguiendo la estructura del ejemplo.

    4. Por último, en el diccionario regions = {} apartado #SOURCES deben seleccionarse las regiones correspondientes a cada una de las fuentes siguiendo el patrón del ejemplo. Debe haber tantas regiones como número de fuentes.


Para ejecutar el modelo es necesario estar en el directorio /montecarlo/ y poner en la terminal el comando `./montecarlo.sh {nº de simulaciones}` por ejemplo si queremos hacer 500 simulaciones el comando sería $`./montecarlo.sh 500`

Ejecutado esto, el modelo enseñará por la terminal el progreso de las simulaciones indicando el comienzo de cada una de ellas, por lo que es normal que esta salida quiera llevarse a un fichero aparte y ejecutarse en segundo plano, para ello 
podemos poner el comando $`./montecarlo 500 > exit.log &`

Una vez el algoritmo haya terminado todas las simulaciones dará los resultados en el fihero emissions_results.json, indicando el número de la fuente y la estimación de su flujo de emisión.


**NOTA**: Es importante que si se interrumpe la simulación y no se han eliminado los ficheros q_values.csv y error_values.csv en la carpeta outputs/test estos sean eliminados antes de empezar otra simulación de nuevo.

