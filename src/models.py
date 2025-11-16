from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    characters: Mapped[list["Character"]] = relationship(
        secondary="favorite_characters", back_populates="users"
    )
    planets: Mapped[list["Planet"]] = relationship(
        secondary="favorite_planets", back_populates="users"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Character(db.Model):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(10), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(10), nullable=False)

    users: Mapped[list["User"]] = relationship(
        secondary="favorite_characters", back_populates="characters")


class Planet(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    # ¡user_id ELIMINADO!
    name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    population: Mapped[int] = mapped_column(Integer, nullable=False)
    diameter: Mapped[int] = mapped_column(Integer, nullable=False)
    terrain: Mapped[str] = mapped_column(String(20), nullable=False)

    users: Mapped[list["User"]] = relationship(
        secondary="favorite_planets", back_populates="planets")


class Vehicle(db.Model):
    __tablename__ = "vehicles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    crew: Mapped[int] = mapped_column(Integer, nullable=False)
    model: Mapped[str] = mapped_column(String(20), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(40), nullable=False)


class FavoriteCharacter(db.Model):
    __tablename__ = "favorite_characters"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))

    user: Mapped["User"] = relationship()
    character: Mapped["Character"] = relationship()


class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planets"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))

    user: Mapped["User"] = relationship()
    planet: Mapped["Planet"] = relationship()