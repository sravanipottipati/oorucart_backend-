import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oorucart_backend.settings')
django.setup()

from vendors.models import Vendor, Product, ProductVariant
from decimal import Decimal

def add(vendor, name, category, price, desc, variants):
    p, created = Product.objects.get_or_create(
        vendor=vendor, name=name,
        defaults={'category': category, 'price': Decimal(str(price)), 'description': desc, 'is_available': True}
    )
    if not created:
        p.category = category
        p.price = Decimal(str(price))
        p.save()
    for vname, vprice in variants:
        ProductVariant.objects.get_or_create(
            product=p, name=vname,
            defaults={'price': Decimal(str(vprice)), 'stock_quantity': 50, 'is_available': True}
        )
    print(f'  ✅ {name}')

# Sri Lakshmi Supermarket
v = Vendor.objects.get(shop_name='Sri Lakshmi Supermarket')
print('Sri Lakshmi Supermarket')
add(v,'Sona Masoori Rice','staples',65,'Premium quality rice',[('1kg',65),('5kg',310),('10kg',600)])
add(v,'Wheat Flour','staples',45,'Fresh chakki atta',[('1kg',45),('5kg',210),('10kg',400)])
add(v,'Poha','staples',30,'Thick poha',[('500g',30),('1kg',58)])
add(v,'Toor Dal','dal_pulses',90,'Premium toor dal',[('500g',90),('1kg',175),('2kg',340)])
add(v,'Chana Dal','dal_pulses',75,'Fresh chana dal',[('500g',75),('1kg',145)])
add(v,'Moong Dal','dal_pulses',85,'Yellow moong dal',[('500g',85),('1kg',165)])
add(v,'Urad Dal','dal_pulses',80,'Black urad dal',[('500g',80),('1kg',155)])
add(v,'Sunflower Oil','oils',105,'Refined sunflower oil',[('500ml',58),('1L',105),('2L',200),('5L',490)])
add(v,'Groundnut Oil','oils',180,'Cold pressed',[('500ml',95),('1L',180),('2L',350)])
add(v,'Coconut Oil','oils',130,'Pure coconut oil',[('200ml',65),('500ml',130),('1L',255)])
add(v,'Sugar','sugar_salt',45,'Fine white sugar',[('500g',24),('1kg',45),('5kg',215)])
add(v,'Salt','sugar_salt',20,'Iodized table salt',[('500g',12),('1kg',20)])
add(v,'Jaggery','sugar_salt',60,'Natural cane jaggery',[('500g',32),('1kg',60)])
add(v,'Turmeric Powder','spices',35,'Pure turmeric',[('100g',35),('200g',65),('500g',150)])
add(v,'Red Chilli Powder','spices',45,'Spicy red chilli',[('100g',45),('200g',85),('500g',200)])
add(v,'Coriander Powder','spices',35,'Fresh coriander',[('100g',35),('200g',65)])
add(v,'Cumin Seeds','spices',55,'Whole cumin seeds',[('100g',55),('200g',105)])
add(v,'Garam Masala','spices',60,'Aromatic blend',[('50g',35),('100g',60),('200g',115)])
add(v,'Parle G','snacks',10,'Classic biscuits',[('100g',10),('400g',35)])
add(v,'Haldirams Mixture','snacks',30,'Crispy namkeen',[('150g',30),('400g',75)])
add(v,'Tata Tea','beverages',85,'Premium tea',[('250g',85),('500g',165),('1kg',320)])
add(v,'Bru Coffee','beverages',95,'Instant coffee',[('50g',45),('100g',85),('200g',165)])
add(v,'Horlicks','beverages',199,'Health drink',[('200g',115),('500g',199),('1kg',375)])

# Fresh Dairy Centre
v = Vendor.objects.get(shop_name='Fresh Dairy Centre')
print('Fresh Dairy Centre')
add(v,'Full Cream Milk','milk',28,'Fresh milk',[('500ml',15),('1L',28),('2L',54)])
add(v,'Toned Milk','milk',24,'Low fat milk',[('500ml',13),('1L',24)])
add(v,'Curd','curd',35,'Fresh homemade curd',[('200g',20),('400g',35),('1kg',80)])
add(v,'Greek Yogurt','curd',55,'Thick creamy yogurt',[('100g',30),('200g',55)])
add(v,'Butter','butter',55,'Fresh white butter',[('100g',55),('200g',105),('500g',250)])
add(v,'Amul Butter','butter',60,'Salted Amul butter',[('100g',60),('500g',280)])
add(v,'Paneer','paneer',80,'Fresh soft paneer',[('200g',80),('500g',185),('1kg',360)])
add(v,'Ghee','ghee',180,'Pure cow ghee',[('250ml',95),('500ml',180),('1L',350)])
add(v,'Cheese Slices','butter',120,'Processed cheese',[('200g',75),('400g',120)])
add(v,'Lassi','curd',30,'Sweet chilled lassi',[('200ml',20),('500ml',45)])
add(v,'Eggs','eggs',90,'Farm fresh eggs',[('6 pcs',50),('12 pcs',90),('30 pcs',210)])

