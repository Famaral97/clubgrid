from sqlalchemy import create_engine, text
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import sessionmaker
from prettytable import PrettyTable

from src.adapters.yaml import load_conditions
from src.helpers import to_dict
from src.models.club import Club
from src.models.grid import Grid
from src.models.answer import Answer
from src.models.condition import Condition


def validate_conditions(session):
    validation_table = PrettyTable(["ID", 'Sts', '# Sols', "Tags", "Description", "Error Message"])
    validation_table.align = "l"

    for condition in session.query(Condition).all():
        try:
            results = session.query(Club).filter(text(condition.expression)).all()

            status = "🟩" if len(results) > 5 else "⚠️" if len(results) > 0 else "🟨"

            validation_table.add_row([
                condition.id,
                status,
                len(results),
                condition.tag,
                condition.description,
                ""
            ])
        except Exception as error:
            validation_table.add_row([
                condition.id,
                "🟥",
                "-",
                condition.tag,
                condition.description,
                error.orig.msg
            ])
    return validation_table


url = "mysql+mysqlconnector://flaskuser:flaskpassword@localhost:3306/flaskdb"
engine = create_engine(url)

Session = sessionmaker(bind=engine)

session = Session()

all_conditions = load_conditions()

session.query(Answer).delete()
session.query(Grid).delete()
session.query(Condition).delete()
session.commit()

stmt = insert(Condition).values([to_dict(condition) for condition in all_conditions])
stmt = stmt.on_duplicate_key_update(stmt.inserted)
session.execute(stmt)
session.commit()

report = validate_conditions(session)

print(report)

session.close()
