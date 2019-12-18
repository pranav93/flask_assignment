from run import create_app
from models import db, Employee, Category, EmployeeInterest
from scripts import employees

if __name__ == '__main__':
    app = create_app("config")

    with app.app_context():
        for an_employee in employees.employees:
            employee_record = Employee(
                name=an_employee['name']
            )
            db.session.add(employee_record)
            db.session.flush()
            employee_record_id = employee_record.id

            for an_interest in an_employee['interests']:
                category = Category.query.filter_by(name=an_interest).first()
                if not category:
                    category = Category(
                        name=an_interest
                    )
                    db.session.add(category)
                    db.session.flush()

                category_id = category.id
                employee_interest_record = EmployeeInterest(
                    employee_id=employee_record_id,
                    interest_id=category_id,
                )
                db.session.add(employee_interest_record)
                db.session.flush()

        db.session.commit()
