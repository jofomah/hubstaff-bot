
import os

from hubstaff import app


app.run(host=os.environ.get('APP_HOST'), port=os.environ.get('APP_PORT'), debug=True)
