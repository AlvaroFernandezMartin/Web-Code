import os
from django.core.files import File
from products.models import Category, Product

# Ruta base donde están almacenadas las imágenes en subcarpetas por categoría
BASE_DIR = "/Users/user/Documents/Web Code/ralawise_images_selenium"

def load_products_from_images():
    for category_name in os.listdir(BASE_DIR):
        category_path = os.path.join(BASE_DIR, category_name)

        if not os.path.isdir(category_path):
            continue  # saltar archivos sueltos

        # Crear o conseguir la categoría
        category, created = Category.objects.get_or_create(name=category_name.replace("_", " "))

        # Recorrer todas las imágenes .webp en esa carpeta
        for filename in os.listdir(category_path):
            if not filename.lower().endswith('.webp'):
                continue

            image_path = os.path.join(category_path, filename)

            # Crear producto
            with open(image_path, 'rb') as img_file:
                product = Product(
                    name=os.path.splitext(filename)[0],  # nombre sin extensión
                    category=category
                )
                product.image.save(filename, File(img_file), save=True)

            print(f"✔ Producto creado: {product.name} en categoría {category.name}")

# Ejecutar esta función en un shell de Django:
# python manage.py shell
# >>> from script_path import load_products_from_images
# >>> load_products_from_images()
