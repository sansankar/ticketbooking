
from ticket import create_app
import os
app=create_app()

print(os.environ['FLASK_ENV'])

if __name__=='__main':
  
    app.run(debug=True,port=3000)