from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('principal/', views.principal, name='principal'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contactos, name='contactos'),
    path('servicios/', views.tienda, name='servicios'),
    path('tienda/', views.tienda, name='tienda'),
    path('promociones/', views.promociones, name='promociones'),
    path('productos/', views.productos, name='productos'),
    path('categoria/', views.categoria, name='categoria'),
    path('categorias/', views.categoria, name='categorias'),
    path('rebajas/', views.rebajas, name='rebajas'),
    
    # URLs del carrito
    path('carrito/', login_required(views.ver_carrito), name='ver_carrito'),
    path('agregar/<int:producto_id>/', login_required(views.agregar_al_carrito), name='agregar_al_carrito'),
    path('eliminar/<int:item_id>/', login_required(views.eliminar_del_carrito), name='eliminar_del_carrito'),
    path('actualizar/<int:item_id>/', login_required(views.actualizar_cantidad), name='actualizar_cantidad'),
]