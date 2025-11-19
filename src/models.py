from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default=True)
    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
    
    @staticmethod
    def all_users():
        return User.query.all()


class People(db.Model):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    height: Mapped[str] = mapped_column(String(10), nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "gender": self.gender,
        }
    
    @staticmethod
    def get_all_people():
        return People.query.all()

class Planet(db.Model):
    __tablename__ = "planets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    terrain: Mapped[str] = mapped_column(
        String(120), unique=False, nullable=False)
    population: Mapped[str] = mapped_column(
        String(10), unique=False, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "population": self.population,
        }
    
    @staticmethod
    def all_planets():
        return Planet.query.all()


class Favorite(db.Model):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True)
    user: Mapped[User] = relationship(back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
        }