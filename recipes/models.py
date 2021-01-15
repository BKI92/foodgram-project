from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    RED = 'red'
    BLUE = 'blue'
    BLACK = 'black'
    ORANGE = 'orange'
    GREEN = 'green'
    YELLOW = 'yellow'
    CYAN = 'cyan'
    PURPLE = 'purple'
    VIOLET = 'violet'
    COLORS = (
        (RED, 'red'),
        (BLUE, 'blue'),
        (BLACK, 'black'),
        (ORANGE, 'orange'),
        (GREEN, 'green'),
        (YELLOW, 'yellow'),
        (CYAN, 'cyan'),
        (PURPLE, 'purple'),
        (VIOLET, 'violet'),
    )
    title = models.CharField('Название', unique=True, max_length=15)
    style = models.CharField('Стиль', max_length=30, null=False, default='green', choices=COLORS)
    slug = models.SlugField('Слаг', unique=True, max_length=15)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Ingredient(models.Model):
    title = models.CharField('Название', db_index=True, max_length=30)
    dimension = models.CharField('Единицы измерения', max_length=15)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


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

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.ingredient} - {self.amount}'

    class Meta:
        verbose_name = 'Ингредиент с количеством'
        verbose_name_plural = 'Ингредиенты с количеством'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'], name='unique follow')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(
        Recipe,
        related_name='favorites',
        verbose_name='Избранные рецепты'
    )

    def __str__(self):
        return f"{self.user}'s  recipes"

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class ShopList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(
        Recipe,
        related_name='shop_list',
        verbose_name='Список покупок'
    )

    def __str__(self):
        return f"{self.user}'s - ShopList"

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'


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

    class Meta:
        verbose_name = 'История покупок'
        verbose_name_plural = 'Истории покупок'
