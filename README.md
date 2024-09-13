# AIPL ACCESS LINK : https://agratasinfotech.com/
# Agratas Infotech Private Limited ERP

Welcome to the Agratas Infotech Private Limited ERP project! This web-based ERP system leverages modern AI integrated features to streamline and enhance business processes for Agratas Infotech. Our team of 224 dedicated developers is working diligently to create a robust, scalable, and user-friendly ERP solution.

## Features

- **AI-Powered Task Distribution:** HR, Business Analysts, and Admins can control task flow and visualize distribution via heatmaps, utilizing AI-powered dashboards.
  
- **AI-Generated Email Templates:** GenAI creates email templates for mass outreach. Easily manage and send CSV-based bulk emails to clients.

- **Data Analytics for AI/ML Models:** Advanced Excel prompts allow Data Analysts to efficiently handle data, apply formulas, and query databases. Predict product completion, measure workforce performance, and analyze team productivity.

- **Automated Internship Enrollment System:** Simplifies handling of internship programs and event enrollments with automatic responses.

- **Razor Pay Integration:** Provides seamless payment handling through Razor Pay integration.

- **Virtual Try-On:** Allows customers to experience a virtual try-on of software solutions via the customer dashboard.

- **AI-Driven Task Automation:** Automates task distribution for product managers by prioritizing and allocating tasks based on AI-driven insights.

- **Customer Data Control:** Customers can delete their data and receive AI-generated confirmation emails within minutes, ensuring complete data removal.


## Getting Started

### Prerequisites

Before setting up the Django project, ensure you have the following installed on your system:

- Python 3.8 or higher
- Django 3.2 or higher
- pip (Python package installer)
- virtualenv (to create isolated Python environments)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/CipherNinja/AIPL_SOURCE_CODE.git
   cd AIPL_SOURCE_CODE
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup the Database**

   Apply the initial database migrations:

   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**

   Create a superuser account to access the Django admin:

   ```bash
   python manage.py createsuperuser
   ```

   Follow the prompts to set up your superuser account.

6. **Run the Development Server**

   Start the Django development server:

   ```bash
   python manage.py runserver
   ```

   Your ERP system should now be running at `http://127.0.0.1:8000/`.

### Configuration

#### Environment Variables

Ensure you set the necessary environment variables. You can create a `.env` file in the root directory to manage these variables:

```plaintext
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/erp
```

Replace `your_secret_key` with a secure, random key. Adjust the `DATABASE_URL` to match your database configuration.

## Contributing

We welcome contributions from our team of developers. If you are part of the development team, please follow these guidelines:

1. **Branch Naming Convention**
   - Use meaningful names for branches, e.g., `feature/user-authentication`, `bugfix/inventory-issue`.

2. **Pull Requests**
   - Ensure your code is well-documented.
   - Write clear, concise commit messages.
   - Submit pull requests to the `develop` branch for review.

3. **Code Reviews**
   - All code must be reviewed and approved by at least one other developer before merging.
   - Address any feedback promptly.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements

Special thanks to the dedicated team of developers who make this project possible:

- Priyesh Pandey (Backend Developer)
- Manan Tyagi (Data Analyst)
- Abhiroop Gosh (ERP Admin)
- Prashant Dwivedi (Data Analyst)
- Sandeep Singh (CEO & Ex- AI Engineer)
- Prashant Jha (Frontend Developer Intern)
- Vishal Soni (Frontend Developer Intern)
- Bhavishya Chaturvedi (Frontend Developer Intern)
- Bhavya Jethi (Frontend Developer Intern)
- Abhishek Khatana (UI-UX Developer Intern)
- S. A. Dhanuka (Devops Engg. Intern)
- Mohak Verma (Content Writer | SEO)
- Ankit Gupta (Content Writer | SEO)
- Khusi Mishra (Content Writer | SEO)
- Sahil Chaubey (SEM Manager)
- ... and many more!

## Contact

For any questions or concerns, please contact our project manager at [info@agratasinfotech.com](mailto:info@agratasinfotech.com).

---
