from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(unique=True, max_length=15)
    style = models.CharField('Стиль', max_length=30, null=False, default="green")
    slug = models.SlugField(max_length=15, unique=True, default="", null=False)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(db_index=True, max_length=30)
    dimension = models.CharField(max_length=15)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes"
    )
    title = models.CharField(unique=True, max_length=200)
    description = models.TextField(blank=False, verbose_name='Описание рецепта')
    image = models.ImageField(upload_to='recipes/')
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipe_ingredient',
        through='IngredientRecipes',
        verbose_name='Ингредиенты в рецепте',
    )
    tag = models.ManyToManyField(
        Tag, related_name='recipe_tags',
        verbose_name='Тэги рецепта'
    )
    duration = models.PositiveSmallIntegerField()
    slug = models.SlugField(unique=True, blank=True)
    pub_date = models.DateTimeField(
        "Дата создания", auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.title


class IngredientRecipes(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'


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
        related_name='favorite',
        verbose_name='Избранные рецепты'
    )


class Basket(models.Model):
    USE_STATUS = [('True', 'True'), ('False', 'False')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(
        Recipe,
        related_name='basket',
        verbose_name='Корзина'
    )
    created = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
        db_index=True
    )
    used = models.CharField(choices=USE_STATUS, default='False', max_length=10)

    def __str__(self):
        return f"{self.user} - {self.created}"
