# Bike Ride Service API

A simple, scalable FastAPI backend for managing bike ride sessions.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- IDE: PyCharm 

### 2. Setup & Running

1. **Obtain the code** 

```bash
# Clone the repository to your local machine
git clone https://github.com/Hjhh1201/locobike-test.git
```

2. **Open in PyCharm**

   Launch PyCharm.

   Click **Open Project** and select the `bike_ride_api` folder.

   PyCharm may prompt: *"Python interpreter is not configured"*. Click **Configure Python Interpreter** -> **Add Interpreter** -> **Virtualenv Environment** -> **OK**. (Or go to **Settings**, **Project** and select a proper Python interpreter)

3. **Install Dependencies**

   Open the **Terminal** tab at the bottom of PyCharm and run:

   ```bash
   pip install -r requirements.txt
   ```

4. **Running the Application**

   In the same terminal, start the Uvicorn server:

   ```bash
   uvicorn main:app --reload --port 8000
   ```

   Test the application through **Interactive FastAPI Docs**: [http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)

   **SQLite Database**: The `storage.db` file will be automatically created in the root directory upon the first request.

   (**Note: if the running is not successful, try other port number like 8001**)

   Ride IDs are **automatically incremented** (1, 2, 3, etc.) for each new session. When you execute the `start` method, the response will display the specific `ride_id` and `user_id` to verify the creation of the ride.



### Testing

We use `pytest` for unit tests of pricing logic and API constraints.



### System Design: Scaling to 500k Users

### Architecture Overview

To support 50,000 bikes and 500,000 users, the system would transition from a monolithic SQLite setup to a **Distributed Microservices Architecture**:

1. **Component Boundaries**:
   - **IoT Connector**: Uses **MQTT protocol** for low-latency, bi-directional communication with smart locks.
   - **Ride Service**: Handles session lifecycle, using **Redis** for distributed locking to prevent concurrent start/end conflicts.
   - **Pricing Engine**: An independent service that processes bills asynchronously via a Message Queue (e.g., RabbitMQ/Kafka).
2. **Failure Scenarios & Resilience**:
   - **Scenario : Database High Load**: We would implement **Read/Write Splitting** for the PostgreSQL cluster and use **Redis Caching** for active ride lookups to reduce primary DB pressure.




[Mobile App] --HTTP--> [API Gateway] --Rest--> [Ride Service]

                            |                       |
                     [Auth Service]          [PostgreSQL / Redis]
                                                    |
[Smart Lock] <-------[MQTT Broker] <----------------+




### AI Usage Reflection

1. I used Google Gemini
2. I asked AI to write some unit tests for my code. I asked AI to finish two GET apis for me. I asked AI to write the calculation method for me. 
3. The AI used pytest for unit testing. I noticed that after pip install pytest httpx, I have new dependencies but the requirements.txt is not updated, which might cause test failures for other users.
4. I  manually run  pip freeze > requirements.txt again in the terminal after using pytest to update the requirements.txt.  In the FastAPI **Interactive API Docs**: http://127.0.0.1:8000/docs, I manually tested the two POST methods. I firstly executed the start method with a user id. Then with the same user ID, I executed the end method with the same user id after waiting for more than 15 minutes (riding simulation). Then I manually checked the response from the POST methods to see if the calculation functionality works properly. 