from django.db import models
from django.contrib.auth.models import User


# -----------------------------
# Common Base Model (Optional)
# -----------------------------
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# -----------------------------
# Category Model
# -----------------------------
class Category(BaseModel):
    CATEGORY_TYPE = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPE)

    def __str__(self):
        return f"{self.name} ({self.type})"


# -----------------------------
# Income Model
# -----------------------------
class Income(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    source = models.CharField(max_length=255, blank=True, null=True)

    date = models.DateField()

    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - ₹{self.amount}"

    class Meta:
        ordering = ['-date']   # 🔥 newest first


# -----------------------------
# Expense Model
# -----------------------------
class Expense(BaseModel):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('bank', 'Bank Transfer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    date = models.DateField()
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.amount}"


# -----------------------------
# Loan / Lend Model
# -----------------------------
class Loan(BaseModel):
    LOAN_TYPE = (
        ('borrowed', 'Borrowed'),   # You took money
        ('lent', 'Lent'),           # You gave money
    )

    STATUS = (
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('completed', 'Completed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=255)
    loan_type = models.CharField(max_length=10, choices=LOAN_TYPE)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')

    note = models.TextField(blank=True, null=True)

    def balance(self):
        return self.total_amount - self.paid_amount

    def __str__(self):
        return f"{self.person_name} - {self.total_amount}"


# -----------------------------
# Todo Model
# -----------------------------
class Todo(BaseModel):
    PRIORITY = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    is_completed = models.BooleanField(default=False)

    priority = models.CharField(max_length=10, choices=PRIORITY, default='medium')

    due_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.priority})"

    class Meta:
        ordering = ['-created_at']
