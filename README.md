# ✈️ Airport Management API  
**REST API for flight booking system with JWT authentication & Docker deployment**  

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)  
![DRF](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)  
![Postgres](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)  
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)  
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)  
![AutoAdmin](https://img.shields.io/badge/Auto_Admin-38B2AC?style=for-the-badge&logo=robotframework&logoColor=white)

## 📌 Key Features  
- **Flight & Route Management** (Countries → Cities → Airports)  
- **Airline/Aircraft CRUD** with media uploads  
- **Booking System** with seat availability checks  
- **JWT Authentication** for passengers/staff  
- **Real-time Status Updates** (Scheduled/Delayed/Canceled)  
- **Swagger Documentation** with OpenAPI 3.0  

---

## 🛠 Tech Stack  
| Layer          | Technology                          |
|----------------|-------------------------------------|
| **Backend**    | Django 4.2 + Django REST Framework  |
| **Database**   | PostgreSQL 15 (with PostGIS-ready)  |
| **Auth**       | JWT (Access/Refresh tokens)         |
| **Deployment** | Docker + Docker Compose             |
| **Docs**       | Swagger/Redoc                       |

---

## 🗄 Database Structure  
![DB Diagram](./docs/db_diagram.svg)

--- 

## 🚀 How to run locally?

1. **Clone the repository**:
   ```bash
   git@github.com:Sotnikov-100/airport-api-service.git && cd airport-api-service
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   ```

3. **Start containers**:
   ```bash
   docker-compose up --build -d
   ```

--- 

## 💡 Why This Project?
- **Production-Ready**: Dockerized with PostgreSQL optimization
- **Extensible: Ready** for payment gateways/notifications
- **Modern**: JWT auth, DRF serializers, nested routers
- **Perfect Portfolio Piece**: Demonstrates complex data modeling

---

### 👉 Contributions welcome! Submit PRs or feature requests.
