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

IMAGE_MAP = {
    'tomato':      'https://images.unsplash.com/photo-1546094096-0df4bcabd337?w=400',
    'onion':       'https://images.unsplash.com/photo-1587049352851-8d4e89133924?w=400',
    'potato':      'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400',
    'carrot':      'https://images.unsplash.com/photo-1582515073490-39981397c445?w=400',
    'spinach':     'https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400',
    'cabbage':     'https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=400',
    'brinjal':     'https://images.unsplash.com/photo-1615484477778-ca3b77940c25?w=400',
    'chilli':      'https://images.unsplash.com/photo-1588252303782-cb80119abd6d?w=400',
    'cucumber':    'https://images.unsplash.com/photo-1604977042946-1eecc30f269e?w=400',
    'beans':       'https://images.unsplash.com/photo-1567375698348-5d9d5ae99de0?w=400',
    'cauliflower': 'https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?w=400',
    'ladies':      'https://images.unsplash.com/photo-1595855759920-86582396756a?w=400',
    'okra':        'https://images.unsplash.com/photo-1595855759920-86582396756a?w=400',
    'garlic':      'https://images.unsplash.com/photo-1540148426945-6cf22a6b2383?w=400',
    'ginger':      'https://images.unsplash.com/photo-1615485500704-8e990f9900f7?w=400',
    'mushroom':    'https://images.unsplash.com/photo-1552825897-bb4dc4677a34?w=400',
    'banana':      'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400',
    'apple':       'https://images.unsplash.com/photo-1570913149827-d2ac84ab3f9a?w=400',
    'mango':       'https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?w=400',
    'grape':       'https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=400',
    'orange':      'https://images.unsplash.com/photo-1547514701-42782101795e?w=400',
    'watermelon':  'https://images.unsplash.com/photo-1587049633312-d628ae50a8ae?w=400',
    'papaya':      'https://images.unsplash.com/photo-1526318472351-c75fcf070305?w=400',
    'pomegranate': 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=400',
    'guava':       'https://images.unsplash.com/photo-1536511132770-e5058c7e8c46?w=400',
    'coconut':     'https://images.unsplash.com/photo-1580984969071-a8da5656c2fb?w=400',
    'milk':        'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400',
    'curd':        'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400',
    'butter':      'https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=400',
    'cheese':      'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=400',
    'paneer':      'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=400',
    'ghee':        'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=400',
    'egg':         'https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400',
    'bread':       'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400',
    'cake':        'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400',
    'biscuit':     'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400',
    'cookie':      'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400',
    'puff':        'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400',
    'tea':         'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400',
    'coffee':      'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400',
    'juice':       'https://images.unsplash.com/photo-1534353436294-0dbd4bdac845?w=400',
    'water':       'https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400',
    'lassi':       'https://images.unsplash.com/photo-1571197119738-a86e8e2a8594?w=400',
    'rice':        'https://images.unsplash.com/photo-1536304993881-ff86e6acf7aa?w=400',
    'dal':         'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400',
    'flour':       'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400',
    'sugar':       'https://images.unsplash.com/photo-1559598467-f8b76c8155d0?w=400',
    'oil':         'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400',
    'masala':      'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400',
    'spice':       'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400',
    'chips':       'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400',
    'namkeen':     'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400',
    'biryani':     'https://images.unsplash.com/photo-1563379091339-03246963d881?w=400',
    'curry':       'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400',
    'roti':        'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400',
    'dosa':        'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400',
    'idli':        'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400',
    'samosa':      'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400',
    'chicken':     'https://images.unsplash.com/photo-1598103442097-8b74394b95c3?w=400',
    'mutton':      'https://images.unsplash.com/photo-1545247181-516773cae754?w=400',
    'fish':        'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400',
    'default':     'https://images.unsplash.com/photo-1542838132-92c53300491e?w=400',
}

def get_image_url_for_product(product_name):
    name_lower = product_name.lower()
    for keyword, url in IMAGE_MAP.items():
        if keyword in name_lower:
            return url
    return IMAGE_MAP['default']

def upload_images():
    products = Product.objects.filter(image='')
    total = products.count()
    print(f"\n📦 Found {total} products without images\n")
    success = 0
    failed = 0
    for i, product in enumerate(products, 1):
        print(f"[{i}/{total}] {product.name}...", end=' ')
        try:
            image_url = get_image_url_for_product(product.name)
            response = requests.get(image_url, timeout=10)
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
        except Exception as e:
            print(f"❌ Failed: {e}")
            failed += 1
    print(f"\n{'='*50}")
    print(f"✅ Success: {success}")
    print(f"❌ Failed:  {failed}")
    print(f"{'='*50}\n")

if __name__ == '__main__':
    upload_images()
