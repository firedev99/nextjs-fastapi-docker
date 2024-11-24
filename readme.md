# 🚀 **NextJS with FastAPI Backend Starter** 

![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Postgres](https://img.shields.io/badge/Postgres-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white&style=for-the-badge)


## 🌟 **Overview**
This project is a full-stack web application built with:
- **[FastAPI](https://fastapi.tiangolo.com/)** for the backend.
- **[Next.js](https://nextjs.org/)** for the frontend.
- **[PostgreSQL](https://www.postgresql.org/)** for the database.
- **[Redis](https://redis.io/)** as a caching layer and task broker.
- **[Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)** for task management and background jobs.
- **[Docker](https://www.docker.com/)** for containerization and deployment.
- **[Ngnix](https://nginx.org/en/)** as Reverse Proxy Server.



## 🛠️ **Features**
- User authentication **(Built-in/Google)** with role-based access control.
- Frontend and Backend services are automatically proxied in a single port `8000` through **Nginx**.
- API endpoints for different user roles **(e.g., Admin, User, Doctor)**.
- Applying Caching using **Redis**.
- Asynchronous task processing with **Celery**.
- Fully containerized setup using **Docker**.
- All sensitive data is encrypted using **AES (Advanced Encryption Standard) in GCM (Galois/Counter Mode)** for robust data protection, ensuring confidentiality, integrity, and authenticity both in **backend** and **frontend**.
- Storing Hashed Passowords for security enhancement.
- General users receive short, unique URLs generated securely from `UIDs`. This ensures user-friendly links while maintaining data security.


## 📂 **Directory Structure**
```plaintext
├── backend
│   ├── alembic
│   ├── app
│   │   ├── db           # Postgres Database
│   │   ├── routers      # API Endpoints
│   │   ├── workers      # Celery Tasks
│   │   ├── main.py      # FastAPI Application
│   ├── main.py          # Declared Main FasAPI Application
│   ├── .env             # Environment variables for the backend
│   ├── alembic.ini      # Generated Alembic file
│   └── Dockerfile       # Docker configuration for the backend
├── frontend
│   ├── app              # Next.js app router
│   ├── .env             # Environment variables for the frontend
│   └── Dockerfile       # Docker configuration for the frontend
├── nginx
│   └── nginx.conf       # Nginx configuration for backend and frontend
├── .env                 # Environment variables for the root 
└── compose.yaml         # Multi-container orchestration
```

## 👻 **API Endpoints**
Endpoints | Method | Description | Params | Auth | Role 
|:---|:---:|:---|:---:|:---:|:---:|
| api/v1/auth/login | POST | Login with credentials | None | No | General | 
| api/v1/auth/signup | POST | Signup with credentials | None | No | General | 
| api/v1/auth/google | GET | Google redirect URL | Custom | No | General | 
| api/v1/auth/google/callback | GET | Google callback URL | Custom | No | General | 
| api/v1/send-email | GET | Send mail using Celery | None | No | General | 
| api/v1/tasks/{task_id} | GET | Retrive the task details | id | No | General | 
| api/v1/redis/dogs | GET | Retrive and Store Caching using Redis | None | No | General | 
| `🏥 HOSPITALS`
| api/v1/hospitals/all | GET | Retrieve all the hospitals | offset, limit | No | General | 
| api/v1/hospitals/profile | GET | Retrieve all the hospitals | id | No | General | 
| `🧜🏻‍♂️ DOCTORS`
| api/v1/users/doctor/all | GET | Retrieve all the doctors | offset, limit | No | General | 
| api/v1/users/doctors/profile | GET | Retrieve specific doctor profile | id | No | General | 
| api/v1/users/doctors/{hospital_id}/all | GET | Retrieve all the doctors of a specific hospital | id | No | General | 
| `🥶 PATIENTS`
| api/v1/users/patients/profile | GET | Retrieve specific patient profile | id | Yes | Patient | 
| api/v1/users/patients/profile | PUT | Update specific patient profile | id | Yes | Patient | 
| api/v1/users/patients/profile/password | PUT | Update specific patient profile password | None | Yes | Patient | 
| `❤️‍🩹 PATIENT HEALTH RECORDS`
| api/v1/users/patients/health/records | Get | Retrieve Specific patient health records | id | Yes | Patient | 
| api/v1/users/patients/health/records | POST | Create health records for specific patient | id | Yes | Patient | 
| api/v1/users/patients/health/records | PUT | Update specific patient health records | id | Yes | Patient | 
| api/v1/users/patients/health/records/glucoose | PUT | Update specific patient blood glucose records | id | Yes | Patient | 
| api/v1/users/patients/health/records/pressure | PUT | Update specific patient blood pressure records | id | Yes | Patient | 
| ```🦹🏻 ADMIN USERS```
| api/v1/admin/users/new | POST | Create new user | None | Yes | Admin | 
| api/v1/admin/users/all | GET | Retrieve all the users | offset, limit | Yes | Admin | 
| api/v1/admin/users/profile | GET | Retrieve specific user profile | id | Yes | Admin | 
| api/v1/admin/users/profile | PUT | Update specific user profile | id | Yes | Admin | 
| api/v1/admin/users/profile | DELETE | Delete specific user profile | id / [ids] | Yes | Admin | 
| api/v1/admin/users/patients/new | POST | Create new patient | None | Yes | Admin | 
| api/v1/admin/users/patients/all | GET | Retrieve all the patinets | offset, limit | Yes | Admin | 
| api/v1/admin/users/patients/profile | GET | Retrieve specific patient profile | id | Yes | Admin | 
| api/v1/admin/users/patients/profile | PUT | Update specific patient profile | id | Yes | Admin | 
| api/v1/admin/users/patients/profile | DELETE | Delete specific patient profile | id / [ids] | Yes | Admin | 
| api/v1/admin/users/doctors/{hospital_id}/new | POST | Create new doctor | id | Yes | Admin | 
| api/v1/admin/users/doctors/all | GET | Retrieve all the doctors | offset, limit | Yes | Admin | 
| api/v1/admin/users/doctors/profile | GET | Retrieve specific doctor profile | id | Yes | Admin | 
| api/v1/admin/users/doctors/profile | PUT | Update specific doctor profile | id | Yes | Admin | 
| api/v1/admin/users/doctors/profile | DELETE | Delete specific doctor profile | id / [ids] | Yes | Admin | 
| api/v1/admin/users/doctors/{hospital_id}/all | GET | Retrieve all the doctors of a specific hospital | id | Yes | Admin | 
| `❤️‍🩹 ADMIN PATIENT HEALTH RECORDS`
| api/v1/admin/users/patients/health/records/new | POST | Create specific patient health records | id | Yes | Admin | 
| api/v1/admin/users/patients/health/records/all | GET | Retrieve all the patient health records | offset, limit | Yes | Admin | 
| api/v1/admin/users/patients/health/records | GET | Retrieve specific patient health records | id | Yes | Admin | 
| api/v1/admin/users/patients/health/records | PUT | Update specific patient health records | id | Yes | Admin | 
| api/v1/admin/users/patients/health/records | DELETE | Delete specific patient health records | id / [ids] | Yes | Admin | 
| `🏥 ADMIN HOSPITALS`
| api/v1/admin/hospitals/new | POST | Create new hospital | None | Yes | Admin | 
| api/v1/admin/hospitals/all | GET | Retrieve all the hospitals | offset, limit | Yes | Admin | 
| api/v1/admin/hospitals/profile | GET | Retrieve specific hospital information | id | Yes | Admin | 
| api/v1/admin/hospitals/profile | PUT | Update specific hospital information | id | Yes | Admin | 
| api/v1/admin/hospitals/profile | DELETE | Delete specific hospital information | id / [ids] | Yes | Admin | 

<br>


## ⚙️ Setup and Installation 
### 1. Prerequisites 
Ensure you have the following installed:
- [docker](https://docs.docker.com/get-docker/)
- [nodejs](https://nodejs.org/en) (Optional)
- [python](https://www.python.org/downloads/) (Optional)

### 2. Clone the repository
```bash
git clone https://github.com/firedev99/nextjs-fastapi-docker.git 
cd nextjs-fastapi-docker
```

### 3. Environment Variables
Create a `.env` file the root directory 

```js
POSTGRES_USER=
POSTGRES_PASS=
POSTGRES_DATABASE_NAME=
PGADMIN_DEFAULT_EMAIL=
PGADMIN_DEFAULT_PASS=
REDIS_PASSWORD=
FLOWER_BASIC_AUTH=
```

Navigate to backend folder and create another `.env` file in that directory.
```bash
cd backend
```

```js
FRONTEND_ORIGINS=
ACCESS_TOKEN_EXPIRES=
REFRESH_TOKEN_EXPIRES=
HASHING_SECRET_KEY=
JWT_SECRET_KEY=
JWT_ALGORITHM=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=
OWNER_EMAIL=
SMTP_PASSWORD=
SMTP_HOST=
SMTP_PORT=
POSTGRES_USER=
POSTGRES_PASS=
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DATABASE_NAME=
PGADMIN_DEFAULT_EMAIL=
PGADMIN_DEFAULT_PASS=
REDIS_PASSWORD=
REDIS_HOST= 
REDIS_PORT=
FLOWER_BASIC_AUTH=
CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=
```

Navigate to frontend folder and create another `.env` file in that directory.
```bash
cd frontend
```

```js
NEXT_PUBLIC_ENCRYPTION_SECRET_KEY=
```


### 4. Create a `virtualenv` in the backend folder (Optional)
```py
python3 -m venv venv
``` 
- on mac activate using command `source venv/bin/acitvate`
- on windows activate using command `venv/Scripts/acitvate`


### 5. Start the application
Run the application using `docker-compose` command:
```bash
cd nextjs-fastapi-docker
docker-compose up 
```
- After loading all the resources and databases you can visit [http://localhost:8000](http://localhost:8000) where `Frontend` and `Backend` services are automatically proxied through `Nginx`. 

### 6. Run the Applications Locally (Optional / Will take other additional steps)
### Frontend:
```bash
cd nextjs-fastapi-docker 
cd frontend
yarn dev 
```

### Backend:
make sure the backend virtual env is activated [check this instruction](#4-create-a-virtualenv-in-the-backend-folder-optional).
```bash
cd backend
python main.py
```

### 7. Connect the PostgreSQL Database
### Dpage/PgAdmin4:
Go to [http:/localhost:8080](http:/localhost:8080) and add the following stuffs:
- host: `postgres`
- port: `5433`
- user: `postgres`
- db: `gluco_guide`

### Localhost Machine
If you intend to use the database with your locally installed applications like `dbeaver` or `pgAdmin (desktop)` just change the host to `localhost`
- host: `localhost`
- port: `5433`
- user: `postgres`
- db: `gluco_guide`


### Migrations 
Run the `backend cli` container from `docker desktop` application or use the following command from terminal

```bash
docker exec -it <container name> /bin/bash
```

Then run the following `migration` command:
```bash
alembic upgrade head
```


<br>
<br>

# 🤝 Contributing 
### 1. Create a Branch
Create a new branch for your feature or bug fix: 

 ```bash
git checkout -b feature/your-feature-name
```

### 2. Commit Your Changes 
Commit your changes with descriptive message:
```bash
git add .
git commit -m "description of your feature"
git push origin feature/your-feature-name 
```

### 3. Open a Pull Request
- Navigate to the original repository on GitHub.
- Click the `Pull Requests` tab.
- Click `New Pull Request` and select your branch.
- Provide a clear `title` and description of your changes, and submit the pull request.

<br>
<br>

# 👨🏻‍🍳 Merging and Syncing Updates 
To add upstream remote to the forked repository, run the following command

```bash
git remote add upstream https://github.com/firedev99/nextjs-fastapi-docker.git
```

To synchronized with the original repository, run the following command

```bash
git fetch upstream
git merge upstream/master
```

# 👨‍🎨 Some Useful Commands to Help with inpecting this project 
### 🔌 Github
Commit Changes 
```bash
git add .
git commit -m "commit description"
git push -u origin master
```


View Existing Remote URL
```bash
git remote -v
```


Change the "origin" Remote's URL
```bash
git remote set-url origin https://github.com/user/repo2.git
```


### 📦 Docker Compose 
If you want to run your services in the background, you can pass the `-d` flag (for "detached" mode) to `docker compose up` and use `docker compose ps`

Initialize or Run containers in detached mode w/o building new images:
```bash
docker-compose up -d 
```

Rebuild containers and run the docker instance:
```bash
docker-compose --build 
```

If you started Compose with docker compose up -d, stop your services once you've finished with them
```bash
docker-compose stop
```

You can bring everything down, removing the containers entirely, with the command:
```bash
docker-compose down
```

List the local volumes, images, containers:
```bash
docker volume ls 
docker image ls 
docker container ls 
```

Remove all dangling images. If -a is specified, also remove all images not referenced by any container, remove all the containers, remove volume.
```bash
docker image prune -a
docker container prune 
docker volume prune 
docker volume rm <volume name>
``` 


### 🛠️ IP Address Listing 
```
# for mac users

cat /etc/hosts
sudo lsof -iTCP -sTCP:LISTEN -P -n
sudo lsof -i TCP:PORTNUMBER (PORTNUMBER e.g, 3000)
# or 
sudo lsof -i :PORTNUMBER (PORTNUMBER e.g, 3000)
```
The `/etc/hosts` file is a plain text file that maps hostnames to IP addresses for the local host and other hosts on the internet.

```bash
# for windows users 

netstat -a -n -o
```

### 🫙 PostgreSQL Cluster
Check if the port is accepting connection or not from `PostgreSQL` Cluster with the following command:
```bash
pg_isready -h localhost -p 5433
```

<br>

# 📄 License 
This project is licensed under the MIT License. See the [LICENSE](LICENSE) for details.

<br>

# ⚓️ Ports 
- Main Application / Nginx: [http://localhost:8000](http://localhost:8000)
- Backend Server: [http://localhost:8001](http://localhost:8001)
- Frontend Client: [http://localhost:3000](http://localhost:3000)
- PgAdmin DB Software: [http://localhost:8080](http://localhost:8080)
- Redis DB Software: [http://localhost:5540](http://localhost:5540)
- Flower Task/Worker Monitor: [http://localhost:5555](http://localhost:5555)
- PostgreSQL Hosting Port: `5433`
- PostgreSQL Hosting Port: `6379`


<br>

# 💬 Contact
If you have any questions, feel free to reach out:
- **Github** - [@firedev99](https://github.com/firedev99)
- **Twitter** - [@firethedev99](https://twitter.com/thedevguy99)
- **Email** - firethedev@gmail.com

    