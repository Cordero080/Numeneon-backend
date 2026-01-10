#!/usr/bin/env python
import os
import django
import random
from datetime import datetime, timedelta  # NEW: For date manipulation

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'numeneon.settings')
django.setup()

from django.contrib.auth.models import User
from posts.models import Post

# Clear existing posts for fresh seed data
print('Clearing existing posts...')
Post.objects.all().delete()  # NEW: Removes ALL posts from database

# Create friend users if they don't exist
friend_users = [
    {'username': 'pabloPistola', 'email': 'pablo@test.com', 'first_name': 'Pablo', 'last_name': 'Cordero'},
    {'username': 'titod', 'email': 'tito@test.com', 'first_name': 'Tito', 'last_name': 'Del Valle'},
    {'username': 'arthurb', 'email': 'arthur@test.com', 'first_name': 'Arthur', 'last_name': 'Brown'},
    {'username': 'nataliap', 'email': 'natalia@test.com', 'first_name': 'Natalia', 'last_name': 'Perez'},
    {'username': 'colinw', 'email': 'colin@test.com', 'first_name': 'Colin', 'last_name': 'Wang'},
    {'username': 'crystalr', 'email': 'crystal@test.com', 'first_name': 'Crystal', 'last_name': 'Rivera'},
]

print('Creating friend users...')
for u in friend_users:
    user, created = User.objects.get_or_create(
        username=u['username'],
        defaults={
            'email': u['email'],
            'first_name': u['first_name'],
            'last_name': u['last_name'],
        }
    )
    if created:
        user.set_password('test123')
        user.save()
        print(f'  Created user: {u["username"]}')
    else:
        print(f'  User exists: {u["username"]}')

# Get users
users = {u.username: u for u in User.objects.all()}
print('Users:', list(users.keys()))

# ============================================================================
# MOCK POSTS DATA - EXPANDED FOR ANALYTICS
# ============================================================================
# Each user has 20+ posts for dense heatmap coverage
# Posts spread across 365 days with clusters for wave peaks
# BOOSTED engagement for maximum heatmap visibility!
# This creates visible waves and brightly lit heatmaps!
# ============================================================================

# Helper functions for engagement - MASSIVELY BOOSTED for visible heatmap
def high_engagement():
    """High activity posts - creates bright wave peaks"""
    return {
        'likes': random.randint(800, 1500),
        'comments': random.randint(150, 300),
        'shares': random.randint(100, 200),
    }

def medium_engagement():
    """Medium activity - still quite visible"""
    return {
        'likes': random.randint(400, 800),
        'comments': random.randint(80, 150),
        'shares': random.randint(50, 100),
    }

def low_engagement():
    """Lower activity - but still lights up heatmap"""
    return {
        'likes': random.randint(200, 400),
        'comments': random.randint(40, 80),
        'shares': random.randint(25, 50),
    }

def random_engagement():
    """Mix of engagement levels - more high engagement for visibility"""
    choice = random.random()
    if choice < 0.40:  # 40% high
        return high_engagement()
    elif choice < 0.75:  # 35% medium
        return medium_engagement()
    else:  # 25% low
        return low_engagement()

