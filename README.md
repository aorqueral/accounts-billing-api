# Accounts & Billing API
🚧 En construcción (Semana 1)

API en **Django/DRF** para gestión de:
- Autenticación con JWT
- Clientes
- Planes y suscripciones
- Facturación mock (invoices)
- Export CSV

## 🚀 Stack
- Django 5 + DRF
- PostgreSQL (Docker)
- JWT (SimpleJWT)
- Tests con pytest
- Docker Compose
- CI/CD (GitHub Actions en progreso)

## ▶️ Cómo correr
```bash
# levantar servicios
docker compose up -d --build

# migraciones iniciales
docker compose exec web python manage.py migrate

# crear superusuario (opcional)
docker compose exec web python manage.py createsuperuser

# probar endpoint de salud
curl http://localhost:8000/health/
```

## 📂 Estructura inicial
```
accounts_billing_api/
  apps/
    accounts/      # auth, roles
    customers/     # clientes
    billing/       # planes, subscripciones, invoices
  config/          # settings, urls
  docker/          # dockerfile y config
  tests/
```

## ✅ Estado
- [x] Config base Django + DRF + Docker
- [x] Endpoint `/health`
- [ ] Modelos de Customers y Plans
- [ ] JWT + roles
- [ ] Tests de integración
- [ ] CI/CD con GitHub Actions
