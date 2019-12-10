from sqlalchemy import create_engine


def test_create_tables():
    from exemple_formation.models import Base
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

