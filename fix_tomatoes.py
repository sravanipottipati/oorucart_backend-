import os
import sys
import django
import requests
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oorucart_backend.settings')
sys.path.insert(0, '/Users/sravanipottipati/projects/oorucart_backend')
django.setup()

import cloudinary.uploader
from vendors.models import Product

url = 'https://images.unsplash.com/photo-1607305387299-a3d9611cd469?w=400'

products = Product.objects.filter(name='Fresh Tomatoes', image='')
print(f"Found {products.count()} Fresh Tomatoes without image")

for product in products:
    try:
        response = requests.get(url, timeout=10)
        result = cloudinary.uploader.upload(
            BytesIO(response.content),
            folder='shop2me/products',
            public_id=f"product_{str(product.id)[:8]}",
            overwrite=True,
            resource_type='image'
        )
        product.image = result['public_id']
        product.save()
        print(f"✅ {product.vendor.shop_name} - uploaded")
    except Exception as e:
        print(f"❌ Failed: {e}")
