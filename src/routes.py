from datetime import datetime
from typing import Any

from flask import request, Response, jsonify, Blueprint

from .database import db
from .models import User, Meal

main_bp = Blueprint('main_routes', __name__)

@main_bp.post('/user')
def create_user() -> Response | tuple[Response, int]:
    data: Any = request.json
    username: str = data.get('username')
    password: str = data.get('password')

    if username and password:
        user: User = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return create_response('Usuário cadastrado com sucesso!')

    return create_response('Dados inválidos', 400)


@main_bp.post('/meal')
def create_meal() -> Response | tuple[Response, int]:
    data: Any = request.json

    name: str = data.get('name')
    description: str = data.get('description')
    diet: bool = data.get('diet')
    username: str = data.get('username')
    date_str: str = data.get('date')
    date: datetime = datetime.fromisoformat(date_str) if date_str else None

    if name and description and diet is not None and username:
        user: User = User.query.filter_by(username=username).first()

        if user is None:
            return create_response(f'Usuário com username "{username}" não foi encontrado!', 404)

        meal: Meal = Meal(name=name, description=description, diet=diet, user=user)

        if date:
            meal.timestamp = date

        db.session.add(meal)
        db.session.commit()
        return create_response('Refeição criado com sucesso!')

    return create_response('Dados inválidos', 400)


@main_bp.patch('/meal/<int:id_meal>')
def update_meal(id_meal) -> Response:
    meal: Meal | None = Meal.query.get(id_meal)

    if not isinstance(id_meal, int) or id_meal <= 0:
        return create_response('Id da refeição inválida!', 400)

    if meal is None:
        return create_response('Refeição não encontrada!')

    data: Any = request.json

    name: str = data.get('name')
    description: str = data.get('description')
    diet: bool = data.get('diet')
    date_str: str = data.get('date')
    date: datetime = datetime.fromisoformat(date_str) if date_str else None

    if name:
        meal.name = name

    if description:
        meal.description = description

    if diet:
        meal.diet = diet

    if date:
        meal.timestamp = date

    db.session.commit()

    return create_response('Refeição atualizada com sucesso!')


@main_bp.delete('/meal/<int:id_meal>')
def delete_meal(id_meal: int) -> Response:
    if not isinstance(id_meal, int) or id_meal <= 0:
        return create_response('Id da refeição inválida!', 400)

    meal: Meal | None = Meal.query.get(id_meal)

    if meal is None:
        return create_response('Refeição não encontrada!')

    db.session.delete(meal)
    db.session.commit()

    return create_response('Refeição deletada com sucesso!')


@main_bp.get('/meal/<int:id_meal>')
def get_meal(id_meal: int):
    if not isinstance(id_meal, int) or id_meal <= 0:
        return create_response('Id do usuário inválido!', 400)

    meal: Meal | None = Meal.query.get(id_meal)

    if meal is None:
        return create_response('Refeição não encontrada!')

    return jsonify(meal.to_dict())


@main_bp.get('/meal/user/<int:id_user>')
def get_all_meal_by_user(id_user: int):
    if not isinstance(id_user, int) or id_user <= 0:
        return create_response('Id do usuário inválido!', 400)

    meals_query: list[Meal] = Meal.query.filter_by(user_id=id_user).all()
    meal_list: list[dict] = [m.to_dict() for m in meals_query]

    return jsonify(meal_list)


def create_response(message: str, status: int = None) -> tuple[Response, int] | Response:
    response: Response = jsonify({'message': message})
    return (response, status) if status else response
