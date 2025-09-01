from django.core.management.base import BaseCommand
from products.models import Category, Product


class Command(BaseCommand):
    help = "Seed default categories and products (safe & idempotent)"

    def handle(self, *args, **kwargs):
        # Step 1: Categories
        categories = [
            ('Cakes', 'cakes'),
            ('Burgers', 'burgers'),
            ('Sandwich', 'sandwich'),
            ('Sweets', 'sweets'),
            ('Fryed and Fries', 'fryed-and-fries'),
            ('Loaded Fries', 'loaded-fries'),
            ('Juices', 'juices'),
            ('Shakes', 'shakes'),
            ('Pasta', 'pasta'),
            ('Dumplings', 'dumplings'),
            ('Ice Creams', 'ice-creams'),
            ('Chips', 'chips'),
            ('Bakes', 'bakes'),
            ('Moctails', 'moctails'),
            ('Falooda', 'falooda'),
            ('Shawarma', 'shawarma'),
            ('Brosted', 'brosted'),
            ('Cool Drinks', 'cool-drinks'),
            ('Hot Beverages', 'hot-beverages'),
            ('Mojitos', 'mojitos'),
            ('Avil Milks', 'avil-milks'),
            ('Fruit Salads', 'fruit-salads'),
        ]

        cat_map = {}
        for i, (name, slug) in enumerate(categories):
            try:
                # 1️⃣ Try to get by slug
                category = Category.objects.get(slug=slug)
                category.name = name
                category.order = i
                category.save()
            except Category.DoesNotExist:
                # 2️⃣ If slug not found, check by name
                existing = Category.objects.filter(name=name).first()
                if existing:
                    existing.slug = slug
                    existing.order = i
                    existing.save()
                    category = existing
                else:
                    # 3️⃣ If neither exists, create new
                    category = Category.objects.create(
                        name=name,
                        slug=slug,
                        order=i
                    )
            cat_map[slug] = category

        self.stdout.write(self.style.SUCCESS("✅ Categories seeded."))

        # Step 2: Products (optional demo data)
        products = {
            "cakes": [
                # ("Chocolate Cake", "Rich chocolate delight", 250.0),
                # ("Vanilla Cake", "Classic vanilla sponge", 200.0),
            ],
            "burgers": [],
            "sandwich": [],
            "sweets": [],
            "fryed-and-fries": [],
            "loaded-fries": [],
            "juices": [],
            "shakes": [],
            "pasta": [],
            "dumplings": [],
            "ice-creams": [],
            "chips": [],
            "bakes": [],
            "moctails": [],
            "falooda": [],
            "shawarma": [],
            "brosted": [],
            "cool-drinks": [],
            "hot-beverages": [],
            "mojitos": [],
            "avil-milks": [],
            "fruit-salads": [],
        }

        for slug, items in products.items():
            category = cat_map.get(slug)
            if not category:
                self.stdout.write(self.style.WARNING(f"⚠️ Category {slug} missing, skipping..."))
                continue

            for name, desc, price in items:
                product, created = Product.objects.get_or_create(
                    category=category,
                    name=name,
                    defaults={
                        "description": desc,
                        "price": price,
                        "is_active": True,
                    }
                )
                if not created:
                    product.description = desc
                    product.price = price
                    product.is_active = True
                    product.save()

        self.stdout.write(self.style.SUCCESS("✅ Products seeded successfully!"))
