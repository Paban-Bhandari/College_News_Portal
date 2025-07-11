from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from news.models import Category, NewsArticle, UserProfile
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the database with sample categories and articles'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {'name': 'Campus News', 'description': 'General campus announcements and updates'},
            {'name': 'Academic', 'description': 'Academic news, research, and educational updates'},
            {'name': 'Events', 'description': 'Upcoming events, workshops, and activities'},
            {'name': 'Student Life', 'description': 'Student achievements, clubs, and activities'},
            {'name': 'Technology', 'description': 'Technology updates and IT announcements'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Get or create a sample user
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@college.edu',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write('Created admin user')
        
        # Create user profile
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'is_editor': True}
        )
        
        # Create sample articles
        articles_data = [
            {
                'title': 'Welcome to the New Academic Year',
                'content': '''We are excited to welcome all students, faculty, and staff to the new academic year! 

This year brings exciting opportunities for learning, growth, and collaboration. Our campus is buzzing with energy as we prepare for another successful academic journey.

Key highlights for this semester:
- New course offerings in emerging technologies
- Enhanced library resources
- Updated campus facilities
- Expanded student support services

We encourage everyone to take advantage of the resources available and make the most of your time here. Remember, our success as an institution depends on the active participation and engagement of our entire community.

Let's make this academic year our best one yet!''',
                'summary': 'A warm welcome message to kick off the new academic year with important updates and announcements.',
                'category': categories[0],  # Campus News
                'status': 'published',
            },
            {
                'title': 'Research Symposium: Call for Papers',
                'content': '''The annual Research Symposium is now accepting paper submissions from faculty and graduate students.

This year's theme is "Innovation in Education: Bridging Theory and Practice." We invite submissions across all disciplines that address this important topic.

Important Dates:
- Abstract submission deadline: March 15, 2024
- Full paper deadline: April 30, 2024
- Symposium date: May 15-17, 2024

Categories for submission:
- Educational Technology
- Curriculum Development
- Student Engagement
- Assessment Methods
- Cross-disciplinary Research

Selected papers will be published in our annual research proceedings. For more information and submission guidelines, please visit the research office website or contact Dr. Smith at research@college.edu.''',
                'summary': 'Announcing the call for papers for our annual research symposium with important deadlines and submission guidelines.',
                'category': categories[1],  # Academic
                'status': 'published',
            },
            {
                'title': 'Spring Festival: A Celebration of Diversity',
                'content': '''Join us for our annual Spring Festival, a vibrant celebration of the diverse cultures that make our campus community so special.

This year's festival will feature:
- Cultural performances from around the world
- International food fair
- Traditional music and dance
- Art exhibitions
- Interactive workshops

The festival will take place on the main campus lawn from 10 AM to 6 PM. Admission is free and open to the entire community.

We're still accepting volunteers and performers. If you'd like to participate, please contact the Student Activities Office or email springfestival@college.edu.

This is a wonderful opportunity to learn about different cultures, make new friends, and celebrate the rich diversity of our campus community.''',
                'summary': 'Join us for the annual Spring Festival celebrating campus diversity with performances, food, and cultural activities.',
                'category': categories[2],  # Events
                'status': 'published',
            },
            {
                'title': 'Student Achievement Spotlight: Sarah Johnson',
                'content': '''Congratulations to Sarah Johnson, a senior Computer Science major, who has been awarded the prestigious National Science Foundation Graduate Research Fellowship!

Sarah's research on "Machine Learning Applications in Educational Technology" has been recognized for its innovative approach and potential impact on improving learning outcomes.

During her time at our college, Sarah has:
- Maintained a 3.9 GPA
- Published 3 research papers
- Led the Women in Computer Science club
- Mentored 15 junior students
- Completed internships at top tech companies

Sarah will be pursuing her Ph.D. at Stanford University next fall. Her success is a testament to the quality of education and mentorship available at our institution.

We're proud of Sarah's achievements and look forward to seeing her continued success in the field of computer science education.''',
                'summary': 'Celebrating Sarah Johnson\'s achievement of the NSF Graduate Research Fellowship and her contributions to our campus community.',
                'category': categories[3],  # Student Life
                'status': 'published',
            },
            {
                'title': 'Campus WiFi Upgrade Complete',
                'content': '''The IT department is pleased to announce the completion of our campus-wide WiFi upgrade project.

New features include:
- Increased bandwidth and faster speeds
- Better coverage in all buildings
- Enhanced security protocols
- Guest network access
- Improved reliability

The upgrade was completed over the summer break with minimal disruption to campus operations. All students, faculty, and staff should now experience significantly improved internet connectivity.

To connect to the new network:
1. Select "College_WiFi" from your device's WiFi settings
2. Enter your college credentials
3. Accept the security certificate if prompted

For guest access, use "College_Guest" network with the password provided at the information desk.

If you experience any connectivity issues, please contact the IT Help Desk at helpdesk@college.edu or call extension 1234.''',
                'summary': 'Announcing the completion of campus WiFi upgrade with improved speeds, coverage, and security features.',
                'category': categories[4],  # Technology
                'status': 'published',
            },
        ]
        
        for article_data in articles_data:
            article, created = NewsArticle.objects.get_or_create(
                title=article_data['title'],
                defaults={
                    'content': article_data['content'],
                    'summary': article_data['summary'],
                    'author': user,
                    'category': article_data['category'],
                    'status': article_data['status'],
                    'published_at': timezone.now(),
                }
            )
            if created:
                self.stdout.write(f'Created article: {article.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        ) 