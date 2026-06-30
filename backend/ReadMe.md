# API Documentation

Base URL: `http://localhost:8000`
---

## Auth

### Регистрация
```bash
curl -X POST http://localhost:8000/api/auth/register/ -H "Content-Type: application/json" -d "{\"email\": \"userqwe@example.com\", \"password\": \"password123\", \"first_name\": \"Ivan\", \"sur_name\": \"Ivanov\", \"role\": \"user\"}"
```

**Ответ:**
```json
{
  "message": "Пользователь зарегистрирован",
  "data": {
    "id": "uuid",
    "email": "userqwe@example.com",
    "role": "user",
    "first_name": "Ivan",
    "sur_name": "Ivanov"
  }
}
```

### Логин
```bash
curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d "{\"email\": \"userqwe@example.com\", \"password\": \"password123\"}"
```

**Ответ:**
```json
{
  "message": "Успешная авторизация",
  "data": {
    "token": "b083cb41b65671d2733873ba4b459a528c94f91a"
  }
}
```

---

## Results

### GET — Список результатов
```bash
curl http://localhost:8000/api/results/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

**Ответ:**
```json
{
  "message": "данные успешно получены",
  "total_count": 2,
  "total_pages": 1,
  "current_page": 1,
  "data": [
    {
      "id": "17227dd8-c25d-41a5-b4b5-a8d3ff57a17c",
      "finalConstructionDate": "2026-06-19T13:05:38.685371Z",
      "CountCompletedQuest": 32767,
      "reputation": 32767,
      "evaluationGraphConstruction": 32767,
      "budget": "5502312.00",
      "office_health": 32767
    }
  ]
}
```

### POST — Создать результат
```bash
curl -X POST http://localhost:8000/api/results/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"CountCompletedQuest\": 5, \"reputation\": 80, \"evaluationGraphConstruction\": 90, \"budget\": \"15000.00\", \"office_health\": 75}"
```

**Ответ:**
```json
{
  "success": true,
  "message": "Result created successfully",
  "data": {
    "id": "a5a845d5-861a-45ee-b0b1-b5bf8b08a6ea",
    "finalConstructionDate": "2026-06-25T16:38:04.921211Z",
    "CountCompletedQuest": 5,
    "reputation": 80,
    "evaluationGraphConstruction": 90,
    "budget": "15000.00",
    "office_health": 75
  }
}
```

### GET — Результат по ID
```bash
curl http://localhost:8000/api/results/a5a845d5-861a-45ee-b0b1-b5bf8b08a6ea/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### PUT — Полное обновление результата
```bash
curl -X PUT http://localhost:8000/api/results/a5a845d5-861a-45ee-b0b1-b5bf8b08a6ea/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"CountCompletedQuest\": 5, \"reputation\": 90, \"evaluationGraphConstruction\": 85, \"budget\": \"20000.00\", \"office_health\": 70}"
```

### PATCH — Частичное обновление результата
```bash
curl -X PATCH http://localhost:8000/api/result/a5a845d5-861a-45ee-b0b1-b5bf8b08a6ea/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"reputation\": 95}"
```

### DELETE — Удалить результат
```bash
curl -X DELETE http://localhost:8000/api/results/a5a845d5-861a-45ee-b0b1-b5bf8b08a6ea/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

---

## Sessions

### GET — Список сессий
```bash
curl http://localhost:8000/api/sessions/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### POST — Создать сессию
```bash
curl -X POST http://localhost:8000/api/sessions/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"user\": \"USER_UUID\", \"result\": \"a5a845d5-861a-45ee-b0b1-b5bf8b08a6ea\", \"start_date\": \"2025-01-01\", \"end_date\": \"2025-01-31\"}"
```

### GET — Сессия по ID
```bash
curl http://localhost:8000/api/sessions/SESSION_UUID/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### PUT — Полное обновление сессии
```bash
curl -X PUT http://localhost:8000/api/sessions/SESSION_UUID/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"user\": \"USER_UUID\", \"result\": \"a5a845d5-861a-45ee-b0b1-b5bf8b08a6ea\", \"start_date\": \"2025-01-01\", \"end_date\": \"2025-03-31\"}"
```

### PATCH — Частичное обновление сессии
```bash
curl -X PATCH http://localhost:8000/api/sessions/SESSION_UUID/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"end_date\": \"2025-03-31\"}"
```

### DELETE — Удалить сессию
```bash
curl -X DELETE http://localhost:8000/api/sessions/SESSION_UUID/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### GET — Детали сессии
```bash
curl http://localhost:8000/api/sessions/SESSION_UUID/details/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### POST — Продлить сессию
```bash
curl -X POST http://localhost:8000/api/sessions/SESSION_UUID/extend/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"new_end_date\": \"2025-06-30\"}"
```

### GET — Сессии за период
```bash
curl "http://localhost:8000/api/sessions/by_date_range/?from_date=2025-01-01&to_date=2025-12-31" -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### GET — Мои сессии
```bash
curl http://localhost:8000/api/sessions/my_sessions/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

---

## Users

### GET — Список пользователей
```bash
curl http://localhost:8000/api/users/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### POST — Создать пользователя
```bash
curl -X POST http://localhost:8000/api/users/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"email\": \"new@example.com\", \"password\": \"password123\", \"first_name\": \"Petr\", \"sur_name\": \"Petrov\", \"role\": \"user\"}"
```

### GET — Пользователь по ID
```bash
curl http://localhost:8000/api/users/USER_UUID/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### PUT — Полное обновление пользователя
```bash
curl -X PUT http://localhost:8000/api/users/USER_UUID/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"email\": \"updated@example.com\", \"password\": \"password123\", \"first_name\": \"Petr\", \"sur_name\": \"Petrov\", \"role\": \"user\"}"
```

### PATCH — Частичное обновление пользователя
```bash
curl -X PATCH http://localhost:8000/api/users/USER_UUID/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"first_name\": \"Newname\"}"
```

### DELETE — Удалить пользователя
```bash
curl -X DELETE http://localhost:8000/api/users/USER_UUID/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### GET — Текущий пользователь (me)
```bash
curl http://localhost:8000/api/users/me/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

---

## Фильтры и параметры

### Users — фильтрация
```bash
# По роли
curl "http://localhost:8000/api/users/?role=admin" -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"

# Только активные
curl "http://localhost:8000/api/users/?is_active=true" -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"

# Поиск по имени / email
curl "http://localhost:8000/api/users/?search=ivan" -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### Results — фильтрация
```bash
curl "http://localhost:8000/api/results/?reputation=80&office_health=75" -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### Sessions — фильтрация
```bash
curl "http://localhost:8000/api/sessions/?start_date=2025-01-01&end_date=2025-12-31" -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

---
> **Примечание:** `SESSION_UUID` и `USER_UUID` нужно заменить на реальные UUID из базы.
> UUID результата из примеров: `a5a845d5-861a-45ee-b0b1-b5bf8b08a6ea`