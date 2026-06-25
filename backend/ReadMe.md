🔐 Аутентификация


1. Регистрация



### curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "userqwe@example.com",
    "password": "securepass123",
    "first_name": "Иван",
    "sur_name": "Иванов"
  }'
###



### ### 2. Логин (получение токена)
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "userqwe@example.com",
    "password": "securepass123"
  }'


Сохрани полученный token — он нужен для всех остальных запросов:
TOKEN="полученный_токен"







### 👤 Users




### 3. Список пользователей (с фильтрацией и пагинацией)
curl -X GET "http://localhost:8000/api/auht/merinda/users/?role=user&is_active=true&search=иван&ordering=email&page=1" \
  -H "Authorization: Token $TOKEN"




### 4. Получить пользователя по ID
curl -X GET "http://localhost:8000/api/auht/merinda/users/{user_id}/" \
  -H "Authorization: Token $TOKEN"




### 5. Создать пользователя
bash
curl -X POST http://localhost:8000/api/auht/merinda/users/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "pass12345",
    "first_name": "Петр",
    "sur_name": "Петров",
    "role": "user"
  }'




### 6. Обновить пользователя (полное обновление)
curl -X PUT "http://localhost:8000/api/auht/merinda/users/{user_id}/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "updated@example.com",
    "first_name": "Петр",
    "sur_name": "Петров",
    "role": "user",
    "is_active": true
  }'




### 7. Частично обновить пользователя
curl -X PATCH "http://localhost:8000/api/auht/merinda/users/{user_id}/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Пётр"
  }'




### 8. Удалить пользователя
curl -X DELETE "http://localhost:8000/api/auht/merinda/users/{user_id}/" \
  -H "Authorization: Token $TOKEN"




### 9. Получить текущего пользователя (/me)
curl -X GET "http://localhost:8000/api/auht/merinda/users/me/" \
  -H "Authorization: Token $TOKEN"




### 📊 Results




### 10. Список результатов (с фильтрацией)
curl -X GET "http://localhost:8000/api/auht/merinda/results/?reputation=50&office_health=80&ordering=-budget&page=1" \
  -H "Authorization: Token $TOKEN"




### 11. Получить результат по ID
curl -X GET "http://localhost:8000/api/auht/merinda/results/{result_id}/" \
  -H "Authorization: Token $TOKEN"




### 12. Создать результат
curl -X POST http://localhost:8000/api/auht/merinda/results/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reputation": 50,
    "office_health": 80,
    "evaluationGraphConstruction": 5,
    "budget": "150000.00",
    "CountCompletedQuest": 3
  }'




### 13. Обновить результат (полное)
curl -X PUT "http://localhost:8000/api/auht/merinda/results/{result_id}/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reputation": 75,
    "office_health": 90,
    "evaluationGraphConstruction": 7,
    "budget": "200000.00",
    "CountCompletedQuest": 5
  }'



### 
### 14. Частично обновить результат
curl -X PATCH "http://localhost:8000/api/auht/merinda/results/{result_id}/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "budget": "175000.00"
  }'




### 15. Удалить результат

curl -X DELETE "http://localhost:8000/api/auht/merinda/results/{result_id}/" \
  -H "Authorization: Token $TOKEN"




### 16. Статистика результата (/stats)

curl -X GET "http://localhost:8000/api/auht/merinda/results/{result_id}/stats/" \
  -H "Authorization: Token $TOKEN"




📅 Sessions




### 17. Список сессий (с фильтрацией)

curl -X GET "http://localhost:8000/api/auht/merinda/sessions/?user_id={user_id}&result_id={result_id}&start_date=2024-01-01&end_date=2024-12-31&ordering=-start_date&page=1" \
  -H "Authorization: Token $TOKEN"




### 18. Получить сессию по ID

curl -X GET "http://localhost:8000/api/auht/merinda/sessions/{session_id}/" \
  -H "Authorization: Token $TOKEN"




### 19. Создать сессию

curl -X POST http://localhost:8000/api/auht/merinda/sessions/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "{user_id}",
    "result": "{result_id}",
    "start_date": "2024-06-01",
    "end_date": "2024-06-30"
  }'




### 20. Обновить сессию (полное)

