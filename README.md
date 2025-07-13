# College News Portal

A modern Django-based news portal for college campuses with user authentication, article management, and interactive features like comments and likes.

## Features

- **User Authentication**: Registration, login, logout, and password management
- **Article Management**: Create, edit, delete, and publish articles
- **Categories**: Organize articles by categories
- **Interactive Features**: Like articles and comment system
- **User Dashboard**: Personal dashboard for managing articles
- **Responsive Design**: Modern, mobile-friendly interface
- **Admin Interface**: Full Django admin integration

## Technology Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite (can be configured for PostgreSQL/MySQL)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Image Handling**: Pillow

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd college-news-portal
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the project root with the following variables:
   ```
   DJANGO_SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   ```

6. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Populate with sample data (optional)**
   ```bash
   python manage.py populate_sample_data
   ```

9. **Run the development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    - Main site: http://127.0.0.1:8000/
    - Admin interface: http://127.0.0.1:8000/admin/

## Project Structure

```
college_news_portal/
├── college_news/          # Django project settings
├── news/                  # Main application
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── urls.py           # URL routing
│   ├── forms.py          # Form definitions
│   ├── admin.py          # Admin interface
│   └── templates/        # HTML templates
├── media/                # User-uploaded files
├── static/               # Static files (CSS, JS, images)
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Models

### NewsArticle
- Title, content, summary
- Author (User)
- Category
- Status (draft, published, archived)
- Featured image
- View count, likes, comments
- Timestamps

### Category
- Name and description
- Related articles

### UserProfile
- Extended user information
- Bio and profile picture
- Editor privileges

### Like
- User or anonymous likes
- IP address tracking for anonymous users

### Comment
- User or anonymous comments
- Approval system
- Content moderation

## Management Commands

- `populate_sample_data`: Creates sample categories and articles for testing

## Security Features

- CSRF protection
- XSS protection
- Secure headers (in production)
- Input validation
- User authentication and authorization

## Deployment

### Production Settings

1. Set `DJANGO_DEBUG=False`
2. Use a strong `DJANGO_SECRET_KEY`
3. Configure `DJANGO_ALLOWED_HOSTS` with your domain
4. Set up a production database (PostgreSQL recommended)
5. Configure static file serving
6. Set up SSL/HTTPS

### Environment Variables

- `DJANGO_SECRET_KEY`: Django secret key for security
- `DJANGO_DEBUG`: Set to False in production
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue on the GitHub repository. 