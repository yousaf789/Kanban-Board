# Kanban Board
A simple and efficient Kanban board application designed to streamline project management and task organization. This application uses Flask for routing and HTML/CSS for structure, providing an easy-to-use interface for managing tasks.

## Features
- User-based login system for personalized Kanban boards.
- Secure access to individual boards with saved progress and customizations.
- Arrow functionality for easy task management.
- Add, edit, and delete tasks with ease.
- Organize tasks into categories (To Do, In Progress, Completed).

## Installation
1. Clone the repository

```bash
git clone https://github.com/yourusername/kanban-board.git
```
2. Create and activate a virtual environment

```bash
cd kanban-board
python -m venv venv
venv\Scripts\activate # For MacOS, use: source venv/bin/activate
```
3. Insall the require packages

```bash
pip install -r requirements.txt
```
## Usage
1. Run the Flask application

```bash
flask run
```
2. Open a web browser and visit 'https://127.0.0.1:5000' to access the Kanban board.
3. Register a new account or login to an existing one to start organizing your tasks.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)