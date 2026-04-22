import os, sys, django, requests
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'univerin_backend.settings')
sys.path.insert(0, '/Users/sravanipottipati/projects/univerin_backend')
django.setup()

import cloudinary.uploader
from vendors.models import Vendor

FIXES = {
    'Tomatoes':      'https://images.unsplash.com/photo-1607305387299-a3d9611cd469?w=400',
    'Onions':        'https://images.unsplash.com/photo-1587049352851-8d4e89133924?w=400',
    'Potatoes':      'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400',
    'Carrots':       'https://images.unsplash.com/photo-1582515073490-39981397c445?w=400',
    'Spinach':       'https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400',
    'Cucumber':      'https://images.unsplash.com/photo-1604977042946-1eecc30f269e?w=400',
    'Fresh Tomatoes':'https://images.unsplash.com/photo-1607305387299-a3d9611cd469?w=400',
}

DEFAULT = 'https://images.unsplash.com/photo-1542838132-92c53300491e?w=400'

v = Vendor.objects.filter(shop_name__icontains='ravi').first()
print(f'Fixing: {v.shop_name}\n')

for p in v.products.all():
    if p.image and p.image.public_id:
        print(f'  {p.name} | already has image ✅')
        continue
    url = FIXES.get(p.name, DEFAULT)
    print(f'  {p.name}...', end=' ')
    try:
        response = requests.get(url, timeout=10)
        result = cloudinary.uploader.upload(
            BytesIO(response.content),
            folder='shop2me/products',
            public_id=f"product_{str(p.id)[:8]}",
            overwrite=True,
            resource_type='image'
        )
        p.image = result['public_id']
        p.save()
        print('✅')
    except Exception as e:
        print(f'❌ {e}')

print('\nAll done!')
