# Enterprise B2B Auth & Policy Service

A high-performance microservice for authentication and authorization supporting **Multi-tenancy**, **RBAC** (Role-Based Access Control), and dynamic **ABAC** (Attribute-Based Access Control).

## 🚀 Key Features

* **Multi-Tenancy:** Complete tenant isolation at the database schema level.
* **Hybrid Auth Engine:** 
  * **RBAC:** Fine-grained permissions (`invoices:approve`, `roles:write`).
  * **ABAC:** Dynamic contextual rule evaluation (user department, resource attributes, limits).
* **JWT Security:** Stateless tokens using HS256 with expiration and custom claims.
* **Alembic Migrations:** Database schema versioning with PostgreSQL.
* **Containerized:** Ready-to-use Docker and Docker Compose environment.

---

## 🛠 Tech Stack

* **Language:** Python 3.11+
* **Framework:** FastAPI
* **Database:** PostgreSQL + SQLAlchemy 2.0
* **Migrations:** Alembic
* **Security:** PyJWT, Passlib (bcrypt)
* **DevOps:** Docker, Docker Compose

---

## 🏁 Quick Start

### 1. Environment Setup
Create a `.env` file in the project root:
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres_b2b_password
POSTGRES_DB=enterprise_auth_db
DATABASE_URL=postgresql://postgres:postgres_b2b_password@db:5432/enterprise_auth_db
SECRET_KEY=super_secret_b2b_key

# Enterprise B2B Auth & Policy Service

Высокопроизводительный микросервис аутентификации и авторизации с поддержкой **Multi-tenancy**, **RBAC** (Role-Based Access Control) и динамического **ABAC** (Attribute-Based Access Control).

## 🚀 Основные возможности

* **Multi-Tenancy:** Полная изоляция клиентов (отделов/компаний) на уровне базы данных.
* **Гибридный Auth Engine:** 
  * **RBAC:** Доступ на основе ролей и атомарных разрешений (`invoices:approve`, `roles:write`).
  * **ABAC:** Динамическая вычисление правил доступа по контексту (атрибуты пользователя, отдела, лимиты суммы).
* **JWT Security:** Выдача подписи токенов через HS256 с тайм-аутом сессии и заявками (claims).
* **Alembic Migrations:** Управление схемой базы данных PostgreSQL без потери данных.
* **Docker Ready:** Полноценный Docker-compose сетап с изоляцией окружения.

---

## 🛠 Стек технологий

* **Language:** Python 3.11+
* **Framework:** FastAPI
* **Database:** PostgreSQL + SQLAlchemy 2.0
* **Migrations:** Alembic
* **Security:** PyJWT, Passlib (bcrypt)
* **Infrastructure:** Docker, Docker Compose

---

## 🏁 Быстрый запуск

### 1. Клонирование и настройка окружения
Создайте файл `.env` в корне проекта (или скопируйте `.env.example`):
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres_b2b_password
POSTGRES_DB=enterprise_auth_db
DATABASE_URL=postgresql://postgres:postgres_b2b_password@db:5432/enterprise_auth_db
SECRET_KEY=super_secret_b2b_key