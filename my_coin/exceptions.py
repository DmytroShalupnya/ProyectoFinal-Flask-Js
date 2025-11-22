class ExternalApiError(Exception):
    "Error al conectar con la Api de coin market"
    pass

class DatabaseError(Exception):
    "Algo salio mal al intentar conectar a la base de datos"
    pass

class TransactionError(Exception):
    "No se ha podido grabar la transaccion en la base de datos "
    pass