curl -X PUT "http://localhost:8000/api/auht/merinda/sessions/{session_id}/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "{user_id}",
    "result": "{result_id}",
    "start_date": "2024-07-01",
    "end_date": "2024-07-31"
  }'

  


### 21. Частично обновить сессию

curl -X PATCH "http://localhost:8000/api/auht/merinda/sessions/{session_id}/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "end_date": "2024-08-15"
  }'




### 22. Удалить сессию

curl -X DELETE "http://localhost:8000/api/auht/merinda/sessions/{session_id}/" \
  -H "Authorization: Token $TOKEN"




### 23. Детали сессии (/details)

curl -X GET "http://localhost:8000/api/auht/merinda/sessions/{session_id}/details/" \
  -H "Authorization: Token $TOKEN"




### 24. Мои сессии (/my_sessions)

curl -X GET "http://localhost:8000/api/auht/merinda/sessions/my_sessions/?page=1" \
  -H "Authorization: Token $TOKEN"




### 25. Сессии по диапазону дат (/by_date_range)

curl -X GET "http://localhost:8000/api/auht/merinda/sessions/by_date_range/?from_date=2024-01-01&to_date=2024-12-31&page=1" \
  -H "Authorization: Token $TOKEN"




26. Продлить сессию (/extend)

curl -X POST "http://localhost:8000/api/auht/merinda/sessions/{session_id}/extend/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "new_end_date": "2024-09-30"
  }'



📋 Итоговый список ручек (25 штук)



#	Метод	URL



1	POST	/api/auth/register/



2	POST	/api/auth/login/



3	GET	/api/auht/merinda/users/



4	GET	/api/auht/merinda/users/{id}/



5	POST	/api/auht/merinda/users/



6	PUT	/api/auht/merinda/users/{id}/



7	PATCH	/api/auht/merinda/users/{id}/



8	DELETE	/api/auht/merinda/users/{id}/



9	GET	/api/auht/merinda/users/me/



10	GET	/api/auht/merinda/results/



11	GET	/api/auht/merinda/results/{id}/



12	POST	/api/auht/merinda/results/



13	PUT	/api/auht/merinda/results/{id}/



14	PATCH	/api/auht/merinda/results/{id}/



15	DELETE	/api/auht/merinda/results/{id}/



16	GET	/api/auht/merinda/sessions/



17	GET	/api/auht/merinda/sessions/{id}/



18	POST	/api/auht/merinda/sessions/



19	PUT	/api/auht/merinda/sessions/{id}/



20	PATCH	/api/auht/merinda/sessions/{id}/



21	DELETE	/api/auht/merinda/sessions/{id}/



22	GET	/api/auht/merinda/sessions/{id}/details/



23	GET	/api/auht/merinda/sessions/my_sessions/



24	GET	/api/auht/merinda/sessions/by_date_range/



25	POST	/api/auht/merinda/sessions/{id}/extend/










# API Documentation

Base URL: `http://localhost:8000`

Token: `b083cb41b65671d2733873ba4b459a528c94f91a`

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
curl http://localhost:8000/api/auht/merinda/results/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
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
curl -X POST http://localhost:8000/api/auht/merinda/results/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"CountCompletedQuest\": 5, \"reputation\": 80, \"evaluationGraphConstruction\": 90, \"budget\": \"15000.00\", \"office_health\": 75}"
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
curl http://localhost:8000/api/auht/merinda/results/a5a845d5-861a-45ee-b0b1-b5bf8b08a6ea/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### PUT — Полное обновление результата
```bash
curl -X PUT http://localhost:8000/api/auht/merinda/results/a5a845d5-861a-45ee-b0b1-b5bf8b08a6ea/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"CountCompletedQuest\": 5, \"reputation\": 90, \"evaluationGraphConstruction\": 85, \"budget\": \"20000.00\", \"office_health\": 70}"
```

### PATCH — Частичное обновление результата
```bash
curl -X PATCH http://localhost:8000/api/auht/merinda/results/a5a845d5-861a-45ee-b0b1-b5bf8b08a6ea/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"reputation\": 95}"
```

