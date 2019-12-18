from models import db, Gift, Category, GiftCategory
from run import create_app
from scripts import gifts

if __name__ == '__main__':
    app = create_app("config")

    with app.app_context():
        for a_gift in gifts.gifts:
            gift_record = Gift(
                name=a_gift['name']
            )
            db.session.add(gift_record)
            db.session.flush()
            gift_record_id = gift_record.id

            for a_category in a_gift['categories']:
                category = Category.query.filter_by(name=a_category).first()
                if not category:
                    category = Category(
                        name=a_category
                    )
                    db.session.add(category)
                    db.session.flush()

                category_id = category.id
                gift_category_record = GiftCategory(
                    gift_id=gift_record_id,
                    category_id=category_id,
                )
                db.session.add(gift_category_record)
                db.session.flush()

        db.session.commit()
