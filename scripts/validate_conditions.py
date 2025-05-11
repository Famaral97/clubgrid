from sqlalchemy import create_engine, insert, text
from sqlalchemy.orm import sessionmaker
from prettytable import PrettyTable

from models import Condition, Club


def validate_conditions(session):
    all_conditions = session.query(Condition).all()

    validation_table = PrettyTable(["ID", 'Status', '# Solutions', "Description", "Error Msg"])
    validation_table.align = "l"

    for condition in all_conditions:
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

# Condition.query.delete()

report = validate_conditions(session)

print(report)
