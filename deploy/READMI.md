Módulos y bibliotecas utilizados:
---------------------------------

-   `daemon`: Este módulo se utiliza para demonizar el proceso y ejecutarlo en segundo plano como un servicio.
-   `os`: Este módulo proporciona funciones para interactuar con el sistema operativo, en este caso, se utiliza para acceder a las variables de entorno del sistema.
-   `dotenv`: Es una biblioteca que carga variables de entorno desde un archivo `.env` en el directorio actual.

Variables:
----------

-   `environment`: Almacena el valor de la variable de entorno llamada "ENVIRONMENT".

Funciones:
----------

-   `run()`: Esta función es la parte principal del código. Verifica el valor de `environment`. Si es "production", crea un contexto de demonio y ejecuta la clase `ServiceApi` utilizando el método `start()`. Si no es "production", simplemente ejecuta la clase `ServiceApi` utilizando el método `start()` sin utilizar un contexto de demonio.

Punto de entrada:
-----------------

-   `if __name__ == '__main__':` verifica si el script se está ejecutando directamente como el punto de entrada principal. En caso