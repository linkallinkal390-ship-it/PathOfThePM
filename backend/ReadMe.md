🔐 Аутентификация


1. Регистрация



### curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123",
    "first_name": "Иван",
    "sur_name": "Иванов"
  }'
###



### ### 2. Логин (получение токена)
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
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


