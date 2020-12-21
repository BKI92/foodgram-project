from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    title = models.CharField('Название', unique=True, max_length=15)
    style = models.CharField('Стиль', max_length=30, null=False,
                             default="green")
    slug = models.SlugField('Слаг', unique=True, max_length=15, default="")

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField('Название', db_index=True, max_length=30)
    dimension = models.CharField('Единицы измерения', max_length=15)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    title = models.CharField('Название', unique=True, max_length=200)
    description = models.TextField('Описание рецепта', blank=False)
    image = models.ImageField('Картинка', upload_to='recipes/')
    ingredients = models.ManyToManyField(
        'IngredientAmount',
        verbose_name='Ингридиент',
        related_name='ingredient_amount',

    )
    tags = models.ManyToManyField(
        Tag, related_name='recipe_tags', verbose_name='Тэги рецепта',
    )
    duration = models.PositiveSmallIntegerField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    pub_date = models.DateTimeField(
        'Дата создания', auto_now_add=True,
        db_index=True,
    )

    def __str__(self):
        return self.title


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.ingredient} - {self.amount}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(
        Recipe,
        related_name='favorites',
        verbose_name='Избранные рецепты'
    )


class ShopList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(
        Recipe,
        related_name='shop_list',
        verbose_name='Список покупок'
    )

    def __str__(self):
        return f"{self.user}'s - ShopList"


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        'Дата создания', auto_now_add=True,
        db_index=True,
    )
    recipes = models.ManyToManyField(
        Recipe,
        related_name='history',
        verbose_name='История покупок'
    )

    def __str__(self):
        return f"{self.user}'s - History"
