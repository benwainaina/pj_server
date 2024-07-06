<h1>Server Instructions</h1>

1. Make sure you have docker installed on your machine.
2. The project already ships with the .env files that are needed, so simply:
   1. change run.sh to be executable by typing:
      1. chmod +x run.sh
      2. type `./run.sh build` and hit enter. This which will build the image.
      3. type `./run.sh start` and hit enter. This will start the container.
      4. Now your server is ready to accept requests
3. You can now access the API documentation at this endpoint:
   - http://localhost:8000/swagger/

That is it!
