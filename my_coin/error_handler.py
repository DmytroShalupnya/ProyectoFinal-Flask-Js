from my_coin import app

from flask import render_template, request, jsonify
from my_coin.exceptions import ExternalApiError, DatabaseError, TransactionError

def register_error_handlers(app):
    """
    Registra todos los manejadores de errores para la API REST
    """
    
    @app.errorhandler(404)
    def not_found(error):
        error_to_show = "Lo sentimos!\
            Pagina no encontrada..."
        if request.path.startswith('/api/'):
            return jsonify({"error": "Pagina no encontrada", "codigo": 404}), 404
        return render_template('errors.html', 
                             error_code=404, 
                             error_message=error_to_show), 404
    
    @app.errorhandler(ExternalApiError)
    def handle_api_error(error):
        app.logger.error(f"Error API externa: {str(error)}")
        print(str(error))
        error_to_show = "Fallo al conectar con la Api de Coin Market"
        if request.path.startswith('/api/'):
            
            return jsonify({
                "error":error_to_show,
                "tipo": "API_EXTERNA",
                "codigo": 503
            }), 503
        return render_template('errors.html', 
                             error_code=503, 
                             error_message=error_to_show), 503
    
    @app.errorhandler(DatabaseError)
    def handle_db_error(error):
        error_to_show = "Fallo al intentar conectar con la base de datos. \
            Por favor revise su configuracion y consulte el Readme adjunto."
        app.logger.error(f"Error BD: {str(error)}")
        print(str(error))
        if request.path.startswith('/api/'):
            return jsonify({
                "error": error_to_show,
                "tipo": "BASE_DATOS",
                "codigo": 500
            }), 500
        return render_template('errors.html', 
                             error_code=500, 
                             error_message=error_to_show), 500
    
    @app.errorhandler(TransactionError)
    def handle_transaction_error(error):
        error_to_show = "Fallo al intentar inscribir la compra en la base de datos.\
            Por favor revise su configuracion y consulte el Readme adjunto."
        app.logger.error(f"Error transacción: {str(error)}")
        print(str(error))
        if request.path.startswith('/api/'):
            return jsonify({
                "error": error_to_show,
                "tipo": "TRANSACCION",
                "codigo": 400
            }), 400
        return render_template('errors.html', 
                             error_code=400, 
                             error_message=error_to_show), 400
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        error_to_show = "Vaya!\
            Ha ocurrido algo inesperado, por favor intentelo mas tarde o contacte al soporte tecnico. "
        app.logger.error(f"Error inesperado: {str(error)}")
        print(str(error))
        if request.path.startswith('/api/'):
            return jsonify({
                "error": error_to_show,
                "detalle": str(error),
                "codigo": 500
            }), 500
        return render_template('errors.html', 
                             error_code=500, 
                             error_message=error_to_show), 500