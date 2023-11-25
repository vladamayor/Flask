from typing import Type

from flask import Flask, jsonify, request
from flask.views import MethodView
from pydantic import ValidationError

from models import Advertisements, Session
from schema import CreateAdv

app = Flask("app")


class HttpError(Exception):
    def __init__(self, status_code: int, error_message: dict | list | str):
        self.status_code = status_code
        self.error_message = error_message


def validate(schema: Type[CreateAdv], json_data):
    try:
        model = schema(**json_data)
        validated_data = model.model_dump(exclude_none=True)
    except ValidationError as er:
        raise HttpError(400, er.errors())
    return validated_data


@app.errorhandler(HttpError)
def error_hendler(er: HttpError):
    http_response = jsonify({"status": "error", "discription": er.error_message})
    http_response.status_code = er.status_code
    return http_response


@app.route("/api/advertisements", methods=["POST"])
def create_advertisement():
    json_data = validate(CreateAdv, request.json)

    with Session() as session:
        advertisement = Advertisements(**json_data)
        session.add(advertisement)
        session.commit()
        return jsonify(
            {"message": "Advertisement created successfully", "id": advertisement.id}
        )


@app.route("/api/advertisements/<int:advertisement_id>", methods=["GET"])
def get_advertisement(advertisement_id: int):
    with Session() as session:
        advertisement = session.get(Advertisements, advertisement_id)
        if advertisement is None:
            raise HttpError(404, "Advertisement not found")
        return jsonify(
            {
                "id": advertisement.id,
                "owner": advertisement.owner,
                "title": advertisement.title,
                "description": advertisement.description,
                "data": advertisement.data.isoformat(),
            }
        )


@app.route("/api/advertisements/<int:advertisement_id>", methods=["DELETE"])
def delete_advertisement(advertisement_id: int):
    with Session() as session:
        advertisement = session.get(Advertisements, advertisement_id)
        if advertisement is None:
            raise HttpError(404, "Advertisement not found")
        session.delete(advertisement)
        session.commit()
        return jsonify(
            {"message": "Advertisement deleted successfully", "id": advertisement.id }
            )



if __name__ == "__main__":
    app.run()