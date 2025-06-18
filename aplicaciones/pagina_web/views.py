from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto
from django.http import JsonResponse, HttpResponse
import json

def get_carrito(request):
    # Obtener el carrito de la sesión o crearlo si no existe
    carrito = request.session.get('carrito', {})
    return carrito

def principal(request):
    return render(request, 'principal.html')

def inicio(request):
    return render(request, 'inicio.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def contactos(request):
    return render(request, 'contactos.html')

def tienda(request):
    # Crear algunos productos de ejemplo si no existen
    if not Producto.objects.exists():
        productos_ejemplo = [
            {
                'nombre': 'Proteína Whey Gold',
                'descripcion': 'Suplemento premium para desarrollo muscular y rápida recuperación post-entreno.',
                'precio': 29.99,
                'categoria': 'proteinas',
                'imagen': 'img/1.png'
            },
            {
                'nombre': 'Proteína Isolate',
                'descripcion': 'Alta pureza con bajo contenido en carbohidratos y grasas. Ideal para definición.',
                'precio': 34.99,
                'categoria': 'proteinas',
                'imagen': 'img/1.png'
            },
            {
                'nombre': 'Proteína Vegana',
                'descripcion': 'Fuente completa de proteína de origen vegetal. Sin lácteos ni soja.',
                'precio': 31.99,
                'categoria': 'proteinas',
                'imagen': 'img/1.png'
            },
            {
                'nombre': 'Pre-entreno Xtreme',
                'descripcion': 'Máxima energía, enfoque y resistencia para entrenamientos intensos.',
                'precio': 24.99,
                'categoria': 'preentrenos',
                'imagen': 'img/2.png'
            },
            {
                'nombre': 'Pre-entreno Pump',
                'descripcion': 'Mejora el flujo sanguíneo y la congestión muscular durante el entrenamiento.',
                'precio': 19.99,
                'categoria': 'preentrenos',
                'imagen': 'img/2.png'
            },
            {
                'nombre': 'Pre-entreno Energía Natural',
                'descripcion': 'Energía sostenible sin cafeína. Ideal para entrenamientos nocturnos.',
                'precio': 21.99,
                'categoria': 'preentrenos',
                'imagen': 'img/2.png'
            },
            {
                'nombre': 'Multivitamínico Completo',
                'descripcion': 'Todo lo que tu cuerpo necesita en un solo comprimido. 60 cápsulas.',
                'precio': 14.99,
                'categoria': 'vitaminas',
                'imagen': 'img/3.png'
            },
            {
                'nombre': 'Vitamina D3 + K2',
                'descripcion': 'Fórmula potenciada para la salud ósea y el sistema inmunológico.',
                'precio': 17.99,
                'categoria': 'vitaminas',
                'imagen': 'img/3.png'
            },
            {
                'nombre': 'Omega 3 Ultra',
                'descripcion': 'Ácidos grasos esenciales de alta concentración. 120 cápsulas blandas.',
                'precio': 22.99,
                'categoria': 'vitaminas',
                'imagen': 'img/3.png'
            },
        ]
        
        for producto_data in productos_ejemplo:
            Producto.objects.create(
                nombre=producto_data['nombre'],
                descripcion=producto_data['descripcion'],
                precio=producto_data['precio'],
                categoria=producto_data['categoria'],
                imagen=producto_data['imagen'],
                stock=100
            )
    
    # Obtener productos por categoría
    proteinas = Producto.objects.filter(categoria='proteinas')
    preentrenos = Producto.objects.filter(categoria='preentrenos')
    vitaminas = Producto.objects.filter(categoria='vitaminas')
    
    return render(request, 'tienda.html', {
        'proteinas': proteinas,
        'preentrenos': preentrenos,
        'vitaminas': vitaminas
    })

def productos(request):
    return render(request, 'productos.html')

def categoria(request):
    return render(request, 'categorias.html')

def rebajas(request):
    return render(request, 'rebajas.html')

def promociones(request):
    return render(request, 'promociones.html')

def ver_carrito(request):
    # Vista simple que solo muestra la plantilla
    # El carrito se manejará completamente con JavaScript
    return render(request, 'carrito.html')

def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        carrito = request.session.get('carrito', {})
        
        # Convertir el ID a cadena para usarlo como clave en el diccionario
        producto_id = str(producto_id)
        
        # Verificar si el producto ya está en el carrito
        if producto_id in carrito:
            # Incrementar la cantidad si hay suficiente stock
            if carrito[producto_id]['cantidad'] < producto.stock:
                carrito[producto_id]['cantidad'] += 1
                messages.success(request, f'¡{producto.nombre} añadido al carrito!')
            else:
                messages.warning(request, f'No hay suficiente stock de {producto.nombre}.')
        else:
            # Agregar nuevo producto al carrito
            carrito[producto_id] = {
                'nombre': producto.nombre,
                'precio': float(producto.precio),  # Convertir a float para serialización JSON
                'cantidad': 1,
                'imagen': producto.imagen,
                'categoria': producto.categoria
            }
            messages.success(request, f'¡{producto.nombre} añadido al carrito!')
        
        # Guardar el carrito en la sesión
        request.session['carrito'] = carrito
        
        # Redirigir a la misma página de la que vino la petición
        return redirect(request.META.get('HTTP_REFERER', 'tienda'))
    
    return redirect('tienda')

def eliminar_del_carrito(request, producto_id):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        producto_id = str(producto_id)
        
        if producto_id in carrito:
            producto_nombre = carrito[producto_id]['nombre']
            del carrito[producto_id]
            request.session['carrito'] = carrito
            messages.success(request, f'¡{producto_nombre} eliminado del carrito!')
    
    return redirect('ver_carrito')

def actualizar_cantidad(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        carrito = request.session.get('carrito', {})
        producto_id = str(producto_id)
        
        if producto_id in carrito:
            accion = request.POST.get('accion')
            
            if accion == 'aumentar':
                if carrito[producto_id]['cantidad'] < producto.stock:
                    carrito[producto_id]['cantidad'] += 1
            elif accion == 'disminuir' and carrito[producto_id]['cantidad'] > 1:
                carrito[producto_id]['cantidad'] -= 1
            
            # Guardar el carrito actualizado en la sesión
            request.session['carrito'] = carrito
            
            # Calcular subtotal y total
            subtotal = carrito[producto_id]['cantidad'] * carrito[producto_id]['precio']
            total = sum(item['cantidad'] * item['precio'] for item in carrito.values())
            
            return JsonResponse({
                'success': True,
                'cantidad': carrito[producto_id]['cantidad'],
                'subtotal': f"{subtotal:.2f}",
                'total': f"{total:.2f}"
            })
    
    return JsonResponse({'success': False, 'error': 'Error al actualizar la cantidad'}, status=400)
