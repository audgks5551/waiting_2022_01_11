from django.db import models

#
from core import models as core_models
from users.models import User

class AbstractItem(core_models.TimeStampedModel):

    """ 추상화 """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class StoreType(AbstractItem):

    """ 가게 종류 모델 정의 """

    class Meta:
        verbose_name = "Food Type"

class FoodType(AbstractItem):

    """ 음식 종류 모델 정의 """

    class Meta:
        verbose_name = "Food Detail Type"

class Amenity(AbstractItem):

    """ 편의 시설 모델 정의 """

    class Meta:
        verbose_name_plural = "Amenities"

class Tag(AbstractItem):

    """ 태그 모델 정의"""

    class Meta:
        verbose_name_plural = "tags"

class Image(models.Model):

    """ 이미지 업로드 모델 정의 """

    store = models.ForeignKey("Store", related_name="images", on_delete=models.CASCADE)
    file = models.ImageField(blank=True, upload_to="stores/images")


class Store(models.Model):

    """ 가게 모델 정의 """

    name    = models.CharField("가게 이름", max_length=30)
    qrcode  = models.ImageField(blank=True, upload_to="stores/qrcode/")
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField("가게 주소",max_length=140, default="")
    store_type = models.ForeignKey(
        "StoreType", related_name="stores", on_delete=models.SET_NULL, null=True
    )
    food_type = models.ForeignKey(
        "FoodType", related_name="stores", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField(
        "Amenity", related_name="stores", blank=True
    )
    tags = models.CharField("태그",max_length=200, default="")


    def __str__(self):
        return str(f"{self.name}")
    
    def first_image(self):
        try:
            image, = self.images.all()[:1]
            return image.file.url
        except ValueError:
            return None

    def get_images(self):
        images = self.images.all()
        return images





