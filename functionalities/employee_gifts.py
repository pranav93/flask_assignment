from sqlalchemy import distinct

from models import db, EmployeeGift as EmployeeGiftModel, Gift


class EmployeeGift(object):

    def __init__(self, *args, **kwargs):
        super(EmployeeGift, self).__init__(*args, **kwargs)

    def get_all_assigned_gift_ids(self):
        return set(
            [item[0] for item in db.session.query(distinct(EmployeeGiftModel.gift_id)).all()])

    def get_employee_gift(self, employee_id):
        gift = None
        employee_gift = EmployeeGiftModel.query.filter_by(employee_id=employee_id).first()
        if employee_gift and employee_gift.status == 'gift assignment succeeded':
            gift = Gift.query.filter_by(id=employee_gift.gift_id).first()
        return gift

    def create_employee_gift_record(self, employee_id, assigned_gift_id, status):
        employee_gift_record = EmployeeGiftModel()
        employee_gift_record.employee_id = employee_id
        employee_gift_record.gift_id = assigned_gift_id
        employee_gift_record.status = status
        db.session.add(employee_gift_record)
        db.session.commit()
        assigned_gift = Gift.query.filter_by(id=assigned_gift_id).first()
        return assigned_gift
