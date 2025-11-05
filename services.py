from sqlalchemy.orm import Session
from . import models, schemas
import datetime


def submit_data(db: Session, data: schemas.PerevalInputSchema) -> int:
    try:
        user_data = data.user
        user = db.query(models.User).filter(models.User.email == user_data.email).first()

        if not user:
            user = models.User(
                email=user_data.email,
                fam=user_data.fam,
                name=user_data.name,
                otc=user_data.otc,
                phone=user_data.phone
            )
            db.add(user)
        else:
            user.fam = user_data.fam
            user.name = user_data.name
            user.otc = user_data.otc
            user.phone = user_data.phone

        db.flush()

        coords_data = data.coords
        coords = models.Coords(
            latitude=coords_data.latitude,
            longitude=coords_data.longitude,
            height=coords_data.height
        )
        db.add(coords)
        db.flush()

        level_data = data.level
        pereval = models.PerevalAdded(
            beauty_title=data.beauty_title,
            title=data.title,
            other_titles=data.other_titles,
            connect=data.connect,
            add_time=data.add_time,

            status="new",

            level_winter=level_data.winter,
            level_summer=level_data.summer,
            level_autumn=level_data.autumn,
            level_spring=level_data.spring,

            user_id=user.id,
            coord_id=coords.id
        )
        db.add(pereval)
        db.flush()

        for img_data in data.images:
            image = models.Image(
                data=img_data.data,
                title=img_data.title
            )
            db.add(image)
            pereval.images.append(image)

        db.commit()

        return pereval.id

    except Exception as e:
        db.rollback()
        raise e