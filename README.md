# hashchat

This is a demonstration project of setting up django-channels and using it for a simple group chat

This project uses a simple authentication mechanism and a basic connection
to websockets. 

Just running the project should do it

```
docker-compose up
```

EDIT 1:
Added a sample implementation for on the fly language translation using an ML model from huggingface
For demonstration I just have a EN-DE translation

Before running the app yu need to download the models
```
./manage.py download_language_models --source=de --target=en
./manage.py download_language_models --source=en --target=de
```

Then runserver
```
./manage.py runserver
```