# Reusable media URLs - Tech, Martial Arts, Physics, Natural Phenomena
MEDIA_URLS = {
    # ═══════════════════════════════════════════════════════════════════
    # AURORA / NORTHERN LIGHTS 
    # ═══════════════════════════════════════════════════════════════════
    'aurora_reflection': 'https://images.unsplash.com/photo-1483347756197-71ef80e95f73?w=1200',  # Mirror lake reflection, Iceland
    'aurora_pink': 'https://images.unsplash.com/photo-1579033461380-adb47c3eb938?w=1200',        # Rare pink/magenta aurora
    'aurora_cabin': 'https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=1200',       # Lonely cabin under green curtains
    'aurora_mountain': 'https://images.unsplash.com/photo-1494243762909-b498c7e440a9?w=1200',    # Aurora over jagged peaks
    'aurora_spiral': 'https://images.unsplash.com/photo-1507400492013-162706c8c05e?w=1200',      # Spiral corona overhead
    'aurora_red': 'https://images.unsplash.com/photo-1488866022504-f2584929ca5f?w=1200',         # Rare blood-red aurora
    
    # ═══════════════════════════════════════════════════════════════════
    # COSMIC / CELESTIAL - The Sublime
    # ═══════════════════════════════════════════════════════════════════
    'nebula_pillars': 'https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1200',     # Pillars of Creation vibes
    'milky_way_arch': 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1200',     # Perfect arch over mountains
    'eclipse_corona': 'https://images.unsplash.com/photo-1503416997304-7f8bf166c121?w=1200',     # Solar corona detail
    'supermoon': 'https://images.unsplash.com/photo-1532693322450-2cb5c511067d?w=1200',          # Massive moon on horizon
    'comet_trail': 'https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?w=1200',        # Long exposure comet
    
    # ═══════════════════════════════════════════════════════════════════
    # CYBERPUNK / NEON - Aesthetic
    # ═══════════════════════════════════════════════════════════════════
    'tokyo_rain': 'https://images.unsplash.com/photo-1542051841857-5f90071e7989?w=1200',         # Rainy Tokyo alley, Blade Runner mood
    'neon_alley': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200',            # Hong Kong neon canyon
    'osaka_nights': 'https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?w=1200',       # Dotonbori sensory overload
    'seoul_glow': 'https://images.unsplash.com/photo-1517154421773-0529f29ea451?w=1200',         # Korean neon reflections
    'shanghai_fog': 'https://images.unsplash.com/photo-1474181487882-5abf3f0ba6c2?w=1200',       # Pudong through mist
    'akihabara': 'https://images.unsplash.com/photo-1513407030348-c983a97b98d8?w=1200',          # Electric Town sensory assault
    
    # ═══════════════════════════════════════════════════════════════════
    # TECH / PHYSICS - The Beautiful Machine
    # ═══════════════════════════════════════════════════════════════════
    'lhc_tunnel': 'https://cds.cern.ch/images/CERN-PHOTO-201802-030-3/file?size=large',          # CERN particle accelerator
    'server_cathedral': 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200',      # Data center infinity
    'fiber_optic': 'https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=1200',           # Light through glass
    'motherboard_macro': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200',  # Circuit city landscape
    'tesla_coil': 'https://images.unsplash.com/photo-1517420704952-d9f39e95b43e?w=1200',         # Controlled lightning
    'laser_lab': 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=1200',          # Quantum optics setup
    
    # ═══════════════════════════════════════════════════════════════════
    # NATURAL POWER - Earth's Violence Made Beautiful
    # ═══════════════════════════════════════════════════════════════════
    'lightning_strike': 'https://images.unsplash.com/photo-1461511540115-9d4129be6767?w=1200',   # Pure electricity
    'volcano_lava': 'https://images.unsplash.com/photo-1562889676-9eb5b643e71e?w=1200',          # Molten earth
    'storm_cell': 'https://images.unsplash.com/photo-1527482937786-6f498d7e86c9?w=1200',         # Supercell structure
    'bioluminescence': 'https://images.unsplash.com/photo-1507400492013-162706c8c05e?w=1200',    # Glowing waves
    
    # ═══════════════════════════════════════════════════════════════════
    # MARTIAL ARTS / DISCIPLINE - Form as Art
    # ═══════════════════════════════════════════════════════════════════
    'dojo_light': 'https://www.shaolin.org.gr/images/uploads/the_changing_landscape_of_kung_fu_in_modern_china.jpg',  # Outdoor dojo training
    'meditation_mist': 'https://images.stockcake.com/public/4/7/f/47f1eda0-8c36-44c2-a6ea-026399df7342_large/cyberpunk-samurai-zen-stockcake.jpg',
    'wudang_mountains': 'https://images.unsplash.com/photo-1513415756790-2ac1db1297d0?w=1200',   # Misty Chinese peaks
    'bamboo_forest': 'https://images.unsplash.com/photo-1448375240586-882707db888b?w=1200',      # Infinite green
}


