# Backend API using Python FastAPI

1. Create and activate a virtual environment
2. Install docker and docker-compose
3. Run a local instance of the database using:

   `docker-compose -f run-mongodb-local.yaml up -d`
4. Run the command:

   `pip install -r requirements.txt`

5. Start the API using the command:

   `uvicorn app.main:app --reload`
6. ??????
7. Profit

### To stop the API:

1. Ctrl+C on the terminal to stop the API from running
2. Stop the local database using:

   `docker-compose -f run-mongodb-local.yaml down`
