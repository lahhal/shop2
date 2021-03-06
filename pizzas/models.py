from django.db import models

class Pizza(models.Model):
    name = models.CharField(max_length=30)
    toppings = models.ManyToManyField('Topping', through='ToppingAmount', related_name='pizzas')  # 맞춤형 경유 모델 지정

    def __str__(self):
        return self.name


class Topping(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ToppingAmount(models.Model):
    REGULAR = 1; DOUBLE = 2; TRIPLE = 3
    AMOUNT_CHOICES = (
        (REGULAR, 'Regular'), (DOUBLE, 'Double'), (TRIPLE, 'Triple'),
    )
    pizza = models.ForeignKey('Pizza', related_name='topping_amounts',
        on_delete=models.SET_NULL, null=True)
    topping = models.ForeignKey('Topping', related_name='topping_amounts',
        on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.IntegerField(choices=AMOUNT_CHOICES, default=REGULAR)

    def __str__(self):
        return '{} 토핑을 {} 배 올린 {} 피자'.format(self.topping, self.amount, self.pizza)
