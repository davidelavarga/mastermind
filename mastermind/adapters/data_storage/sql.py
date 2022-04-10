import logging
import os
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.engine import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from sqlalchemy_utils import create_database, database_exists

from mastermind.domain.models.exceptions import GameNotFound
from mastermind.domain.models.guess import Guess
from mastermind.domain.models.status import GameStatus
from mastermind.domain.ports import DataStorage
from mastermind.utils.config_loader import get_config

Base = declarative_base()


class Codes(Base):
    __tablename__ = "codes"

    id = Column(Integer, primary_key=True)
    code = Column(String)
    date = Column(DateTime)
    solved = Column(Boolean)
    surrendered = Column(Boolean)
    guesses = relationship("Guesses")


class Guesses(Base):
    __tablename__ = "guesses"

    id = Column(Integer, primary_key=True)
    code_id = Column(Integer, ForeignKey(Codes.id))
    guess = Column(String)
    black_pegs = Column(Integer)
    white_pegs = Column(Integer)


# TODO Improve with session blocks
class SQLStorage(DataStorage):
    def __init__(self):
        self._config = get_config()["data_storage"]["sql"]
        db_conn_str = self._get_database_conn_str()
        self._engine = create_engine(db_conn_str)
        self._create_database()
        self._create_tables()

    def initialize_game(self, code: str) -> int:
        """Store a new game code"""
        game = Codes(code=code, date=datetime.now(), solved=False, surrendered=False)
        game_id = self._insert(game)
        logging.info("Game code stored in database")
        return game_id

    def get_secret_code(self, game_id: int) -> str:
        """Get the secret code of the given game id"""
        game = self._get_game(game_id)
        return game.code

    def get_status(self, game_id: int) -> GameStatus:
        """Get the current status of the given game"""
        game = self._get_game(game_id)
        last_guess = self._get_last_guess(game_id)

        if last_guess:
            return GameStatus(
                solved=game.solved,
                black_pegs=last_guess.black_pegs,
                white_pegs=last_guess.white_pegs,
                guess_code=last_guess.guess,
            )
        return GameStatus(solved=game.solved)

    def store_guess(
        self, game_id: int, guess: str, black_pegs: int, white_pegs: int
    ) -> int:
        """Store the given guess for the given game"""
        guess_id = self._insert(
            Guesses(
                code_id=game_id,
                guess=guess,
                black_pegs=black_pegs,
                white_pegs=white_pegs,
            )
        )
        logging.info(f"Guess {guess_id} for code {game_id} stored in database")
        return guess_id

    def is_game_solved(self, game_id: int) -> bool:
        """True if given game solved, False otherwise"""
        return self._get_game(game_id).solved

    def resolve_game(self, game_id: int):
        """Resolve the game"""
        with Session(bind=self._engine) as session:
            session.query(Codes).filter(Codes.id == game_id).update(
                {Codes.solved: True}
            )
            try:
                session.commit()
            except SQLAlchemyError as e:
                logging.exception(e)
                session.rollback()

    def get_guesses(self, game_id: int) -> int:
        """Get all guesses for the given game"""
        logging.info(f"Getting last guess for {game_id} from db ...")
        with Session(bind=self._engine) as session:
            guesses = session.query(Guesses).filter(Guesses.code_id == game_id).all()

        return [
            Guess(
                id=g.id, code=g.guess, black_pegs=g.black_pegs, white_pegs=g.white_pegs
            )
            for g in guesses
        ]

    def surrender(self, game_id: int):
        """Set the game as finished and return the secret code"""
        with Session(bind=self._engine) as session:
            session.query(Codes).filter(Codes.id == game_id).update(
                {Codes.surrendered: True}
            )
            try:
                session.commit()
            except SQLAlchemyError as e:
                logging.exception(e)
                session.rollback()

    def _get_database_conn_str(self):
        db_conn_str = os.environ["DB_CONN_STR"]
        db_name = self._config["db_name"]
        if db_conn_str.endswith("/"):
            db_conn_str = db_conn_str[:-1]

        db_conn_str = f"{db_conn_str}/{db_name}"
        if self._config.get("sslmode_required", False):
            db_conn_str = f"{db_conn_str}?sslmode=require"

        return db_conn_str

    def _create_database(self):
        logging.info("Creating DB")
        if not database_exists(self._engine.url):
            create_database(self._engine.url)

    def _create_tables(self):
        Codes.__table__.create(bind=self._engine, checkfirst=True)
        Guesses.__table__.create(bind=self._engine, checkfirst=True)

    def _get_game(self, game_id: int):
        logging.info(f"Getting game {game_id} from db ...")
        with Session(bind=self._engine) as session:
            game = session.query(Codes).filter(Codes.id == game_id).one_or_none()

        if not game:
            raise GameNotFound(f"Game {game_id} not found")
        return game

    def _get_last_guess(self, game_id: int):
        logging.info(f"Getting last guess for {game_id} from db ...")
        with Session(bind=self._engine) as session:
            max_id = session.query(func.max(Guesses.id))
            guess = (
                session.query(Guesses)
                .filter(
                    Guesses.code_id == game_id, Guesses.id == max_id.scalar_subquery()
                )
                .one_or_none()
            )
        return guess

    def _insert(self, base_object: Base):
        with Session(bind=self._engine) as session:
            session.add(base_object)
            session.flush()
            session.refresh(base_object)
            obj_id = base_object.id
            try:
                session.commit()
            except SQLAlchemyError as e:
                logging.exception(e)
                session.rollback()
        return obj_id
