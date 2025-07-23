from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from news.models import Category, NewsArticle, UserProfile
import random

class Command(BaseCommand):
    help = 'Populate database with sample categories and articles'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {
                'name': 'Campus News',
                'description': 'Latest updates and announcements from the college campus'
            },
            {
                'name': 'Academic',
                'description': 'Academic news, research updates, and educational content'
            },
            {
                'name': 'Student Life',
                'description': 'Student activities, events, and campus life stories'
            },
            {
                'name': 'Sports',
                'description': 'Sports news, team updates, and athletic achievements'
            },
            {
                'name': 'Technology',
                'description': 'Technology trends, innovations, and digital developments'
            }
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
        
        # Create admin user if not exists
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@college.edu',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('Created admin user')
        
        # Create editor user if not exists
        editor_user, created = User.objects.get_or_create(
            username='editor',
            defaults={
                'email': 'editor@college.edu',
                'first_name': 'Editor',
                'last_name': 'User',
                'is_staff': True,
                'is_active': True
            }
        )
        if created:
            editor_user.set_password('editor123')
            editor_user.save()
            self.stdout.write('Created editor user')
        
        # Ensure UserProfile exists for both users
        admin_profile, _ = UserProfile.objects.get_or_create(user=admin_user)
        editor_profile, _ = UserProfile.objects.get_or_create(user=editor_user)
        
        # Make editor an editor
        if not editor_profile.is_editor:
            editor_profile.is_editor = True
            editor_profile.save()
        
        # Sample articles data for each category
        articles_data = {
            'Campus News': [
                {
                    'title': 'New Library Extension Opens',
                    'summary': 'The college library has been extended with modern study spaces and digital resources.',
                    'content': '''The much-anticipated library extension has finally opened its doors to students and faculty. The new wing features state-of-the-art study spaces, digital resource centers, and collaborative work areas.

The extension includes:
- 200 new study spaces
- Digital media labs
- Group discussion rooms
- 24/7 access areas
- Enhanced WiFi coverage

"This expansion represents our commitment to providing students with the best possible learning environment," said Dr. Sarah Johnson, Dean of Academic Affairs. "The new facilities will support both individual study and collaborative learning."

The project was completed on schedule and within budget, thanks to generous donations from alumni and local businesses. Students can now access the new facilities during regular library hours, with plans to extend access to 24/7 in the coming months.

The grand opening ceremony will be held next Friday at 2 PM, with refreshments and guided tours available for all attendees.''',
                    'author': admin_user,
                    'status': 'published'
                },
                {
                    'title': 'Campus Safety Improvements Announced',
                    'summary': 'New security measures and safety protocols have been implemented across campus.',
                    'content': '''The college administration has announced comprehensive safety improvements across the entire campus. These measures include enhanced lighting, additional security cameras, and improved emergency response systems.

Key improvements include:
- Installation of 50 new security cameras
- Enhanced lighting in parking areas
- Emergency call boxes at strategic locations
- Improved campus shuttle service
- Updated safety protocols for all buildings

"Student safety is our top priority," stated Campus Security Director Michael Chen. "These improvements will create a safer environment for everyone on campus while maintaining the welcoming atmosphere our community values."

The safety improvements were developed in consultation with students, faculty, and local law enforcement. Regular safety audits will be conducted to ensure all systems remain effective and up-to-date.

Students are encouraged to report any safety concerns through the new campus safety app, available for download on all major platforms.''',
                    'author': editor_user,
                    'status': 'published'
                },
                {
                    'title': 'Student Center Renovation Complete',
                    'summary': 'The student center has been completely renovated with modern amenities and improved spaces.',
                    'content': '''After six months of construction, the student center renovation is finally complete. The updated facility now features modern dining options, improved study areas, and enhanced recreational spaces.

The renovation includes:
- New food court with diverse dining options
- Updated student lounge areas
- Modern fitness center
- Improved accessibility features
- Enhanced WiFi and charging stations

"The new student center provides a central hub for campus life," said Student Affairs Director Lisa Rodriguez. "We've created spaces that support both academic and social needs of our diverse student body."

The grand reopening celebration will feature live music, food samples from the new vendors, and guided tours of the facilities. All students are invited to attend and explore the new spaces.

Regular hours of operation will begin next Monday, with extended hours during finals week.''',
                    'author': admin_user,
                    'status': 'published'
                },
                {
                    'title': 'Parking System Upgrade',
                    'summary': 'The campus parking system has been upgraded with digital permits and improved management.',
                    'content': '''The college has implemented a new digital parking system to improve campus parking management and reduce congestion. The new system includes digital permits, real-time parking availability, and improved enforcement.

New features include:
- Digital parking permits
- Real-time parking space availability
- Mobile app for permit management
- Improved signage and wayfinding
- Enhanced accessibility parking

"The new system will make parking more convenient and efficient for everyone," explained Facilities Manager David Thompson. "Students can now check parking availability in real-time and manage their permits through their phones."

The transition to the new system will be gradual, with both old and new systems running in parallel for the first month. Training sessions for faculty and staff will be held throughout the week.

Students can download the new parking app and register their vehicles starting next Monday.''',
                    'author': editor_user,
                    'status': 'published'
                }
            ],
            'Academic': [
                {
                    'title': 'New Computer Science Program Launched',
                    'summary': 'The college introduces a new Computer Science program with cutting-edge curriculum.',
                    'content': '''The Department of Computer Science has launched a new undergraduate program designed to prepare students for the rapidly evolving technology industry. The program features a modern curriculum that includes artificial intelligence, cybersecurity, and software engineering.

Program highlights:
- Industry-aligned curriculum
- Hands-on project experience
- Internship opportunities
- Modern programming languages
- Cloud computing focus

"Technology is transforming every industry, and our new program ensures students are prepared for these changes," said Dr. Robert Kim, Chair of Computer Science. "We've designed the curriculum in collaboration with industry leaders to ensure relevance and employability."

The program includes partnerships with major tech companies for internships and capstone projects. Students will have access to state-of-the-art computer labs and development environments.

Applications for the fall semester are now open, with limited spots available for the inaugural class.''',
                    'author': admin_user,
                    'status': 'published'
                },
                {
                    'title': 'Research Grant Awarded to Biology Department',
                    'summary': 'The Biology Department receives a major research grant for environmental studies.',
                    'content': '''The Biology Department has been awarded a $2.5 million research grant from the National Science Foundation for a comprehensive study of local ecosystem changes and their impact on biodiversity.

The research project will:
- Study local ecosystem changes over 5 years
- Monitor biodiversity in campus wetlands
- Develop conservation strategies
- Train students in field research
- Publish findings in peer-reviewed journals

"This grant represents a significant opportunity for our department and students," said Dr. Emily Watson, Principal Investigator. "Students will gain hands-on research experience while contributing to important environmental science."

The project will involve both undergraduate and graduate students, providing valuable research experience and potential publication opportunities. Field work will begin next month with regular updates shared with the campus community.

The research team will also host public seminars to share findings with the broader community.''',
                    'author': editor_user,
                    'status': 'published'
                },
                {
                    'title': 'Online Learning Platform Enhanced',
                    'summary': 'The college has upgraded its online learning platform with new features and improved accessibility.',
                    'content': '''The college has significantly enhanced its online learning platform to provide better support for both in-person and remote learning. The upgrades include improved video conferencing, enhanced collaboration tools, and better mobile accessibility.

New platform features:
- Enhanced video conferencing capabilities
- Improved file sharing and collaboration
- Better mobile app experience
- Accessibility improvements
- Integration with popular educational tools

"The enhanced platform supports our commitment to flexible, accessible education," said Dr. Jennifer Lee, Director of Educational Technology. "These improvements will benefit all students, whether they're learning on-campus or remotely."

Faculty have received training on the new features, and student orientation sessions are scheduled throughout the semester. The platform now supports seamless integration with popular educational tools and resources.

Students can access the enhanced platform through the college portal, with 24/7 technical support available.''',
                    'author': admin_user,
                    'status': 'published'
                },
                {
                    'title': 'Study Abroad Programs Expanded',
                    'summary': 'New study abroad opportunities have been added to the college\'s international programs.',
                    'content': '''The Office of International Programs has expanded its study abroad offerings with new partnerships in Europe, Asia, and South America. Students now have access to programs in 15 countries across 25 partner institutions.

New program destinations include:
- Barcelona, Spain (Business and Culture)
- Tokyo, Japan (Technology and Innovation)
- Buenos Aires, Argentina (Spanish Language and Culture)
- Berlin, Germany (Engineering and Sustainability)
- Cape Town, South Africa (Environmental Studies)

"Study abroad experiences are transformative for students," said Dr. Maria Santos, Director of International Programs. "These new partnerships provide diverse opportunities for academic and cultural growth."

Programs range from summer sessions to full academic years, with options for all majors. Financial aid and scholarships are available to make these experiences accessible to all students.

Information sessions will be held throughout the semester, with application deadlines varying by program.''',
                    'author': editor_user,
                    'status': 'published'
                }
            ],
            'Student Life': [
                {
                    'title': 'Spring Festival Planning Underway',
                    'summary': 'Student organizations are planning the annual Spring Festival with exciting new events.',
                    'content': '''The annual Spring Festival is returning with an expanded lineup of events and activities. Student organizations have been working together to create a week-long celebration that showcases campus diversity and talent.

Festival highlights include:
- International food fair
- Student talent show
- Cultural performances
- Art exhibitions
- Sports tournaments
- Live music concerts

"The Spring Festival is one of our most anticipated events," said Student Government President Alex Chen. "This year we're focusing on inclusivity and celebrating the diverse backgrounds of our student body."

The festival will feature over 50 student organizations and include both traditional and new events. Planning committees are still accepting proposals for additional activities and performances.

Volunteer opportunities are available for students interested in helping with event coordination and setup.''',
                    'author': admin_user,
                    'status': 'published'
                },
                {
                    'title': 'New Student Clubs Approved',
                    'summary': 'Several new student clubs have been approved, offering more opportunities for involvement.',
                    'content': '''The Student Activities Board has approved 12 new student clubs, bringing the total number of registered organizations to over 100. The new clubs cover a wide range of interests including academic, cultural, and recreational activities.

New clubs include:
- Robotics and Automation Club
- Environmental Sustainability Group
- Photography and Digital Arts Society
- Entrepreneurship Network
- Mental Health Awareness Coalition
- International Students Association

"Student clubs provide valuable opportunities for leadership development and community building," said Student Activities Director Rachel Green. "These new organizations reflect the diverse interests and needs of our student body."

All new clubs are currently recruiting members and planning their first events. Students interested in joining can attend the upcoming Club Fair or contact club leaders directly.

Funding and resources are available to support club activities and events throughout the academic year.''',
                    'author': editor_user,
                    'status': 'published'
                },
                {
                    'title': 'Campus Housing Improvements',
                    'summary': 'Residence halls have been upgraded with new amenities and improved living spaces.',
                    'content': '''The college has completed major improvements to campus housing facilities, including new amenities, updated common areas, and enhanced security features. The upgrades affect all residence halls and apartment complexes.

Improvements include:
- Updated kitchen facilities
- New study lounges
- Enhanced WiFi coverage
- Improved laundry facilities
- Security system upgrades
- Accessibility improvements

"These improvements create a more comfortable and supportive living environment for our students," said Housing Director Mark Williams. "We've focused on creating spaces that support both academic success and social connection."

The upgrades were completed during summer break to minimize disruption to student life. All residence halls are now fully operational with the new amenities available to all residents.

Student feedback was incorporated into the planning process, ensuring the improvements address actual student needs and preferences.''',
                    'author': admin_user,
                    'status': 'published'
                },
                {
                    'title': 'Career Services Expands Programs',
                    'summary': 'The Career Services office has expanded its programs to better support student career development.',
                    'content': '''Career Services has launched new programs and resources to better support student career development and job placement. The expanded services include enhanced internship programs, career counseling, and networking opportunities.

New programs include:
- Industry-specific career fairs
- Mock interview workshops
- Resume writing clinics
- Networking events
- Alumni mentorship program
- Job shadowing opportunities

"Our expanded services reflect the changing job market and student needs," said Career Services Director Sarah Martinez. "We're providing more personalized support to help students achieve their career goals."

The office has also partnered with local businesses and alumni to create more internship and job opportunities. Regular workshops and events are scheduled throughout the semester.

Students can schedule appointments through the online portal or visit the Career Services office during walk-in hours.''',
                    'author': editor_user,
                    'status': 'published'
                }
            ],
            'Sports': [
                {
                    'title': 'Basketball Team Wins Conference Championship',
                    'summary': 'The college basketball team has won the conference championship for the third consecutive year.',
                    'content': '''The college basketball team has secured its third consecutive conference championship with a thrilling victory in the final game. The team's success reflects the dedication of players, coaches, and the entire athletic department.

Season highlights:
- 25-3 overall record
- Conference championship victory
- Three players named to All-Conference team
- Coach of the Year award
- Record attendance at home games

"This championship represents the culmination of hard work and dedication from everyone involved," said Head Coach James Wilson. "Our players have shown exceptional skill and sportsmanship throughout the season."

The team will now advance to the national tournament, where they hope to build on their conference success. Fans are encouraged to show their support at upcoming games and events.

A celebration ceremony will be held next week to recognize the team's achievements and thank the campus community for their support.''',
                    'author': admin_user,
                    'status': 'published'
                },
                {
                    'title': 'New Athletic Facilities Opening',
                    'summary': 'State-of-the-art athletic facilities are opening to support student athletes and recreational sports.',
                    'content': '''The college is opening new state-of-the-art athletic facilities that will benefit both varsity athletes and recreational sports participants. The facilities include a new fitness center, indoor track, and specialized training areas.

New facilities include:
- 10,000 square foot fitness center
- Indoor running track
- Olympic-size swimming pool
- Multi-purpose courts
- Sports medicine center
- Nutrition center

"These facilities represent our commitment to athletic excellence and student wellness," said Athletic Director Lisa Thompson. "They provide opportunities for both competitive athletes and recreational sports enthusiasts."

The facilities will be available to all students, faculty, and staff with appropriate memberships. Regular fitness classes and training programs will be offered throughout the year.

An open house event will be held this weekend, with guided tours and demonstrations of the new equipment and facilities.''',
                    'author': editor_user,
                    'status': 'published'
                },
                {
                    'title': 'Swimming Team Breaks Records',
                    'summary': 'The swimming team has broken several school records at the regional championships.',
                    'content': '''The college swimming team has achieved remarkable success at the regional championships, breaking five school records and qualifying multiple athletes for the national championships. The team's performance demonstrates exceptional training and dedication.

Record-breaking performances:
- Women's 200m freestyle relay
- Men's 100m butterfly
- Women's 400m individual medley
- Men's 200m backstroke
- Women's 800m freestyle relay

"The team's success reflects the quality of our training program and the dedication of our athletes," said Swimming Coach Michael Rodriguez. "These records represent years of hard work and preparation."

The team will now prepare for the national championships, where they hope to continue their record-breaking performance. The swimming program has become a model for athletic excellence at the college.

A special recognition ceremony will be held to celebrate the team's achievements and honor the record-breaking athletes.''',
                    'author': admin_user,
                    'status': 'published'
                },
                {
                    'title': 'Intramural Sports Program Expanded',
                    'summary': 'The intramural sports program has been expanded with new sports and leagues.',
                    'content': '''The intramural sports program has been significantly expanded to provide more recreational opportunities for students. New sports have been added, and existing leagues have been restructured to accommodate more participants.

New sports and leagues:
- Ultimate Frisbee league
- Indoor soccer tournaments
- Basketball leagues (multiple divisions)
- Volleyball competitions
- Tennis doubles tournaments
- Badminton championships

"Intramural sports provide valuable opportunities for fitness, social connection, and friendly competition," said Recreational Sports Director David Chen. "The expanded program ensures there's something for everyone."

The program now serves over 1,000 students annually, with leagues running throughout the academic year. Registration for fall leagues is now open, with early registration discounts available.

All skill levels are welcome, with divisions designed to ensure competitive balance and enjoyable participation for all students.''',
                    'author': editor_user,
                    'status': 'published'
                }
            ],
            'Technology': [
                {
                    'title': 'Campus WiFi Network Upgraded',
                    'summary': 'The campus WiFi network has been upgraded to provide faster, more reliable internet access.',
                    'content': '''The college has completed a major upgrade to the campus WiFi network, providing faster speeds, better coverage, and improved reliability. The upgrade affects all academic buildings, residence halls, and outdoor spaces.

Network improvements include:
- 5G WiFi technology
- Expanded coverage areas
- Improved bandwidth capacity
- Enhanced security features
- Better device compatibility
- Outdoor WiFi zones

"The upgraded network supports our increasingly digital campus environment," said IT Director Robert Johnson. "Students and faculty can now access high-speed internet anywhere on campus."

The upgrade was completed during summer break to minimize disruption. All users can now connect to the new network using their existing credentials, with improved performance and reliability.

Technical support is available for users experiencing connection issues, and regular maintenance schedules will be posted to minimize service interruptions.''',
                    'author': admin_user,
                    'status': 'published'
                },
                {
                    'title': 'New Computer Labs Open',
                    'summary': 'Three new computer labs have opened with the latest technology and software.',
                    'content': '''The college has opened three new computer labs equipped with the latest technology and software to support academic programs and research. The labs feature high-performance computers, specialized software, and collaborative workstations.

Lab features include:
- High-performance workstations
- 3D modeling and design software
- Data analysis tools
- Video editing suites
- Virtual reality equipment
- Collaborative workspaces

"These labs provide students with access to professional-grade technology and software," said Computer Lab Manager Sarah Kim. "They support both academic coursework and research projects."

The labs are available to all students during regular hours, with extended hours during finals week. Training sessions are available for specialized software and equipment.

Reservations can be made online for group projects or specialized equipment use.''',
                    'author': editor_user,
                    'status': 'published'
                },
                {
                    'title': 'Mobile App for Campus Services',
                    'summary': 'A new mobile app has been launched to provide easy access to campus services and information.',
                    'content': '''The college has launched a comprehensive mobile app that provides students, faculty, and staff with easy access to campus services, information, and resources. The app consolidates multiple services into a single, user-friendly platform.

App features include:
- Course registration and schedules
- Campus dining menus and payments
- Library resources and reservations
- Parking permit management
- Event calendars and tickets
- Emergency alerts and notifications

"The mobile app enhances the campus experience by providing convenient access to essential services," said Digital Services Director Lisa Wang. "It's designed to save time and improve communication."

The app is available for both iOS and Android devices, with regular updates planned to add new features and improvements. User feedback will be incorporated into future development.

Training sessions are available for users who need help navigating the app's features and functionality.''',
                    'author': admin_user,
                    'status': 'published'
                },
                {
                    'title': 'Cybersecurity Awareness Program',
                    'summary': 'A comprehensive cybersecurity awareness program has been launched to protect campus digital resources.',
                    'content': '''The college has launched a comprehensive cybersecurity awareness program to educate students, faculty, and staff about online safety and data protection. The program includes training sessions, resources, and ongoing support.

Program components include:
- Online security training modules
- Phishing awareness campaigns
- Password security workshops
- Data protection guidelines
- Incident response procedures
- Regular security updates

"Cybersecurity is everyone's responsibility," said Information Security Officer David Lee. "This program helps our community understand and practice good security habits."

The program is mandatory for all students and employees, with completion certificates required for continued access to campus systems. Regular updates and refresher training will be provided.

Students can access training materials through the campus portal, with in-person sessions available for those who prefer face-to-face instruction.''',
                    'author': editor_user,
                    'status': 'published'
                }
            ]
        }
        
        # Create articles for each category
        articles_created = 0
        for category in categories:
            if category.name in articles_data:
                for article_data in articles_data[category.name]:
                    article, created = NewsArticle.objects.get_or_create(
                        title=article_data['title'],
                        defaults={
                            'content': article_data['content'],
                            'summary': article_data['summary'],
                            'author': article_data['author'],
                            'category': category,
                            'status': article_data['status'],
                            'published_at': timezone.now()
                        }
                    )
                    if created:
                        articles_created += 1
                        self.stdout.write(f'Created article: {article.title}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(categories)} categories and {articles_created} articles'
            )
        ) 