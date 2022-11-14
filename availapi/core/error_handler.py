from flask import jsonify


# Return validation errors as JSON
def configure_error_handlers(app):
    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_errors(err):
        if err.code == 422:
            if hasattr(err, "data"):
                # Entering here meaning that the error was generated by marshmallow.
                errors_data = err.data["messages"]
            else:
                # Otherwise was a message generated from the flask.abort function.
                errors_data = {"json": {"_schema": [err.description]}}
        elif err.code == 400:
            errors_data = err.description
        return jsonify({"errors": errors_data}), err.code