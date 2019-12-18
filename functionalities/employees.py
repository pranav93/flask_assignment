from sqlalchemy import distinct, func, text, not_

from models import db, Gift, EmployeeGift as EmployeeGiftModel, Employee as EmployeeModel, EmployeeInterest, \
    GiftCategory
from utilities.exceptions import ResourceDoesNotExist


class Employee(object):
    def __init__(self, employee_id):
        self.id = employee_id

    def get_gift(self):
        gift = None
        employee_gift = EmployeeGiftModel.query.filter_by(employee_id=self.id).first()
        if employee_gift and employee_gift.status == 'gift assignment succeeded':
            gift = Gift.query.filter_by(id=employee_gift.gift_id).first()
        return gift

    def get_suitable_gift_ids(self):
        result = db.session.query(
            EmployeeModel, EmployeeInterest, GiftCategory, Gift
        ).join(
            EmployeeModel, EmployeeModel.id == EmployeeInterest.employee_id
        ).join(
            GiftCategory, GiftCategory.category_id == EmployeeInterest.interest_id
        ).join(
            Gift, GiftCategory.gift_id == Gift.id
        ).filter(EmployeeModel.id == self.id).all()

        suitable_gift_ids = {item[3].id for item in result}
        return suitable_gift_ids

    def get_all_matching_gift_ids(self):
        result = db.session.query(EmployeeModel, EmployeeInterest, GiftCategory, Gift).join(
            EmployeeModel, EmployeeModel.id == EmployeeInterest.employee_id).join(
            GiftCategory, GiftCategory.category_id == EmployeeInterest.interest_id).join(
            Gift, GiftCategory.gift_id == Gift.id).all()

        return set([item[3].id for item in result])

    def assign_gift(self):
        assigned_gift = self.get_gift()
        if not assigned_gift:
            print('assigning gift')

            suitable_gift_ids = self.get_suitable_gift_ids()

            # todo: unassigned gifts
            already_assigned_gift_ids = set([item[0] for item in db.session.query(distinct(EmployeeGiftModel.gift_id)).all()])

            unassigned_gift_ids = suitable_gift_ids - already_assigned_gift_ids

            if unassigned_gift_ids:
                assigned_gift_id = next(iter(unassigned_gift_ids))
            else:
                print('no suitable gift found')
                # todo: find the gift that cannot be given to others

                matched_gift_ids = self.get_all_matching_gift_ids()
                all_gift_ids = set(
                    [item[0] for item in db.session.query(distinct(Gift.id)).all()])
                unmatched_gift_ids = all_gift_ids - matched_gift_ids
                unmatched_gift_ids = unmatched_gift_ids - already_assigned_gift_ids

                # assign unmatched gift, if exists
                if unmatched_gift_ids:
                    assigned_gift_id = next(iter(unmatched_gift_ids))
                else:
                    # find the gift that has less categories
                    available_gift_ids = all_gift_ids - already_assigned_gift_ids

                    if not available_gift_ids:
                        raise ResourceDoesNotExist('no suitable gift found')

                    result = db.session.query(
                        GiftCategory.gift_id, func.count(GiftCategory.gift_id).label('category_count')
                    ).filter(
                        GiftCategory.gift_id.in_(list(available_gift_ids))
                    ).group_by(GiftCategory.gift_id).order_by(text('category_count asc')) \
                        .first()
                    assigned_gift_id = result[0]

            employee_gift_record = EmployeeGiftModel()
            employee_gift_record.employee_id = self.id
            employee_gift_record.gift_id = assigned_gift_id
            employee_gift_record.status = 'gift assignment succeeded'
            db.session.add(employee_gift_record)
            db.session.commit()
            assigned_gift = Gift.query.filter_by(id=assigned_gift_id).first()

        return assigned_gift
