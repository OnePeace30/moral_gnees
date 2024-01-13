import typing as T
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import _sa_util
import sqlalchemy as sa



class Base(DeclarativeBase):

    __abstract__ = True

    @classmethod
    def get_or_create(
        cls, session: sa.orm.Session, defaults=None, commit=True, **kwargs
    ):
        """Django-inspired get_or_create."""
        predicates = [getattr(cls, k) == v for k, v in kwargs.items()]
        instance = session.scalar(sa.select(cls).where(*predicates))
        if instance:
            return instance, False

        defaults = defaults or {}
        instance_kwargs = kwargs | defaults
        instance = cls(**instance_kwargs)
        session.add(instance)
        if commit:
            session.commit()

        return instance, True

article_to_uni = sa.Table('article_to_uni', Base.metadata, 
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('uni_id', sa.Integer(), ForeignKey("universities.id")),
    sa.Column('article_id', sa.Integer(), ForeignKey("related_articles.id"))
)

article_to_state = sa.Table('article_to_state', Base.metadata, 
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('state_id', sa.Integer(), ForeignKey("states.id")),
    sa.Column('artical_id', sa.Integer(), ForeignKey("related_articles.id"))
)

class State(Base):
    __tablename__ = 'states'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=True)

class Universities(Base):
    __tablename__ = 'universities'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=True)
    state_id = sa.Column(sa.Integer, sa.ForeignKey('states.id'))

class Sources(Base):
    __tablename__ = "sources"

    link_to_state = sa.Column(sa.Text, name='Link to state news 1', nullable=True)
    domain = sa.Column(sa.Text, name='domain', nullable=True, primary_key=True)
    link = sa.Column(sa.Text, name='link to google news', nullable=True)
    score = sa.Column(sa.Text, name='score of relevance to the university', nullable=True)
    words = sa.Column(sa.Text, name='Words to determine atisimitics event', nullable=True)
    university_name = sa.Column(sa.Text, name='University name1', nullable=True)
    state_name = sa.Column(sa.Text, name='State name1', nullable=True)
    university_id = sa.Column(sa.Text, sa.ForeignKey('universities.id'), name='university_id', nullable=True)
    state_id = sa.Column(sa.Text, sa.ForeignKey('states.id'), name='state_id', nullable=True)
    university = relationship('Universities')
    state = relationship('State')

class RelatedArticles(Base):
    __tablename__ = 'related_articles'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(255), nullable=True)
    link = sa.Column(sa.Text, nullable=True)
    text = sa.Column(sa.Text, nullable=True)
    pic = sa.Column(sa.Text, nullable=True)
    date = sa.Column(sa.DATETIME, nullable=True)
    university = sa.orm.relationship("Universities", secondary=article_to_uni, backref="articles")
    state = sa.orm.relationship("State", secondary=article_to_state, backref="articles")
    