mock_posts = [
    # ========== pabloPistola (24 posts - dense activity) ==========
    # Recent cluster (creates wave peak)
    {'author': 'pabloPistola', 'content':'Kata: choreographed violence against nobody. Weirdly grounding.', 'type': 'thoughts', 'days_ago': 1, **high_engagement()},
    {'author': 'pabloPistola', 'content': 'Aurora over Iceland. Solar wind hitting magnetosphere.', 'type': 'media', 'days_ago': 2, 'media_url': MEDIA_URLS['aurora_reflection'], **high_engagement()},
    {'author': 'pabloPistola', 'content': 'NUMENEON v1.0 shipped. We don\'t talk about week two.', 'type': 'milestones', 'days_ago': 3, **high_engagement()},
    {'author': 'pabloPistola', 'content': '2am code works better. Hypothesis confirmed.', 'type': 'thoughts', 'days_ago': 5, **medium_engagement()},
    {'author': 'pabloPistola', 'content': 'Tokyo rain. Neon bleeds into puddles.', 'type': 'media', 'days_ago': 8, 'media_url': MEDIA_URLS['tokyo_rain'], **medium_engagement()},
    # Week 2-3 activity
    {'author': 'pabloPistola', 'content': 'The work exists before the work.', 'type': 'thoughts', 'days_ago': 12, **medium_engagement()},
    {'author': 'pabloPistola', 'content': 'Outdoor dojo. Musashi trained in the woods.', 'type': 'media', 'days_ago': 15, 'media_url': MEDIA_URLS['dojo_light'], **low_engagement()},
    {'author': 'pabloPistola', 'content': 'New PR on the 5k. Legs complained. Ignored.', 'type': 'milestones', 'days_ago': 18, **medium_engagement()},
    # Month 1-2 cluster
    {'author': 'pabloPistola', 'content': 'Glassmorphism is just frosted glass for screens.', 'type': 'thoughts', 'days_ago': 25, **high_engagement()},
    {'author': 'pabloPistola', 'content': 'Neon alley in Hong Kong. Peak cyberpunk.', 'type': 'media', 'days_ago': 30, 'media_url': MEDIA_URLS['neon_alley'], **high_engagement()},
    {'author': 'pabloPistola', 'content': 'Shipped the profile card flip animation.', 'type': 'milestones', 'days_ago': 35, **high_engagement()},
    {'author': 'pabloPistola', 'content': 'CSS is just meditation with more frustration.', 'type': 'thoughts', 'days_ago': 42, **medium_engagement()},
    {'author': 'pabloPistola', 'content': 'Eclipse corona. The universe flexing.', 'type': 'media', 'days_ago': 50, 'media_url': MEDIA_URLS['eclipse_corona'], **medium_engagement()},
    # Month 3-4 activity
    {'author': 'pabloPistola', 'content': 'Imposter syndrome upgraded to certainty.', 'type': 'thoughts', 'days_ago': 75, **low_engagement()},
    {'author': 'pabloPistola', 'content': 'Midpoint presentation done. Survived.', 'type': 'milestones', 'days_ago': 90, **high_engagement()},
    {'author': 'pabloPistola', 'content': 'Osaka nights. Sensory overload approved.', 'type': 'media', 'days_ago': 100, 'media_url': MEDIA_URLS['osaka_nights'], **medium_engagement()},
    # Month 5-6 cluster
    {'author': 'pabloPistola', 'content': 'Git history is just a diary with merge conflicts.', 'type': 'thoughts', 'days_ago': 130, **medium_engagement()},
    {'author': 'pabloPistola', 'content': 'Wudang mountains. Martial arts got philosophical.', 'type': 'media', 'days_ago': 150, 'media_url': MEDIA_URLS['wudang_mountains'], **high_engagement()},
    {'author': 'pabloPistola', 'content': 'First client signed. Accidentally a business.', 'type': 'milestones', 'days_ago': 165, **high_engagement()},
    # Month 7-9 spread
    {'author': 'pabloPistola', 'content': 'React hooks finally clicked. Only took 47 tries.', 'type': 'thoughts', 'days_ago': 200, **medium_engagement()},
    {'author': 'pabloPistola', 'content': 'Pillars of Creation. Star nursery energy.', 'type': 'media', 'days_ago': 230, 'media_url': MEDIA_URLS['nebula_pillars'], **low_engagement()},
    {'author': 'pabloPistola', 'content': 'Push, pull, merge. Lather, rinse, repeat.', 'type': 'milestones', 'days_ago': 260, **medium_engagement()},
    # Month 10-12 activity
    {'author': 'pabloPistola', 'content': 'Started the bootcamp. No idea what\'s coming.', 'type': 'thoughts', 'days_ago': 300, **low_engagement()},
    {'author': 'pabloPistola', 'content': 'Milky Way arch. We are very small.', 'type': 'media', 'days_ago': 340, 'media_url': MEDIA_URLS['milky_way_arch'], **medium_engagement()},

    # ========== arthurb (22 posts) ==========
    {'author': 'arthurb', 'content': 'Physics is just applied curiosity.', 'type': 'thoughts', 'days_ago': 0, **high_engagement()},
    {'author': 'arthurb', 'content': 'CERN tunnel. 27km of humanity asking why.', 'type': 'media', 'days_ago': 3, 'media_url': MEDIA_URLS['lhc_tunnel'], **high_engagement()},
    {'author': 'arthurb', 'content': 'Finished a 26.2 miles marathon. Why.', 'type': 'milestones', 'days_ago': 5, **high_engagement()},
    {'author': 'arthurb', 'content': 'Quantum entanglement > WiFi reliability.', 'type': 'thoughts', 'days_ago': 10, **medium_engagement()},
    {'author': 'arthurb', 'content': 'Tesla coil. Controlled chaos personified.', 'type': 'media', 'days_ago': 14, 'media_url': MEDIA_URLS['tesla_coil'], **medium_engagement()},
    {'author': 'arthurb', 'content': 'Lab results came back positive. For science.', 'type': 'milestones', 'days_ago': 20, **high_engagement()},
    {'author': 'arthurb', 'content': 'The universe left me on seen for 14 billion years.', 'type': 'thoughts', 'days_ago': 28, **medium_engagement()},
    {'author': 'arthurb', 'content': 'Laser lab aesthetics. Quantum optics glow.', 'type': 'media', 'days_ago': 35, 'media_url': MEDIA_URLS['laser_lab'], **low_engagement()},
    {'author': 'arthurb', 'content': 'Conference talk done. Questions survived.', 'type': 'milestones', 'days_ago': 45, **high_engagement()},
    {'author': 'arthurb', 'content': 'Schrödinger\'s deadline: both met and missed.', 'type': 'thoughts', 'days_ago': 60, **medium_engagement()},
    {'author': 'arthurb', 'content': 'Pillars of Creation. Dead star stuff made us.', 'type': 'media', 'days_ago': 80, 'media_url': MEDIA_URLS['nebula_pillars'], **high_engagement()},
    {'author': 'arthurb', 'content': 'Published first research paper!', 'type': 'milestones', 'days_ago': 100, **high_engagement()},
    {'author': 'arthurb', 'content': 'Time dilation means I\'m technically early.', 'type': 'thoughts', 'days_ago': 125, **low_engagement()},
    {'author': 'arthurb', 'content': 'Supermoon on the horizon. Scale check.', 'type': 'media', 'days_ago': 150, 'media_url': MEDIA_URLS['supermoon'], **medium_engagement()},
    {'author': 'arthurb', 'content': 'Got accepted to Geneva conference!', 'type': 'milestones', 'days_ago': 180, **high_engagement()},
    {'author': 'arthurb', 'content': 'Entropy increases. So does my coffee intake.', 'type': 'thoughts', 'days_ago': 210, **medium_engagement()},
    {'author': 'arthurb', 'content': 'Comet trail. Long exposure magic.', 'type': 'media', 'days_ago': 245, 'media_url': MEDIA_URLS['comet_trail'], **low_engagement()},
    {'author': 'arthurb', 'content': 'Half-marathon done. Legs questioned everything.', 'type': 'milestones', 'days_ago': 280, **medium_engagement()},
    {'author': 'arthurb', 'content': 'Fermi paradox keeps me up at night.', 'type': 'thoughts', 'days_ago': 310, **low_engagement()},
    {'author': 'arthurb', 'content': 'Storm cell forming. Nature\'s violence.', 'type': 'media', 'days_ago': 335, 'media_url': MEDIA_URLS['storm_cell'], **medium_engagement()},
    {'author': 'arthurb', 'content': 'Started the PhD journey. No turning back.', 'type': 'milestones', 'days_ago': 355, **high_engagement()},
    {'author': 'arthurb', 'content': 'Day 1 of physics program. Excited and terrified.', 'type': 'thoughts', 'days_ago': 360, **medium_engagement()},

    # ========== nataliap (20 posts) ==========
    {'author': 'nataliap', 'content': 'Beat the bread to the oven. Victory.', 'type': 'thoughts', 'days_ago': 1, **high_engagement()},
    {'author': 'nataliap', 'content': 'Server cathedral. Prayers are HTTP requests.', 'type': 'media', 'days_ago': 4, 'media_url': MEDIA_URLS['server_cathedral'], **high_engagement()},
    {'author': 'nataliap', 'content': 'Caramel hit 338°F exactly. Professional.', 'type': 'milestones', 'days_ago': 7, **high_engagement()},
    {'author': 'nataliap', 'content': 'Backend work is ctrl+F and disappointment.', 'type': 'thoughts', 'days_ago': 12, **medium_engagement()},
    {'author': 'nataliap', 'content': 'Lightning strike. Nature debugging itself.', 'type': 'media', 'days_ago': 18, 'media_url': MEDIA_URLS['lightning_strike'], **medium_engagement()},
    {'author': 'nataliap', 'content': 'JWTs verified. Middleware gatekeeping works.', 'type': 'milestones', 'days_ago': 25, **high_engagement()},
    {'author': 'nataliap', 'content': 'makemigrations. migrate. No errors. Suspicious.', 'type': 'thoughts', 'days_ago': 35, **medium_engagement()},
    {'author': 'nataliap', 'content': 'Circuit board macro. Electron city.', 'type': 'media', 'days_ago': 45, 'media_url': MEDIA_URLS['motherboard_macro'], **low_engagement()},
    {'author': 'nataliap', 'content': 'Sourdough starter survived the week.', 'type': 'milestones', 'days_ago': 55, **medium_engagement()},
    {'author': 'nataliap', 'content': 'Django ORM is just SQL with extra steps.', 'type': 'thoughts', 'days_ago': 70, **high_engagement()},
    {'author': 'nataliap', 'content': 'Fiber optics. Light running errands.', 'type': 'media', 'days_ago': 90, 'media_url': MEDIA_URLS['fiber_optic'], **medium_engagement()},
    {'author': 'nataliap', 'content': 'First API deployed. It responds!', 'type': 'milestones', 'days_ago': 115, **high_engagement()},
    {'author': 'nataliap', 'content': 'Print statements > debugger. Fight me.', 'type': 'thoughts', 'days_ago': 145, **low_engagement()},
    {'author': 'nataliap', 'content': 'Volcano lava. Molten earth energy.', 'type': 'media', 'days_ago': 175, 'media_url': MEDIA_URLS['volcano_lava'], **high_engagement()},
    {'author': 'nataliap', 'content': 'A year of gym consistency. Muscles exist.', 'type': 'milestones', 'days_ago': 210, **high_engagement()},
    {'author': 'nataliap', 'content': 'Foreign keys are just trust issues in SQL.', 'type': 'thoughts', 'days_ago': 250, **medium_engagement()},
    {'author': 'nataliap', 'content': 'Aurora cabin. Lonely but beautiful.', 'type': 'media', 'days_ago': 285, 'media_url': MEDIA_URLS['aurora_cabin'], **medium_engagement()},
    {'author': 'nataliap', 'content': 'Learned Python basics. print("hello world")', 'type': 'milestones', 'days_ago': 320, **low_engagement()},
    {'author': 'nataliap', 'content': 'Starting the coding journey. Nervous.', 'type': 'thoughts', 'days_ago': 350, **medium_engagement()},
    {'author': 'nataliap', 'content': 'Signed up for bootcamp. Let\'s go.', 'type': 'milestones', 'days_ago': 362, **high_engagement()},

    # ========== colinw (22 posts) ==========
    {'author': 'colinw', 'content':'Downtown and want to argue about shows?', 'type': 'thoughts', 'days_ago': 2, **high_engagement()},
    {'author': 'colinw', 'content': 'Eclipse corona. The universe flexing hard.', 'type': 'media', 'days_ago': 4, 'media_url': MEDIA_URLS['eclipse_corona'], **high_engagement()},
    {'author': 'colinw', 'content': 'Promoted to team lead! Leadership unlocked.', 'type': 'milestones', 'days_ago': 8, **high_engagement()},
    {'author': 'colinw', 'content': 'The best code is code someone else can fix.', 'type': 'thoughts', 'days_ago': 15, **medium_engagement()},
    {'author': 'colinw', 'content': 'Cyberpunk samurai meditation vibes.', 'type': 'media', 'days_ago': 22, 'media_url': MEDIA_URLS['meditation_mist'], **medium_engagement()},
    {'author': 'colinw', 'content': 'First 1:1 as lead went well. Learning.', 'type': 'milestones', 'days_ago': 30, **medium_engagement()},
    {'author': 'colinw', 'content': 'Simple solutions work but shouldn\'t look lazy.', 'type': 'thoughts', 'days_ago': 40, **high_engagement()},
    {'author': 'colinw', 'content': 'Wudang mountains. Mist recommended.', 'type': 'media', 'days_ago': 52, 'media_url': MEDIA_URLS['wudang_mountains'], **low_engagement()},
    {'author': 'colinw', 'content': 'Team shipped on time. First time ever.', 'type': 'milestones', 'days_ago': 65, **high_engagement()},
    {'author': 'colinw', 'content': 'Meetings could have been emails. All of them.', 'type': 'thoughts', 'days_ago': 80, **medium_engagement()},
    {'author': 'colinw', 'content': 'Akihabara sensory assault. Electric Town.', 'type': 'media', 'days_ago': 95, 'media_url': MEDIA_URLS['akihabara'], **high_engagement()},
    {'author': 'colinw', 'content': 'Half-marathon complete! 13.1 miles down.', 'type': 'milestones', 'days_ago': 115, **high_engagement()},
    {'author': 'colinw', 'content': 'Code review is just reading someone\'s diary.', 'type': 'thoughts', 'days_ago': 140, **medium_engagement()},
    {'author': 'colinw', 'content': 'Shanghai fog. Pudong through mist.', 'type': 'media', 'days_ago': 165, 'media_url': MEDIA_URLS['shanghai_fog'], **medium_engagement()},
    {'author': 'colinw', 'content': 'Got the job offer! Celebrating tonight.', 'type': 'milestones', 'days_ago': 195, **high_engagement()},
    {'author': 'colinw', 'content': 'Agile is just organized chaos with sticky notes.', 'type': 'thoughts', 'days_ago': 225, **low_engagement()},
    {'author': 'colinw', 'content': 'Aurora mountain view. Worth the cold.', 'type': 'media', 'days_ago': 255, 'media_url': MEDIA_URLS['aurora_mountain'], **high_engagement()},
    {'author': 'colinw', 'content': 'Seagull stole my burrito. Respect. Fear.', 'type': 'milestones', 'days_ago': 285, **medium_engagement()},
    {'author': 'colinw', 'content': 'Starting new role next week. Nervous energy.', 'type': 'thoughts', 'days_ago': 315, **medium_engagement()},
    {'author': 'colinw', 'content': 'Bamboo forest. Wind sounds like breathing.', 'type': 'media', 'days_ago': 340, 'media_url': MEDIA_URLS['bamboo_forest'], **low_engagement()},
    {'author': 'colinw', 'content': 'Completed the interview gauntlet. Exhausted.', 'type': 'milestones', 'days_ago': 358, **high_engagement()},
    {'author': 'colinw', 'content': 'First day at bootcamp. Everything is new.', 'type': 'thoughts', 'days_ago': 363, **medium_engagement()},

    # ========== crystalr (20 posts) ==========
    {'author': 'crystalr', 'content': 'Rest day. Body said no. I said fair.', 'type': 'thoughts', 'days_ago': 0, **high_engagement()},
    {'author': 'crystalr', 'content': 'Osaka at night. Sensory overload philosophy.', 'type': 'media', 'days_ago': 3, 'media_url': MEDIA_URLS['osaka_nights'], **high_engagement()},
    {'author': 'crystalr', 'content': 'Broke 20 minutes on the 5k. Legs outvoted.', 'type': 'milestones', 'days_ago': 6, **high_engagement()},
    {'author': 'crystalr', 'content': 'Moved a div 2 pixels. Stared. Moved it back.', 'type': 'thoughts', 'days_ago': 11, **medium_engagement()},
    {'author': 'crystalr', 'content': 'Seoul neon reflections. Every surface a screen.', 'type': 'media', 'days_ago': 18, 'media_url': MEDIA_URLS['seoul_glow'], **medium_engagement()},
    {'author': 'crystalr', 'content': 'Friend requests working! Accept, decline, block.', 'type': 'milestones', 'days_ago': 28, **high_engagement()},
    {'author': 'crystalr', 'content': 'Copilot assisted. So did caffeine and spite.', 'type': 'thoughts', 'days_ago': 40, **medium_engagement()},
    {'author': 'crystalr', 'content': 'Fiber optics. Light trapped running errands.', 'type': 'media', 'days_ago': 55, 'media_url': MEDIA_URLS['fiber_optic'], **low_engagement()},
    {'author': 'crystalr', 'content': 'First PR merged. Code is in production!', 'type': 'milestones', 'days_ago': 70, **high_engagement()},
    {'author': 'crystalr', 'content': 'CSS grid finally makes sense. Only took a week.', 'type': 'thoughts', 'days_ago': 90, **high_engagement()},
    {'author': 'crystalr', 'content': 'Aurora spiral overhead. Corona magic.', 'type': 'media', 'days_ago': 110, 'media_url': MEDIA_URLS['aurora_spiral'], **medium_engagement()},
    {'author': 'crystalr', 'content': 'Month 1: Hello World. Month 6: deployed app.', 'type': 'milestones', 'days_ago': 135, **high_engagement()},
    {'author': 'crystalr', 'content': 'Flexbox is just CSS doing yoga.', 'type': 'thoughts', 'days_ago': 165, **medium_engagement()},
    {'author': 'crystalr', 'content': 'Rare blood-red aurora. Worth the wait.', 'type': 'media', 'days_ago': 195, 'media_url': MEDIA_URLS['aurora_red'], **high_engagement()},
    {'author': 'crystalr', 'content': 'First website live! Can click things!', 'type': 'milestones', 'days_ago': 230, **high_engagement()},
    {'author': 'crystalr', 'content': 'Semicolons are just decorative at this point.', 'type': 'thoughts', 'days_ago': 265, **low_engagement()},
    {'author': 'crystalr', 'content': 'Bioluminescence waves. Ocean glowing.', 'type': 'media', 'days_ago': 295, 'media_url': MEDIA_URLS['bioluminescence'], **medium_engagement()},
    {'author': 'crystalr', 'content': 'Wrote first line of JavaScript. alert("hi")', 'type': 'milestones', 'days_ago': 325, **medium_engagement()},
    {'author': 'crystalr', 'content': 'Learning to code. Everything is confusing.', 'type': 'thoughts', 'days_ago': 350, **low_engagement()},
    {'author': 'crystalr', 'content': 'Day 1 of the journey. Let\'s see.', 'type': 'milestones', 'days_ago': 364, **medium_engagement()},

    # ========== titod (22 posts) ==========
    {'author': 'titod', 'content': 'Brain left after hour 2. Fingers kept typing.', 'type': 'thoughts', 'days_ago': 0, **high_engagement()},
    {'author': 'titod', 'content': 'Rare pink aurora. Worth the frostbite.', 'type': 'media', 'days_ago': 2, 'media_url': MEDIA_URLS['aurora_pink'], **high_engagement()},
    {'author': 'titod', 'content': '100 days of code. Half were README edits.', 'type': 'milestones', 'days_ago': 5, **high_engagement()},
    {'author': 'titod', 'content': 'Three coffees in. Jittery but functional.', 'type': 'thoughts', 'days_ago': 10, **medium_engagement()},
    {'author': 'titod', 'content': 'Milky Way arch. Billions of suns. We\'re small.', 'type': 'media', 'days_ago': 16, 'media_url': MEDIA_URLS['milky_way_arch'], **high_engagement()},
    {'author': 'titod', 'content': 'First client signed. Accidentally a business.', 'type': 'milestones', 'days_ago': 24, **high_engagement()},
    {'author': 'titod', 'content': 'Debugging is leaving angry comments for past me.', 'type': 'thoughts', 'days_ago': 33, **medium_engagement()},
    {'author': 'titod', 'content': 'Bamboo forest. Infinite green and peace.', 'type': 'media', 'days_ago': 45, 'media_url': MEDIA_URLS['bamboo_forest'], **low_engagement()},
    {'author': 'titod', 'content': 'Full-stack app done. Frontend talks to backend!', 'type': 'milestones', 'days_ago': 60, **high_engagement()},
    {'author': 'titod', 'content': 'Stack Overflow copy-paste warrior. No shame.', 'type': 'thoughts', 'days_ago': 78, **high_engagement()},
    {'author': 'titod', 'content': 'Tokyo rain reflections. Blade Runner mood.', 'type': 'media', 'days_ago': 95, 'media_url': MEDIA_URLS['tokyo_rain'], **medium_engagement()},
    {'author': 'titod', 'content': 'Deployed to production. Didn\'t break.', 'type': 'milestones', 'days_ago': 115, **high_engagement()},
    {'author': 'titod', 'content': 'npm install is just downloading the internet.', 'type': 'thoughts', 'days_ago': 140, **medium_engagement()},
    {'author': 'titod', 'content': 'Neon alley vibes. Hong Kong energy.', 'type': 'media', 'days_ago': 165, 'media_url': MEDIA_URLS['neon_alley'], **high_engagement()},
    {'author': 'titod', 'content': 'Git push without fear. Branching works.', 'type': 'milestones', 'days_ago': 195, **medium_engagement()},
    {'author': 'titod', 'content': 'Documentation is future me doing a favor.', 'type': 'thoughts', 'days_ago': 225, **low_engagement()},
    {'author': 'titod', 'content': 'Server room cathedral. Blinking lights.', 'type': 'media', 'days_ago': 255, 'media_url': MEDIA_URLS['server_cathedral'], **medium_engagement()},
    {'author': 'titod', 'content': 'First merge conflict resolved. Battle won.', 'type': 'milestones', 'days_ago': 285, **high_engagement()},
    {'author': 'titod', 'content': 'Variable naming is harder than the actual code.', 'type': 'thoughts', 'days_ago': 315, **medium_engagement()},
    {'author': 'titod', 'content': 'Lightning strike. Pure electricity.', 'type': 'media', 'days_ago': 340, 'media_url': MEDIA_URLS['lightning_strike'], **low_engagement()},
    {'author': 'titod', 'content': 'Wrote first function. It returned something!', 'type': 'milestones', 'days_ago': 355, **high_engagement()},
    {'author': 'titod', 'content': 'Started learning to code. No idea what awaits.', 'type': 'thoughts', 'days_ago': 363, **medium_engagement()},
]

