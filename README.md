(https://circleci.com/gh/circleci/mongofinil.svg?&style=shield&circle-token=164758844dde09a6836d692607af15c997c93f28)

# Type/Code Development Exercise

[Exercise Outline](https://github.com/chrisrcoles/typecodebackend/blob/master/)
[API Endpoint](http://typecodebackend-dev.us-east-1.elasticbeanstalk.com/api/v1)

## Application Architecture 

Built with [Python Django](https://www.djangoproject.com/) 

## Setting Up the Application 

1. `$> git clone https://github.com/chrisrcoles/typecodebackend`

2. Platform dependencies must be installed. You will need Python3.6 and Postgres.

- Install [Homebrew](https://docs.brew.sh/Installation)

- `$> brew install python3.6`

- `$> brew install postgres`

3. Install pip, virtualenv

- `$> sudo easy_install pip`

- `$> pip install virtualenv`

4. Create and activate virtualenv

- `$virtualenvs> virtualenv -p python3.6 typecode`

- `$virtualenvs> source typecode/bin/activate`
 
5. Install app dependencies.

- `$typecodebackend> pip install -r app/requirements.txt`

6. Create Postgres DB and Postgres User
```
   >$ psql template1
   >template1=# CREATE DATABASE typecode;
   >template1=# CREATE USER typecode with PASSWORD 'typecode';
```

7. Migrate App
 `$typecodebackend> ./app.manage.py migrate`
 
8. Start App
`$typecodebackend> ./app.manage.py runserver`
 
## API Spec

### GET /api/v1/posts

Returns an array of posts

### POST /api/v1/posts

Create a post 

### GET /api/v1/posts/:slug

Return a single post object queried by its slug

### PUT /api/v1/posts/:slug

Update a single post object by its slug

### DELETE /api/v1/posts/:slug

Delete a single post object by its slug

### GET /api/v1/posts/:post_id

Return a single post object queried by its ID

### PUT /api/v1/posts/:post_id

Update a single post object by its ID

### DELETE /api/v1/posts/:post_id

Delete a single post object by its ID