# Nellore Grocery Store
v = Vendor.objects.get(shop_name='Nellore Grocery Store')
print('Nellore Grocery Store')
add(v,'Maida','flour',40,'All purpose flour',[('500g',22),('1kg',40),('5kg',190)])
add(v,'Sooji','flour',30,'Fine semolina',[('500g',30),('1kg',58)])
add(v,'Tamarind','spices',40,'Seedless tamarind',[('100g',20),('250g',45),('500g',80)])
add(v,'Dry Red Chilli','spices',50,'Whole dry chillies',[('100g',30),('250g',70)])
add(v,'Tomato Ketchup','packaged',85,'Maggi ketchup',[('200g',45),('500g',85),('1kg',155)])
add(v,'Pickle','packaged',55,'Andhra mango pickle',[('200g',35),('500g',75)])
add(v,'Lays Chips','snacks',20,'Crispy chips',[('26g',10),('52g',20),('100g',35)])
add(v,'Kurkure','snacks',20,'Masala snack',[('40g',10),('90g',20)])
add(v,'Good Day Biscuits','snacks',30,'Butter biscuits',[('100g',15),('200g',30)])
add(v,'Surf Excel','cleaning',45,'Washing powder',[('200g',25),('500g',55),('1kg',105)])
add(v,'Vim Dish Wash','cleaning',35,'Dish wash bar',[('200g',20),('500g',45)])
add(v,'Phenyl','cleaning',55,'Floor cleaner',[('500ml',35),('1L',55),('2L',100)])
add(v,'Clinic Plus Shampoo','personal_care',85,'Nourishing shampoo',[('80ml',45),('175ml',85),('340ml',155)])
add(v,'Colgate Toothpaste','personal_care',65,'Strong teeth',[('50g',35),('100g',55),('200g',100)])
add(v,'Lifebuoy Soap','personal_care',35,'Germ protection',[('100g',20),('4 pack',75)])

# Cool Drinks & Snacks
v = Vendor.objects.get(shop_name='Cool Drinks & Snacks')
print('Cool Drinks & Snacks')
add(v,'Pepsi','soft_drinks',40,'Chilled Pepsi',[('250ml',20),('600ml',40),('2L',90)])
add(v,'Coca Cola','soft_drinks',40,'Classic Cola',[('250ml',20),('600ml',40),('2L',90)])
add(v,'7UP','soft_drinks',40,'Lemon drink',[('250ml',20),('600ml',40)])
add(v,'Mirinda','soft_drinks',40,'Orange drink',[('250ml',20),('600ml',40)])
add(v,'Frooti','juices',20,'Mango drink',[('200ml',20),('500ml',40),('1L',75)])
add(v,'Real Juice','juices',65,'Mixed fruit juice',[('200ml',35),('1L',99)])
add(v,'Tropicana','juices',85,'Orange juice',[('200ml',45),('1L',110)])
add(v,'Mineral Water','water',20,'Pure drinking water',[('500ml',10),('1L',20),('2L',35)])
add(v,'Red Bull','soft_drinks',115,'Energy drink',[('250ml',115)])
add(v,'Lays Classic','chips',20,'Classic salted chips',[('26g',10),('52g',20),('104g',35)])
add(v,'Lays Masala','chips',20,'Masala chips',[('26g',10),('52g',20)])
add(v,'Kurkure Masala','chips',20,'Spicy masala',[('40g',10),('90g',20)])
add(v,'Haldirams Bhujia','namkeen',35,'Crispy bhujia',[('150g',35),('400g',80)])
add(v,'Haldirams Mixture','namkeen',30,'Crispy mixture',[('150g',30),('400g',75)])
add(v,'Dairy Milk','chocolates',40,'Cadbury chocolate',[('36g',20),('72g',40),('160g',85)])
add(v,'KitKat','chocolates',30,'Wafer chocolate',[('37g',20),('73g',40)])
add(v,'Bourbon Biscuits','snacks',25,'Chocolate biscuits',[('100g',15),('200g',28)])

print('ALL DONE!')
