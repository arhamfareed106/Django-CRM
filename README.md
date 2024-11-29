# Django Customer Relationship Management (DCRM)

A sophisticated Customer Relationship Management system built with Django, featuring advanced analytics, interactive visualizations, and a modern user interface.

## 🌟 Features

### 📊 Advanced Analytics Dashboard
- **Record Growth Forecast**: Time-series analysis with 7-day moving average predictions
- **Anomaly Detection**: Statistical analysis to identify unusual record patterns
- **State-based Analytics**: Geographic distribution of records with clustering
- **Interactive Visualizations**: Powered by ApexCharts.js for dynamic data representation

### 👥 Customer Record Management
- Create, read, update, and delete customer records
- Comprehensive customer information tracking
- Advanced search and filtering capabilities
- Bulk record operations
- Data validation and error handling

### 🔒 Security & Authentication
- Secure user authentication system
- Role-based access control
- Password encryption
- Session management
- Protected API endpoints

### 🎨 Modern User Interface
- Responsive design for all devices
- Dark mode support
- Interactive data visualizations
- Intuitive navigation
- Tailwind CSS styling

## 🛠️ Technical Stack

### Backend
- **Framework**: Django 5.1.3
- **Database**: SQLite
- **Python Version**: 3.13.0

### Frontend
- **CSS Framework**: Tailwind CSS
- **Charts**: ApexCharts.js
- **Icons**: Font Awesome
- **Animations**: AOS (Animate On Scroll)

### Key Libraries
- pandas: Data manipulation and analysis
- numpy: Numerical computations
- scipy: Scientific computing
- scikit-learn: Machine learning operations
- faker: Test data generation

## 📦 Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd dcrm
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Generate sample data (optional):
```bash
python manage.py generate_records 1000
```

7. Run the development server:
```bash
python manage.py runserver
```

## 🚀 Usage

### Dashboard Analytics
- Access the dashboard at `/dashboard/`
- View record growth trends and forecasts
- Monitor anomaly detection results
- Analyze state-based record distribution

### Record Management
- Add new records at `/add_record/`
- View and edit records at `/record/<id>/`
- Delete records at `/delete_record/<id>/`
- Search records using the search bar

### User Management
- Register new users at `/register/`
- Login at `/login/`
- Logout at `/logout/`
- View features at `/features/`

## 🔧 Development

### Project Structure
```
dcrm/
├── dcrm/                   # Project settings
├── website/                # Main application
│   ├── management/         # Custom management commands
│   ├── migrations/         # Database migrations
│   ├── static/            # Static files (CSS, JS)
│   ├── templates/         # HTML templates
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   └── urls.py            # URL routing
└── requirements.txt       # Project dependencies
```

### Key Components

#### Models
- `Record`: Customer information storage
- Custom user model with enhanced capabilities

#### Views
- Class-based views for CRUD operations
- API endpoints for analytics data
- Authentication views
- Dashboard views with analytics

#### Templates
- Base template with common layout
- Dashboard template with charts
- Record management forms
- Authentication templates

## 📈 Analytics Features

### Record Growth Forecast
- Time series analysis of record creation
- 7-day moving average calculation
- Future growth predictions
- Confidence intervals

### Anomaly Detection
- Statistical analysis of record patterns
- Dynamic threshold calculation
- Automatic anomaly flagging
- Visual representation of anomalies

### State Clusters
- Geographic distribution analysis
- State-based record density
- Cluster visualization
- Regional trends

## 🔐 Security Measures

- CSRF protection
- Password hashing
- Session security
- Form validation
- XSS prevention
- SQL injection protection

## 🎯 Future Enhancements

1. Advanced Reporting
   - Custom report generation
   - Export capabilities
   - Scheduled reports

2. Enhanced Analytics
   - Predictive customer behavior
   - Advanced segmentation
   - Custom metrics

3. Integration Features
   - Email integration
   - Calendar sync
   - Document management

4. Performance Optimization
   - Caching implementation
   - Query optimization
   - Bulk operations

## 👥 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django Framework
- Tailwind CSS
- ApexCharts.js
- Open source community
