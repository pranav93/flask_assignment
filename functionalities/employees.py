from flask import current_app
from sqlalchemy import distinct

from functionalities.employee_gifts import EmployeeGift
from functionalities.gift_categories import GiftCategory
from models import db, Gift, Employee as EmployeeModel, EmployeeInterest, \
    GiftCategory as GiftCategoryModel
from utilities.exceptions import ResourceDoesNotExist


class Employee(object):
    def __init__(self, employee_id, *args, **kwargs):
        self.id = employee_id
        super(Employee, self).__init__(*args, **kwargs)

    def get_suitable_gift_ids(self):
        result = db.session.query(
            EmployeeModel, EmployeeInterest, GiftCategoryModel, Gift
        ).join(
            EmployeeModel, EmployeeModel.id == EmployeeInterest.employee_id
        ).join(
            GiftCategoryModel, GiftCategoryModel.category_id == EmployeeInterest.interest_id
        ).join(
            Gift, GiftCategoryModel.gift_id == Gift.id
        ).filter(EmployeeModel.id == self.id).all()

        suitable_gift_ids = {item[3].id for item in result}
        return suitable_gift_ids

    def get_all_matching_gift_ids(self):
        result = db.session.query(EmployeeModel, EmployeeInterest, GiftCategoryModel, Gift).join(
            EmployeeModel, EmployeeModel.id == EmployeeInterest.employee_id).join(
            GiftCategoryModel, GiftCategoryModel.category_id == EmployeeInterest.interest_id).join(
            Gift, GiftCategoryModel.gift_id == Gift.id).all()

        return set([item[3].id for item in result])

    def assign_gift(self):
        employee_gift = EmployeeGift()
        gift_category = GiftCategory()
        assigned_gift = employee_gift.get_employee_gift(self.id)
        if not assigned_gift:
            current_app.logger.info('no gift is assigned to employee with id {}'.format(self.id))
            current_app.logger.info('assigning gift')
            suitable_gift_ids = self.get_suitable_gift_ids()
            current_app.logger.debug('suitable gift ids for employee with id {} are {}'.format(
                self.id, suitable_gift_ids
            ))

            # find unassigned suitable gifts
            already_assigned_gift_ids = employee_gift.get_all_assigned_gift_ids()
            current_app.logger.debug('already assigned gift ids are {}'.format(already_assigned_gift_ids))
            unassigned_suitable_gift_ids = suitable_gift_ids - already_assigned_gift_ids
            current_app.logger.debug('unassigned suitable gift ids are {}'.format(unassigned_suitable_gift_ids))

            if unassigned_suitable_gift_ids:
                assigned_gift_id = next(iter(unassigned_suitable_gift_ids))
                current_app.logger.debug('assigning gift with id {} to employee with id {}'.format(
                    assigned_gift_id, self.id))
            else:
                current_app.logger.info('no suitable gift found')
                # find the gift that cannot be given to others

                matched_gift_ids = self.get_all_matching_gift_ids()  # here we get the list of gifts that are
                # matching the user interests

                all_gift_ids = set(
                    [item[0] for item in db.session.query(distinct(Gift.id)).all()])
                unmatched_gift_ids = all_gift_ids - matched_gift_ids
                unmatched_gift_ids = unmatched_gift_ids - already_assigned_gift_ids

                current_app.logger.debug('unwanted gift ids'.format(unmatched_gift_ids))

                # assign unmatched gift, if exists
                if unmatched_gift_ids:
                    assigned_gift_id = next(iter(unmatched_gift_ids))
                    current_app.logger.debug('assigning gift with id {} to employee with id {}'.format(
                        assigned_gift_id, self.id))
                else:
                    # find the gift that has less categories, as even the gifts that no one wants are not available
                    available_gift_ids = all_gift_ids - already_assigned_gift_ids
                    current_app.logger.debug('available gift ids are {}'.format(available_gift_ids))

                    if not available_gift_ids:
                        raise ResourceDoesNotExist('no gifts are available')
                    current_app.logger.info('finding the optimum gift id')
                    assigned_gift_id = gift_category.get_optimum_gift_id(list(available_gift_ids))
                    current_app.logger.debug('assigning gift with id {} to employee with id {}'.format(
                        assigned_gift_id, self.id))

            assigned_gift = employee_gift.create_employee_gift_record(self.id, assigned_gift_id,
                                                                      'gift assignment succeeded')
        current_app.logger.info('assigned gift id is {} for employee with id {}'.format(assigned_gift.id, self.id))

        return assigned_gift
