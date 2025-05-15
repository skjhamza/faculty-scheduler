
Built by https://www.blackbox.ai

---

# Faculty Scheduler

## Project Overview
Faculty Scheduler is a web application designed to help manage departments and programs within educational institutions. It provides functionalities for tracking departments, programs, and associated entities such as teachers and students. The application is built with Flask and utilizes SQLAlchemy for database interactions.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/faculty-scheduler.git
   cd faculty-scheduler
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file or export the variables in your terminal:
   ```bash
   export SECRET_KEY='your-secret-key'
   export DATABASE_URL='sqlite:///faculty_scheduler.db'
   export MAIL_SERVER='your-mail-server'
   export MAIL_PORT=587  # or appropriate port
   export MAIL_USE_TLS=True
   export MAIL_USERNAME='your-email'
   export MAIL_PASSWORD='your-password'
   ```

5. **Run the application**:
   ```bash
   python run.py
   ```

## Usage
After running the application, you can access it via `http://127.0.0.1:5000/`. The application will allow you to manage departments and programs, view teachers and students, and implement various features to streamline academic management.

## Features

- Manage **Departments** and **Programs** with options to add, update, and retrieve information.
- Retrieve counts of **Teachers** and **Students** associated with each department.
- Calculate current semester and total credits for programs (with placeholder methods for future logic).
- Filter and retrieve students by enrollment year.
- Configuration options for mailing notifications and session management.

## Dependencies

The project is built on the following dependencies (found in `requirements.txt`):

- Flask
- Flask-SQLAlchemy

(Note: Please ensure to check the `requirements.txt` file for any additional dependencies that may not be explicitly detailed here.)

## Project Structure

The project is structured as follows:

```
faculty-scheduler/
│
├── app/                  # Main application package
│   ├── __init__.py       # Application factory
│   └── models.py         # Database models (Department, Program, etc.)
│
├── config.py             # Configuration settings
├── run.py                # Entry point to run the application
└── requirements.txt       # Python package dependencies
```

This structure provides a clean separation between application logic, configurations, and model definitions, making the project maintainable and scalable.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.