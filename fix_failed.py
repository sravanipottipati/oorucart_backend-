import os
import sys
import django
import requests
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'univerin_backend.settings')
sys.path.insert(0, '/Users/sravanipottipati/projects/univerin_backend')
django.setup()

import cloudinary.uploader
from vendors.models import Product

# Fixed URLs for the 4 failed products
FIXES = {
    'Rice 1kg':       'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400',
    'Biryani':        'https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=400',
    'Fried Rice':     'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400',
    'Fresh Tomatoes': 'https://images.unsplash.com/photo-1607305387299-a3d9611cd469?w=400',
}

def fix_failed():
    print("\n🔧 Fixing 4 failed products...\n")
    success = 0
    for name, url in FIXES.items():
        print(f"  {name}...", end=' ')
        try:
            product = Product.objects.get(name=name)
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            result = cloudinary.uploader.upload(
                BytesIO(response.content),
                folder='shop2me/products',
                public_id=f"product_{str(product.id)[:8]}",
                overwrite=True,
                resource_type='image'
            )
            product.image = result['public_id']
            product.save()
            print(f"✅ uploaded")
            success += 1
        except Product.DoesNotExist:
            print(f"⚠️  Product not found in DB")
        except Exception as e:
            print(f"❌ Failed: {e}")
    print(f"\n✅ Fixed {success}/4 products\n")

if __name__ == '__main__':
    fix_failed()
