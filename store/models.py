from django.contrib.auth.models import AbstractUser
from django.db import models


# represents each user of the application
class User(AbstractUser):
    imageUrl = models.URLField(max_length=200, null=True, blank=True)
    # Show the username of the user
    def __str__(self) -> str:
        return f"{self.username}"

# represents each course category
class Category(models.Model):
    name = models.CharField(max_length=255)
    imageUrl = models.URLField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    # Show the name of the category
    def __str__(self) -> str:
        return f"{self.name}"
    
# represents each instructor
class Instructor(models.Model):
    name = models.CharField(max_length=255)
    imageUrl = models.URLField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="instructor")
    # Show the name of the instructor
    def __str__(self) -> str:
        return f"{self.name}"

# represents each course
class Course(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    student = models.ManyToManyField(User, blank=True, related_name='courses')
    imageUrl = models.URLField(max_length=200, null=True, blank=True)
    objectives = models.TextField(blank=True, null=True)
    participant = models.TextField(blank=True, null=True)
    requirement = models.TextField(blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)

    # Show the category and the name of the course
    def __str__(self) -> str:
        return f"{self.category.name} {self.name}"

# represents each client's occupation area
class Area(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name

# represents each client (brand)
class Client(models.Model):
    name = models.CharField(max_length=255)
    imageUrl = models.URLField(max_length=200, null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True, related_name='brands')
    # Show the name of the brand
    def __str__(self) -> str:
        return self.name

# represents each comment about the course
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    # Show the name of the user and comment
    def __str__(self) -> str:
        return f"Comment from: {self.user.username} Comment: {self.comment}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="cartItem")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.course.name} (Quantidade: {self.quantity})"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    courses = models.ManyToManyField(Course, related_name="purchased_courses")
    timestamp = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    is_paid = models.BooleanField(default=False)

    def add_courses_from_cart(self, cart_items):
        for item in cart_items:
            self.courses.add(item.course)
        self.total_price = sum(item.course.price for item in cart_items)
        self.is_paid = True
        self.save()

    def __str__(self) -> str:
        return f"Compra #{self.id} por {self.user.username}"