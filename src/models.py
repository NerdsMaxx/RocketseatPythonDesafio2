from datetime import datetime
from typing import List

from sqlalchemy import String, TIMESTAMP, false, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

from .database import db  # <<< CORREÇÃO APLICADA AQUI (import relativo)


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    role: Mapped[str] = mapped_column(String(80), nullable=False, default='user')

    # Relacionamento: Um usuário tem muitas refeições
    # "Meal" é o nome da classe do outro lado do relacionamento.
    # back_populates="user" liga este relacionamento ao atributo 'user' na classe Meal.
    # O tipo é List["Meal"] porque um usuário pode ter uma lista de refeições.
    meals: Mapped[List["Meal"]] = relationship(back_populates="user")


class Meal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(250))
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    diet: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # Chave Estrangeira (Foreign Key)
    # "user.id" refere-se à coluna 'id' na tabela 'user'.
    # O nome da tabela 'user' é inferido do nome da classe User.
    # Se User tivesse __tablename__ = 'users_table', aqui seria 'users_table.id'.
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    # Relacionamento: Muitas refeições pertencem a um usuário
    # "User" é o nome da classe do outro lado.
    # back_populates="meals" liga este relacionamento ao atributo 'meals' na classe User.
    user: Mapped["User"] = relationship(back_populates="meals")

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'diet': self.diet,
            'date': self.timestamp.isoformat(),
            'username': self.user.username,
        }
