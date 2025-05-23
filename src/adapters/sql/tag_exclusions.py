from sqlalchemy.dialects.mysql import insert
from src.adapters.sql import db

from src.helpers import to_dict
from src.models.tag_exclusion import TagExclusion


def insert_all(tag_exclusions, app):
    with app.app_context():
        stmt = insert(TagExclusion).values([to_dict(tag_exclusion) for tag_exclusion in tag_exclusions])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)

        db.session.execute(stmt)

        db.session.commit()
