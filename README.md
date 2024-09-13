# AIPL ACCESS LINK : https://agratasinfotech.com/
# Agratas Infotech Private Limited ERP

Welcome to the Agratas Infotech Private Limited ERP project! This web-based ERP system leverages modern AI integrated features to streamline and enhance business processes for Agratas Infotech. Our team of 224 dedicated developers is working diligently to create a robust, scalable, and user-friendly ERP solution.

## Features

- **AI-Powered Insights:** Gain actionable insights through advanced AI algorithms.
- **User Management:** Efficiently manage users, roles, and permissions.
- **Inventory Management:** Track and manage inventory levels, orders, sales, and deliveries.
- **Financial Management:** Comprehensive financial management tools to handle accounting, billing, and payments.
- **Customer Relationship Management (CRM):** Manage customer interactions, sales, and service.
- **Human Resources:** Streamline HR processes including payroll, recruitment, and employee management.
- **Reporting and Analytics:** Generate detailed reports and analytics to drive data-informed decisions.
- **Customizable Dashboards:** Create and customize dashboards to fit your specific needs.

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
- Sandeep Singh (Ai Engineer)
- Prashant Jha (Frontend Developer)
- Arun Kumar (Data Analyst)
- ... and many more!

## Contact

For any questions or concerns, please contact our project manager at [info@agratasinfotech.com](mailto:info@agratasinfotech.com).

---
