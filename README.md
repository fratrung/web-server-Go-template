# Web Server Template in Go  

This repository provides a **basic template** for developing a **simple web server in Go** that serves HTML pages.  
The server is automatically generated through a Python script, which creates the necessary code to handle **GET requests** for various HTML pages.  

---

## 🚀 Installation & Usage  

### Requirements  
Before proceeding, make sure you have installed:  
- [Go](https://go.dev/dl/)  
- [Python 3](https://www.python.org/downloads/)  
- [Docker](https://www.docker.com/get-started)  

---

### 1. Clone the repository  
Download the repository from Git:  
```bash
git clone https://github.com/fratrung/web-server-Go-template.git
cd web-server-Go-template
```
Rename **.env.example** in **.env**

### 2. Configurations
Before starting the server, modify the following files to set up the IP and port:
- **.env** -> Contains credentials for the database. (database is not implemented actually)
    **example**
    ```bash
    DB_USER=user
    DB_PASSWORD=passwordsecure
    ```
- **config.yaml** -> Define server settings and environment variables for database.

    ```yaml
    database:
        host: localhost
        port: 5432
        name: "myDB"
    
    web-server:
        port: 8080
    ```
### 3. Create Python virtual environment
This project includes a Python script that generates the server code.
To run it, you need to create and activate a virtual environment:

```bash
python3 -m venv env
```

Activate virtual environments:

- **On macOS/Linux**:
 ```bash
source env/bin/activate
 ``` 

 - **On Windows**:
```bash
env/bin/activate
 ``` 

### 4. Generate the server code
run the script:

```bash
python3 generate.py
 ``` 

During execution, you will be prompted to specify the APIs the server will expose.
Once completed, the script will automatically generate the following files:
- **api-server.json** -> Contains defined API paths and methods.
- **docker-compose.yaml** -> Configures the server deployment with Docker.


### 5. Starting the server
After generating the files, you can start the server by running:
```bash
docker compose up --build
 ``` 