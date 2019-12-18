from sqlalchemy import func, text

from models import db, GiftCategory as GiftCategoryModel


class GiftCategory(object):

    def __init__(self, *args, **kwargs):
        super(GiftCategory, self).__init__(*args, **kwargs)

    def get_optimum_gift_id(self, available_gift_ids):
        result = db.session.query(
            GiftCategoryModel.gift_id, func.count(GiftCategoryModel.gift_id).label('category_count')
        ).filter(
            GiftCategoryModel.gift_id.in_(available_gift_ids)
        ).group_by(GiftCategoryModel.gift_id).order_by(text('category_count asc')) \
            .first()
        return result[0]
