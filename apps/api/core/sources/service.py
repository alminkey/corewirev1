from sqlalchemy import select

from ..db.models import Source


def list_active_sources(session):
    return session.scalars(select(Source).where(Source.active.is_(True))).all()


def create_source(session, **fields):
    source = Source(**fields)
    session.add(source)
    session.commit()
    return source