### DELETE — Удалить результат
```bash
curl -X DELETE http://localhost:8000/api/auht/merinda/results/a5a845d5-861a-45ee-b0b1-b5bf8b08a6ea/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

---

## Sessions

### GET — Список сессий
```bash
curl http://localhost:8000/api/auht/merinda/sessions/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### POST — Создать сессию
```bash
curl -X POST http://localhost:8000/api/auht/merinda/sessions/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"user\": \"USER_UUID\", \"result\": \"a5a845d5-861a-45ee-b0b1-b5bf8b08a6ea\", \"start_date\": \"2025-01-01\", \"end_date\": \"2025-01-31\"}"
```

### GET — Сессия по ID
```bash
curl http://localhost:8000/api/auht/merinda/sessions/SESSION_UUID/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### PUT — Полное обновление сессии
```bash
curl -X PUT http://localhost:8000/api/auht/merinda/sessions/SESSION_UUID/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"user\": \"USER_UUID\", \"result\": \"a5a845d5-861a-45ee-b0b1-b5bf8b08a6ea\", \"start_date\": \"2025-01-01\", \"end_date\": \"2025-03-31\"}"
```

### PATCH — Частичное обновление сессии
```bash
curl -X PATCH http://localhost:8000/api/auht/merinda/sessions/SESSION_UUID/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"end_date\": \"2025-03-31\"}"
```

### DELETE — Удалить сессию
```bash
curl -X DELETE http://localhost:8000/api/auht/merinda/sessions/SESSION_UUID/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### GET — Детали сессии
```bash
curl http://localhost:8000/api/auht/merinda/sessions/SESSION_UUID/details/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### POST — Продлить сессию
```bash
curl -X POST http://localhost:8000/api/auht/merinda/sessions/SESSION_UUID/extend/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"new_end_date\": \"2025-06-30\"}"
```

### GET — Сессии за период
```bash
curl "http://localhost:8000/api/auht/merinda/sessions/by_date_range/?from_date=2025-01-01&to_date=2025-12-31" -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### GET — Мои сессии
```bash
curl http://localhost:8000/api/auht/merinda/sessions/my_sessions/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

---

## Users

### GET — Список пользователей
```bash
curl http://localhost:8000/api/auht/merinda/users/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### POST — Создать пользователя
```bash
curl -X POST http://localhost:8000/api/auht/merinda/users/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"email\": \"new@example.com\", \"password\": \"password123\", \"first_name\": \"Petr\", \"sur_name\": \"Petrov\", \"role\": \"user\"}"
```

### GET — Пользователь по ID
```bash
curl http://localhost:8000/api/auht/merinda/users/USER_UUID/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### PUT — Полное обновление пользователя
```bash
curl -X PUT http://localhost:8000/api/auht/merinda/users/USER_UUID/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"email\": \"updated@example.com\", \"password\": \"password123\", \"first_name\": \"Petr\", \"sur_name\": \"Petrov\", \"role\": \"user\"}"
```

### PATCH — Частичное обновление пользователя
```bash
curl -X PATCH http://localhost:8000/api/auht/merinda/users/USER_UUID/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a" -H "Content-Type: application/json" -d "{\"first_name\": \"Newname\"}"
```

### DELETE — Удалить пользователя
```bash
curl -X DELETE http://localhost:8000/api/auht/merinda/users/USER_UUID/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### GET — Текущий пользователь (me)
```bash
curl http://localhost:8000/api/auht/merinda/users/me/ -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

---

## Фильтры и параметры

### Users — фильтрация
```bash
# По роли
curl "http://localhost:8000/api/auht/merinda/users/?role=admin" -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"

# Только активные
curl "http://localhost:8000/api/auht/merinda/users/?is_active=true" -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"

# Поиск по имени / email
curl "http://localhost:8000/api/auht/merinda/users/?search=ivan" -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### Results — фильтрация
```bash
curl "http://localhost:8000/api/auht/merinda/results/?reputation=80&office_health=75" -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

### Sessions — фильтрация
```bash
curl "http://localhost:8000/api/auht/merinda/sessions/?start_date=2025-01-01&end_date=2025-12-31" -H "Authorization: Token b083cb41b65671d2733873ba4b459a528c94f91a"
```

---

> **Примечание:** `SESSION_UUID` и `USER_UUID` нужно заменить на реальные UUID из базы.
> UUID результата из примеров: `a5a845d5-861a-45ee-b0b1-b5bf8b08a6ea`