print('Creating posts...')
for p in mock_posts:
    username = p['author']
    if username in users:
        # Step 1: Create the post with basic fields
        post = Post.objects.create(
            author=users[username],
            content=p['content'],
            type=p.get('type', 'thoughts'),
            media_url=p.get('media_url', None),
            # Set engagement counts from our mock data
            likes_count=p.get('likes', 0),       # NEW: Uses 'likes' from dict, defaults to 0
            comment_count=p.get('comments', 0),  # NEW: Uses 'comments' from dict
            shares_count=p.get('shares', 0),     # NEW: Uses 'shares' from dict
        )
        
        # Step 2: Override created_at timestamp for analytics spread
        # We do this AFTER create() because auto_now_add fields can't be set during creation
        days_ago = p.get('days_ago', 0)  # Get days_ago, default to 0 (today)
        post.created_at = datetime.now() - timedelta(days=days_ago)
        #                 ^^^^^^^^^^^^^^   ^^^^^^^^^^^^^^^^^^^^^
        #                 |                |
        #                 |                timedelta(days=5) = a duration of 5 days
        #                 Current date/time
        #
        # Example: If today is Dec 23 and days_ago=10:
        #          datetime.now() = Dec 23, 2024 14:30:00
        #          timedelta(days=10) = 10 days
        #          Result: Dec 13, 2024 14:30:00
        
        post.save()  # NEW: Must call save() to persist the created_at change
        
        print(f'  Created: {username} - {p["content"][:40]}... (days_ago: {days_ago})')
    else:
        print(f'  SKIPPED (user not found): {username}')

print(f'\nTotal posts in database: {Post.objects.count()}')
print('Done!')