# Blog API

Simple backend API can be use for making a blog. This runs in python version 3.9.0.

### Model Database Structure:

    Author - is the blogger
    Category - a category for an article
    Article - article in a category, can have multiple images, comments, nested comments
    Image - set multiple images for an article
    Comment - set comments for an article
    NestedComment -set child comments for a parent comment

### Installation:

```bash
pip install -requirements.txt
```

### Migrate all apps:

```bash
python manage.py migrate
python manage.py makemigrations api
python manage.py migrate api
```

### Run server:

```bash
python manage.py runserver
```

## Available endpoints

Authentication:

```bash
auth/registration/
auth/login/
auth/user/
auth/password/change/
auth/logout/
auth/password/reset/
auth/password/reset/confirm/
```

Blog:

```
articles/                         //Method get, post
article/<slug>/detail/            //Method get, put, patch, delete
article/<slug>/comment/           //Method get, post
comment/<slug>/detail/            //Method get, put, patch, delete
article/<slug>/image/             //Method post
image/<slug>/detail/              //Method get, put, patch, delete
comment/<slug>/nested_comment/    //Method post
nested_comment/<slug>/detail/     //Method get, put, patch, delete
categories/                       //Method get, post
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
