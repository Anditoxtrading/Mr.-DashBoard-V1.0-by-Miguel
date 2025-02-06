Mr. DashBoard - Bybit Futures Dashboard

Descripción

Mr. DashBoard es una aplicación desarrollada en Python con Dash que permite visualizar y analizar datos de operaciones en Bybit Futures. Utiliza la API de Bybit para obtener información sobre el PnL (Profit and Loss), operaciones ganadas y perdidas, distribución de monedas operadas y diversos gráficos interactivos para mejorar el análisis de trading.

Requisitos

Para ejecutar esta aplicación, necesitas instalar las siguientes dependencias:

pip install dash dash-bootstrap-components plotly pybit

Configuración

Clona este repositorio o descarga los archivos del proyecto.

Crea un archivo config.py en la raíz del proyecto y añade tus credenciales de API de Bybit:

api_key = "TU_API_KEY"
api_secret = "TU_API_SECRET"

Ejecución

Para iniciar la aplicación, ejecuta el siguiente comando en la terminal:

python nombre_del_script.py

Luego, abre tu navegador y accede a http://127.0.0.1:8050/ para ver el dashboard en acción.

Funcionalidades

Consulta de PnL en un rango de fechas determinado.

Visualización de operaciones ganadas y perdidas.

Gráficos interactivos de distribución de ganancias y pérdidas.

Análisis de PnL por horas y días de la semana.

Identificación de las monedas más rentables.

Notas

La API de Bybit puede tener restricciones en cuanto al número de solicitudes por minuto. Revisa la documentación oficial si necesitas más información.

Asegúrate de utilizar credenciales seguras y no compartirlas públicamente.

Licencia

Este proyecto es de código abierto y se puede modificar y distribuir libremente bajo los términos de la licencia MIT.
