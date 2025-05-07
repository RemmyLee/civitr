![image](https://github.com/user-attachments/assets/1014498f-b60d-4c03-9704-89e28a78c1a4)


A simple web interface for interacting with the models.db file released by https://www.reddit.com/user/rupertavery 

(https://www.reddit.com/r/StableDiffusion/comments/1kfvt73/civitai_model_database_checkpoints_and_loras/)



By defualt, this will run on port 5000 like any other flask application. To change that, you can edit run.py:

from app import create_app, db

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1234)