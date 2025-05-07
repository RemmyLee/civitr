# CIVITR

![image](https://github.com/user-attachments/assets/1014498f-b60d-4c03-9704-89e28a78c1a4)

## About

A simple web interface for interacting with the models.db file released by [rupertavery](https://www.reddit.com/user/rupertavery) 

([Reddit Post](https://www.reddit.com/r/StableDiffusion/comments/1kfvt73/civitai_model_database_checkpoints_and_loras/))

## Features

- Browse AI models by type, base model, and tags
- View model details including versions and files
- Search functionality for models, creators, and tags
- Explore creator profiles
- Filter models by various criteria
- Mobile-friendly responsive design

## Installation

1. Clone this repository
2. Install required dependencies (Flask, SQLAlchemy, etc.)
3. Place the models.db file in the instance directory
4. Run the application using `python run.py`

## Configuration

By default, this will run on port 5000 like any other Flask application. To change that, you can edit run.py:

```python
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1234)