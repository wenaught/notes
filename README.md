[![test](https://github.com/wenaught/notes/actions/workflows/test.yml/badge.svg)](https://github.com/wenaught/notes/actions/workflows/test.yml) [![codecov](https://codecov.io/gh/wenaught/notes/branch/development/graph/badge.svg?token=X22TKAHMA4)](https://codecov.io/gh/wenaught/notes)

# Notes

**Notes** is a sample API for managing todo lists, notes, and such.
It's meant to be a showcase of my own developer skills, and serves
no other purpose.

## Configuration

**Notes** uses Flask's [instance folder](https://flask.palletsprojects.com/en/2.0.x/config/#instance-folders)
for storing configuration files. Said files can be written in either JSON or YAML and passed to Flask at runtime.

Example:
```yaml
# OpenAPI configuration values, see https://apiflask.com/configuration/#openapi-fields
CONTACT:
  name: contact
  email: contact@example.com
LICENSE:
  name: MPL 2.0
  url: https://www.mozilla.org/en-US/MPL/2.0/
DESCRIPTION: |
  A description of the API.
SERVERS:
  - name: Development Server
    url: http://localhost:5000

# Flask app configuration values, see https://flask.palletsprojects.com/en/2.0.x/config/#builtin-configuration-values
SECRET_KEY: secret
```

Following environment variables need to be set:
* `MONGO_URL` specifies the URL at which the MongoDB database for the API can be accessed;
* `FLASK_ENV` specifies the [environment](https://flask.palletsprojects.com/en/2.0.x/config/#environment-and-debug-features) for Flask, and can be set to either `development` or `production`; 
* `FLASK_APP` specifies [how to load the app](https://flask.palletsprojects.com/en/2.0.x/cli/#application-discovery) and needs to be set to `notes:create_app('<config_file_name>')`.

## Usage

**Notes** doesn't need to (but can) be installed, and can be launched 
as any other Flask application:

```shell
flask run
```

## License

**Notes** is licensed under [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/).