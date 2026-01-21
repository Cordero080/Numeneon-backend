# =============================================================================
# MAKEFILE - Command Shortcuts for NUMENEON App
# =============================================================================
# 
# WHAT IS A MAKEFILE?
# A Makefile is a simple text file that stores shortcuts for terminal commands.
# The `make` command is built into macOS (and Linux). When you type `make <name>`,
# it looks for a file called "Makefile" in your current folder, finds the 
# matching shortcut name, and runs the command underneath it.
#
# HOW TO USE:
# 1. Open terminal
# 2. Navigate to this folder (wherever you cloned the repo)
# 3. Type: make <shortcut>
#
# RUN FROM ANYWHERE:
#   make -C /path/to/Numeneon-backend b
#   Or add this alias to ~/.zshrc (replace path with YOUR repo location):
#   alias numeneon='make -C /path/to/Numeneon-backend'
#   Then just type: numeneon b
#
# EXAMPLES:
#   make b          → starts the backend server
#   make f          → starts the frontend server
#   make dev        → starts BOTH servers (in separate terminals)
#   make migrate    → applies database migrations
#   make users      → lists all users in database
#
# NOTE: You MUST type "make" before every shortcut. The shortcut alone won't work.
#       ✅ Correct:
#       ❌ Wrong:   b
#
# IMPORTANT: The indentation before commands MUST be a TAB, not spaces!
# =============================================================================

# Get the directory where this Makefile is located
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

# -----------------------------------------------------------------------------
# SERVER COMMANDS - Start your development servers
# -----------------------------------------------------------------------------

b:  # Start backend (Django) server at http://localhost:8000
	cd $(ROOT_DIR)/backend && python manage.py runserver 8000

f:  # Start frontend (Vite/React) server at http://localhost:5173
	cd $(ROOT_DIR)/frontend && npm run dev

dev:  # Start both servers (opens new terminal for frontend)
	@echo "Starting backend..."
	@osascript -e 'tell app "Terminal" to do script "cd $(ROOT_DIR)/frontend && npm run dev"'
	cd $(ROOT_DIR)/backend && python manage.py runserver 8000


# -----------------------------------------------------------------------------
# DATABASE COMMANDS - Manage your Django database
# -----------------------------------------------------------------------------

migrate:  # Apply pending database migrations (run after changing models)
	cd $(ROOT_DIR)/backend && python manage.py migrate

makemigrations:  # Create new migration files after changing models
	cd $(ROOT_DIR)/backend && python manage.py makemigrations

seed:  # Populate database with test data
	cd $(ROOT_DIR)/backend && python seed_posts.py

shell:  # Open Django interactive shell (to query database manually)
	cd $(ROOT_DIR)/backend && python manage.py shell

dbshell:  # Open SQLite shell (raw SQL queries)
	cd $(ROOT_DIR)/backend && sqlite3 db.sqlite3


# -----------------------------------------------------------------------------
# USER MANAGEMENT - Create and manage users
# -----------------------------------------------------------------------------

superuser:  # Create an admin user for Django admin panel
	cd $(ROOT_DIR)/backend && python manage.py createsuperuser

users:  # List all users in database
	cd $(ROOT_DIR)/backend && python manage.py shell -c "from django.contrib.auth.models import User; [print(f'ID: {u.id}, Username: {u.username}, Email: {u.email}') for u in User.objects.all()]"


# -----------------------------------------------------------------------------
# GIT COMMANDS - Version control shortcuts
# -----------------------------------------------------------------------------

status:  # Check git status
	cd $(ROOT_DIR) && git status

push:  # Push current branch to origin
	cd $(ROOT_DIR) && git push origin $$(git branch --show-current)

pull:  # Pull latest changes from origin
	cd $(ROOT_DIR) && git pull origin $$(git branch --show-current)


# -----------------------------------------------------------------------------
# INSTALL & SETUP - Install dependencies
# -----------------------------------------------------------------------------

install-frontend:  # Install frontend npm packages
	cd $(ROOT_DIR)/frontend && npm install

install-backend:  # Install backend Python packages
	cd $(ROOT_DIR)/backend && pip install -r requirements.txt

install:  # Install both frontend and backend dependencies
	cd $(ROOT_DIR)/frontend && npm install
	cd $(ROOT_DIR)/backend && pip install -r requirements.txt


# -----------------------------------------------------------------------------
# TESTING - Run tests
# -----------------------------------------------------------------------------

test:  # Run Django tests
	cd $(ROOT_DIR)/backend && python manage.py test


# -----------------------------------------------------------------------------
# CLEANUP - Remove generated files
# -----------------------------------------------------------------------------

clean:  # Remove Python cache files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
