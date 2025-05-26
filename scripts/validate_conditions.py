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
from src.models.grid_type import GridType


def validate_conditions(session):

    grid_types = session.query(GridType).all()

    columns = ["ID", 'Sts', "Tags", "Description", "Error Message", "Total"]

    for grid_type in grid_types:
        columns.append(grid_type.id)

    validation_table = PrettyTable(columns)
    validation_table.align = "l"

    for condition in session.query(Condition).all():
        try:
            results = session.query(Club).filter(text(condition.expression)).all()

            status = "🟩" if len(results) > 5 else "⚠️" if len(results) > 0 else "🟨"

            base_row = [
                condition.id,
                status,
                condition.tag,
                condition.description,
                "",
                len(results),
            ]

            for grid_type in grid_types:
                base_row.append(len(session.query(Club).filter(text(grid_type.expression)).filter(text(condition.expression)).all()))


            validation_table.add_row(base_row)
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
