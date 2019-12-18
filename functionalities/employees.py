from sqlalchemy import distinct, func, text, not_

from functionalities.employee_gifts import EmployeeGift
from models import db, Gift, EmployeeGift as EmployeeGiftModel, Employee as EmployeeModel, EmployeeInterest, \
    GiftCategory
from utilities.exceptions import ResourceDoesNotExist


class Employee(object):
    def __init__(self, employee_id, *args, **kwargs):
        self.id = employee_id
        super(Employee, self).__init__(*args, **kwargs)

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
        employee_gift = EmployeeGift()
        assigned_gift = employee_gift.get_employee_gift(self.id)
        if not assigned_gift:
            print('assigning gift')

            suitable_gift_ids = self.get_suitable_gift_ids()

            # find unassigned suitable gifts
            already_assigned_gift_ids = employee_gift.get_all_assigned_gift_ids()
            unassigned_suitable_gift_ids = suitable_gift_ids - already_assigned_gift_ids

            if unassigned_suitable_gift_ids:
                assigned_gift_id = next(iter(unassigned_suitable_gift_ids))
            else:
                print('no suitable gift found')
                # find the gift that cannot be given to others

                matched_gift_ids = self.get_all_matching_gift_ids()  # here we get the list of gifts that are
                # matching the user interests

                all_gift_ids = set(
                    [item[0] for item in db.session.query(distinct(Gift.id)).all()])
                unmatched_gift_ids = all_gift_ids - matched_gift_ids
                unmatched_gift_ids = unmatched_gift_ids - already_assigned_gift_ids

                # assign unmatched gift, if exists
                if unmatched_gift_ids:
                    assigned_gift_id = next(iter(unmatched_gift_ids))
                else:
                    # find the gift that has less categories, as even the gifts that no one wants are not available
                    available_gift_ids = all_gift_ids - already_assigned_gift_ids

                    if not available_gift_ids:
                        raise ResourceDoesNotExist('no gifts are available')

                    result = db.session.query(
                        GiftCategory.gift_id, func.count(GiftCategory.gift_id).label('category_count')
                    ).filter(
                        GiftCategory.gift_id.in_(list(available_gift_ids))
                    ).group_by(GiftCategory.gift_id).order_by(text('category_count asc')) \
                        .first()
                    assigned_gift_id = result[0]

            assigned_gift = employee_gift.create_employee_gift_record(self.id, assigned_gift_id,
                                                                      'gift assignment succeeded')

        return assigned_gift
