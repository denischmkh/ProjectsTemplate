import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from main_app.models import Category, Item, Specialty, Statistic

class Command(BaseCommand):
    help = 'Populates the database with 500 items and related data'

    def handle(self, *args, **options):
        fake = Faker()
        
        # Create categories first (we need at least one for the items)
        self.stdout.write('Creating categories...')
        categories = []
        category_names = [
            'Restaurants', 'Hotels', 'Shops', 'Services', 
            'Entertainment', 'Education', 'Healthcare', 'Technology',
            'Sports', 'Art & Culture'
        ]
        icons = [
            'ph-storefront', 'ph-house', 'ph-shopping-cart', 'ph-wrench',
            'ph-game-controller', 'ph-graduation-cap', 'ph-heart-straight', 'ph-desktop',
            'ph-soccer-ball', 'ph-paint-brush'
        ]
        
        for i, name in enumerate(category_names):
            slug = slugify(name)
            icon = icons[i] if i < len(icons) else 'ph-storefront'
            description = fake.paragraph()
            
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slug,
                    'description': description,
                    'icon': icon
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {name}')
            else:
                self.stdout.write(f'Category already exists: {name}')
        
        # Create specialties
        self.stdout.write('Creating specialties...')
        specialties = []
        specialty_names = [
            'Family-friendly', 'Pet-friendly', 'Eco-friendly', 'Budget', 'Luxury',
            'Open 24/7', 'Delivery', 'Takeout', 'Outdoor seating', 'Vegan options',
            'Gluten-free', 'Organic', 'Local', 'International', 'Award-winning'
        ]
        
        for name in specialty_names:
            specialty, created = Specialty.objects.get_or_create(name=name)
            specialties.append(specialty)
            if created:
                self.stdout.write(f'Created specialty: {name}')
            else:
                self.stdout.write(f'Specialty already exists: {name}')
        
        # Create 500 items
        self.stdout.write('Creating 500 items...')
        for i in range(500):
            category = random.choice(categories)
            name = fake.company()
            slug = slugify(f"{name}-{i}")  # Ensure unique slugs
            
            item = Item.objects.create(
                name=name,
                slug=slug,
                category=category,
                description=fake.paragraph(nb_sentences=5),
                subtitle=fake.catch_phrase(),
                email=fake.email(),
                phone_1=fake.phone_number(),
                phone_2=fake.phone_number() if random.random() > 0.7 else None,
                website=f"https://www.{slugify(name)}.com" if random.random() > 0.3 else None,
                facebook=f"https://facebook.com/{slugify(name)}" if random.random() > 0.5 else None,
                instagram=f"https://instagram.com/{slugify(name)}" if random.random() > 0.5 else None,
                twitter=f"https://twitter.com/{slugify(name)}" if random.random() > 0.7 else None,
                linkedin=f"https://linkedin.com/company/{slugify(name)}" if random.random() > 0.8 else None,
                youtube=f"https://youtube.com/c/{slugify(name)}" if random.random() > 0.9 else None,
                address_line1=fake.street_address(),
                address_line2=fake.secondary_address() if random.random() > 0.7 else None,
                city=fake.city(),
                state=fake.state(),
                country=fake.country(),
                postal_code=fake.postcode(),
                rating=round(random.uniform(1.0, 5.0), 1) if random.random() > 0.2 else None,
                reviews_count=random.randint(0, 1000),
                is_active=random.random() > 0.1,
                is_featured=random.random() > 0.8,
                image=f"https://picsum.photos/id/{random.randint(1, 1000)}/800/600" if random.random() > 0.3 else None,
                metadata={
                    "founded": fake.year(),
                    "employees": random.randint(1, 1000),
                    "price_range": random.choice(["$", "$$", "$$$", "$$$$"]),
                    "keywords": [fake.word() for _ in range(random.randint(1, 5))]
                } if random.random() > 0.5 else None
            )
            
            # Add random specialties to the item
            num_specialties = random.randint(0, 5)
            selected_specialties = random.sample(specialties, num_specialties)
            for specialty in selected_specialties:
                item.specialties.add(specialty)
            
            # Add random statistics to the item
            num_stats = random.randint(0, 3)
            stat_types = ['Visitors', 'Revenue', 'Growth', 'Satisfaction', 'Engagement']
            for _ in range(num_stats):
                stat_name = random.choice(stat_types)
                if stat_name == 'Visitors':
                    value = f"{random.randint(100, 10000)} per month"
                elif stat_name == 'Revenue':
                    value = f"${random.randint(10000, 1000000)}"
                elif stat_name == 'Growth':
                    value = f"{random.randint(1, 100)}%"
                elif stat_name == 'Satisfaction':
                    value = f"{random.randint(70, 100)}%"
                else:
                    value = f"{random.randint(1, 100)} points"
                
                Statistic.objects.create(
                    item=item,
                    name=stat_name,
                    value=value
                )
            
            if (i + 1) % 50 == 0:
                self.stdout.write(f'Created {i + 1} items so far...')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with 500 items!'))