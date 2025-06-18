from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.CharField(max_length=255, default='img/default.png')  # Cambiado a CharField
    stock = models.PositiveIntegerField(default=0)
    categoria = models.CharField(max_length=50, choices=[
        ('proteinas', 'Proteínas'),
        ('preentrenos', 'Pre-entrenos'),
        ('vitaminas', 'Vitaminas y Salud')
    ])
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
    
    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carrito')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Carrito de {self.usuario.username}'
    
    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())
    
    @property
    def cantidad_items(self):
        return sum(item.cantidad for item in self.items.all())

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('carrito', 'producto')
        verbose_name = 'Ítem de carrito'
        verbose_name_plural = 'Ítems de carrito'
    
    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'
    
    @property
    def subtotal(self):
        return self.cantidad * self.producto.precio
