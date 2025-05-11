from sqlalchemy import create_engine, text
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import sessionmaker
from prettytable import PrettyTable

from src.database import to_dict
from src.models import Condition, Club
from src.yaml_adapter import load_conditions


def validate_conditions(session):
    validation_table = PrettyTable(["ID", 'Status', '# Solutions', "Description", "Error Msg"])
    validation_table.align = "l"

    for condition in session.query(Condition).all():
        try:
            results = session.query(Club).filter(text(condition.expression)).all()

            status = "✅" if len(results) > 5 else "⚠️" if len(results) > 0 else "❌"

            validation_table.add_row([
                condition.id,
                status,
                len(results),
                condition.description,
                ""
            ])
        except Exception as error:
            validation_table.add_row([
                condition.id,
                "‼️",
                "-",
                condition.description,
                error.orig.msg
            ])
    return validation_table


url = "mysql+mysqlconnector://flaskuser:flaskpassword@localhost:3306/flaskdb"
engine = create_engine(url)

Session = sessionmaker(bind=engine)

session = Session()

all_conditions = load_conditions()
stmt = insert(Condition).values([to_dict(condition) for condition in all_conditions])
stmt = stmt.on_duplicate_key_update(stmt.inserted)
session.execute(stmt)
session.commit()

report = validate_conditions(session)

print(report)

session.close()
