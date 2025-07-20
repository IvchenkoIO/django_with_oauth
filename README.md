# Disclaimer: This README is a guide on how to set up the project. For more information on how everything works, there are multiple others README files in the different server folders. Also there are comments throughout the code and files including documentations on the tests that were done.

## Prerequisites

1. **Install Docker Desktop**  
   [Download Docker](https://www.docker.com)  
   > *Note: You do not need to create a Docker account. In fact should there be problems, it can help to log out from your account*

2. **Install Windows Subsystem for Linux (WSL)**  
   Follow the [WSL Installation Guide](https://learn.microsoft.com/en-us/windows/wsl/install) if you haven't already.

3. **Check out git repository**  
    [django oauth project](https://github.com/IvchenkoIO/django_with_oauth)  

---

## Setup Instructions

1. **Open a terminal and navigate to the project folder:**
   ```
   cd path/to/django_with_oauth
   ```

2. **Build and run the Docker containers:**

   ```
   docker-compose up --build
   ```

3. **In a second terminal window, navigate to the same folder and run the following commands:**

   ```
   docker-compose exec resource_server python manage.py makemigrations
   docker-compose exec resource_server python manage.py migrate
   docker-compose exec resource_server python manage.py seed_photos
   ```

---

## 🌐 Access the Web Application

1. Open your browser and go to:  
   👉 [https://privacyengproj.ngrok.app/client/](https://privacyengproj.ngrok.app/client/)

2. **Press `Login`**

3. **Choose Your Preferred Privacy Levels:**

   - **Numerical:** `None`, `Hourly`, `8-Hourly`, `Daily`
   - **Images:** `None`, `Mild`, `Medium`, `Heavy`
   - **Text:** `None`, `Anonymize`, `Remove`

4. **Click `Continue`**

5. **Authenticate with the following credentials:**

   - **Username:** `test_1`  
   - **Password:** `rootroot`

6. **Click `Login` and then `Authorize`**

---

## Result

The data will now be served with the selected **privacy transformations** applied.
