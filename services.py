from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from typing import List, Optional, Tuple
import models, schemas
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



def get_pass_by_id(db: Session, pass_id: int) -> Optional[models.PerevalAdded]:
    pereval = db.query(models.PerevalAdded).options(
        joinedload(models.PerevalAdded.user),
        joinedload(models.PerevalAdded.coords),
        joinedload(models.PerevalAdded.images)
    ).filter(models.PerevalAdded.id == pass_id).first()

    return pereval


def get_passes_by_email(db: Session, email: str) -> List[models.PerevalAdded]:
    passes = db.query(models.PerevalAdded).options(
        joinedload(models.PerevalAdded.user),
        joinedload(models.PerevalAdded.coords),
        joinedload(models.PerevalAdded.images)
    ).join(models.User).filter(models.User.email == email).all()

    return passes


def update_pass_by_id(db: Session, pass_id: int, data: schemas.PerevalUpdateSchema) -> Tuple[int, str]:
    try:
        pereval = db.query(models.PerevalAdded).options(
            joinedload(models.PerevalAdded.coords),
            joinedload(models.PerevalAdded.images)
        ).filter(models.PerevalAdded.id == pass_id).first()

        if not pereval:
            return (0, f"Перевал с id={pass_id} не найден")

        if pereval.status != 'new':
            return (0, f"Нельзя редактировать перевал, статус: '{pereval.status}'")

        update_data = data.model_dump(exclude_unset=True)

        if 'beauty_title' in update_data:
            pereval.beauty_title = update_data['beauty_title']
        if 'title' in update_data:
            pereval.title = update_data['title']
        if 'other_titles' in update_data:
            pereval.other_titles = update_data['other_titles']
        if 'connect' in update_data:
            pereval.connect = update_data['connect']

        if 'level' in update_data:
            level_data = update_data['level']
            if 'winter' in level_data: pereval.level_winter = level_data['winter']
            if 'summer' in level_data: pereval.level_summer = level_data['summer']
            if 'autumn' in level_data: pereval.level_autumn = level_data['autumn']
            if 'spring' in level_data: pereval.level_spring = level_data['spring']

        if 'coords' in update_data:
            coords_data = update_data['coords']
            if 'latitude' in coords_data: pereval.coords.latitude = coords_data['latitude']
            if 'longitude' in coords_data: pereval.coords.longitude = coords_data['longitude']
            if 'height' in coords_data: pereval.coords.height = coords_data['height']

        if 'images' in update_data:
            for img in pereval.images:
                db.delete(img)
            pereval.images.clear()

            for img_data in data.images:
                image = models.Image(
                    data=img_data.data,
                    title=img_data.title
                )
                db.add(image)
                pereval.images.append(image)

        db.commit()
        return (1, "Запись успешно обновлена")

    except Exception as e:
        db.rollback()
        return (0, f"Ошибка при обновлении: {str(e)}")