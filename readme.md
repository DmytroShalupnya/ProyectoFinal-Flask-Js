## Antes de empezar
# instalacion
- Crea una base de datos sqlite tres y añade su path en la variable DATA_BASE en config.py 
- Registrate en api.coinmarketcap.com para conseguir una api key e insertala en la variable API_KEY en config.py
- crea un entorno virtual e instala los elementos necesarios desde requirements.txt.

## MyCoin — App de práctica para compra/venta y tradeo de criptomonedas

MyCoin es una pequeña aplicación de práctica construida con Flask + SQLite y un front-end en una sola vista (`templates/index.html`) que permite:

- Consultar y listar movimientos de compra/venta.
- Calcular cambios entre monedas (incluido EUR y varias cripto) a precio de mercado en tiempo real usando la API de CoinMarketCap.
- Registrar compras/ventas y actualizar un “wallet” local.
- Ver en todo momento un panel de estado con métricas de inversión.

Importante: es un proyecto didáctico. Los euros son “infinitos”: no se lleva un saldo de EUR, puedes comprar con cualquier cantidad de EUR sin restringir por disponibilidad. Esto facilita el aprendizaje del flujo de compra/venta sin gestión de efectivo.

## Estado y métricas mostradas

La app expone y presenta un bloque de “Status” en la vista única con estos valores (implementados en `my_coin/conection.py`, clase `Status`):

- invested: EUR invertidos (suma de `amount_from` cuando `coin_from = 'EUR'`).
- recovered: EUR recuperados (suma de `amount_to` cuando `coin_to = 'EUR'`).
- valorCompra: invertido − recuperado (coste neto).
- wallet: valor actual del wallet sumando precios de mercado de las criptos en cartera (consulta en vivo a la API).
- diference: variación porcentual respecto a valorCompra: `((wallet − valorCompra) / valorCompra) × 100`.

Estas métricas también están disponibles vía API en `/api/v1/status` y se actualizan en la interfaz con JavaScript.

## Arquitectura rápida

- Backend: Flask (Python) con CORS habilitado.
- Base de datos: SQLite .
- Front-end: Una sola vista (`templates/index.html`) + Bootstrap + JS en `static/js/app.js` para interactuar con la API.
- Integración externa: CoinMarketCap Pro API para precios en EUR.

## Endpoints principales (API)

- GET `/api/v1/tasa/<moneda_from>/<moneda_to>?amount=<n>`
  - Calcula cuánto recibirías de `moneda_to` al intercambiar `amount` de `moneda_from`.
  - Respuesta: `{ "purchasedAmount": <n>, "status": "success" }`.

- GET `/api/v1/movimientos`
  - Devuelve todos los movimientos registrados (fecha/hora, moneda origen/destino, cantidades y precio unitario).

- POST `/api/v1/compra`
  - Registra una compra/venta o trade entre cripto.
  - Cuerpo JSON esperado: `{ "moneda_from", "amount_from", "moneda_to", "amount_to" }`.

- GET `/api/v1/status`
  - Devuelve las métricas descritas en la sección “Estado y métricas”.

- GET `/`
  - Renderiza la vista única con el formulario de conversión y el panel de estado.

## Requisitos

Dependencias directas usadas por el proyecto:

- Flask
- flask-cors
- requests
- python-dotenv
- JInja2 


## Configuración

1) Python y entorno

- Python 3.11+ recomendado (funciona también con 3.13).
- Crea y activa un virtualenv.
- Instala dependencias:

```cmd
pip install -r requirements.txt
```

1. API Key de CoinMarketCap

- Regístrate en <https://coinmarketcap.com/api/> para obtener una API Key.
- Edita `config.py` y pon tu clave en `API_KEY`.

1. Base de datos SQLite

- La ruta del archivo está en `config.py` como `DATA_BASE = "data/movimientos.db"`.
- Crea el archivo y las tablas ejecutando el SQL de `data/create.sql`. Por ejemplo, en Windows con `sqlite3` disponible en PATH:

```cmd
sqlite3 data\movimientos.db ".read data/create.sql"
```

Si no tienes `sqlite3` en consola, puedes abrir cualquier GUI/cliente SQLite y ejecutar el contenido de `data/create.sql` sobre `data/movimientos.db`.

## Ejecución (Windows, cmd)

La aplicación expone el objeto `app` en `my_coin/__init__.py`. Puedes lanzarla con Flask CLI:

```cmd
set FLASK_APP=my_coin
set FLASK_ENV=development
flask run
```

Luego visita <http://127.0.0.1:5000/>

## Flujo de uso

1) Abre la app en el navegador.
2) En el formulario, selecciona moneda origen y destino e introduce un importe. Pulsa “Get Price” para calcular la conversión al precio actual de mercado.
3) Confirma la compra/venta en el modal “Purchase Ticket”.
4) La tabla de movimientos y el panel de estado se actualizarán automáticamente.

Recuerda: los euros son infinitos en este entorno de práctica; no se controla el saldo de EUR para las compras pero si para la venta.

## Estructura de datos

Tablas principales (ver `data/create.sql`):

- movements: historial de operaciones (datetime, coin_from, amount_from, coin_to, amount_to, price_per_unit).
- wallet: saldo por moneda (se recalcula/actualiza tras cada operación).

## Limitaciones y notas

- Proyecto educativo: sin autenticación, sin roles, sin concurrencia avanzada.
- EUR infinito: no se gestiona caja de EUR; sirve para practicar el flujo.
- El valor del wallet consulta precios en vivo; no hay caché ni históricos.
- Manejo de errores centralizado en `my_coin/error_handler.py` con respuestas JSON para rutas `/api/*` y páginas HTML para el resto.

## Cambios para la reentrega.

- He cambiado la forma de procesar todos los datos. PAra mantener la coma floatante como es debido, la base de datos ahora funciona con string y solo cambiando a Decimal cuando es necesario hacer operaciones.
- He añadido control de datos para hacer las comprobaciones antes de insertar los datos en la base de datos pasando por la clase controlador.
- He solucionado el calculo del vwallet y he corregido el calculo de status.
- Corregida la implementacion del wallet, ahora actualiza cada moneda con la se se opera exceptuando el euro.
- He movido todas las operaciones matematicas de la base de datos al servidor. utilizando la base de datos unicamente para almacenar.
- He añadido el archivo requirements.txt 
- He realizado cambios en el diseño y he mejorado la funcionalidad.
- He reducido a 7 el numero de decimales con los que se trabaja ya que incluso para las moneda mas caras un 0.0000001 ya que con el cambio a eur es menos de 0.01 euros
- He añadido mejoras a la funcionalidad.

## Créditos / Licencia

Proyecto de práctica para aprendizaje de Flask, consumo de APIs y front-end básico con una sola vista.
Creado Por Dmytro Shalupnya. Practica final de Keep coding!
"# ProyectoFinal-Flask-Js" 
"# ProyectoFinal-Flask-Js" 
