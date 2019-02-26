from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Pet(models.Model):

    SEX_CHOICES = (
        (0,'オス'),
        (1,'メス'),
        (2,'秘密'),
    )

    PET_CHOICES = (
        (0,'犬'),
        (1,'猫'),
        (2,'その他'),
    )

    name = models.CharField(max_length=40)
    owner = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
    sex = models.IntegerField(
        verbose_name = '性別',
        choices = SEX_CHOICES,
        default = 0
    )
    together_with = models.IntegerField(
        verbose_name = 'いつから一緒にいますか？',
        default=1985,
        validators=[MinValueValidator(1985)]
    )
    pet_type = models.IntegerField(
        verbose_name = 'ペットの種類',
        choices = PET_CHOICES,
        default = 0
    )
    created_at = models.DateTimeField(default=timezone.now)


class Photo(models.Model):

    image = models.ImageField(verbose_name='写真',upload_to='images/',)
    good_count = models.IntegerField(default=0)
    pub_date = models.DateTimeField(default=timezone.now)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE,null=True)
    is_primary = models.BooleanField(verbose_name='表示用として使う',default=False)
    is_dispalyed = models.BooleanField(verbose_name='表示させますか？',default=False)


    def get_filename(self):
        return os.path.basename(self.file.name)


class Good(models.Model):

    created_at = models.DateTimeField(default=timezone.now)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    good_counter = models.IntegerField(default=0)
    owner = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)

    class Meta:
        db_table = 'good'
        verbose_name = verbose_name_plural = 'いいね'
