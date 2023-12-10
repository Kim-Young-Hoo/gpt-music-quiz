# Musical History Quiz App

### Author : 
- **김영후 (Kim Young Hoo)**

### Project Description : 
(TODO : should add an image or something here)
- A web application that provides a service of solving `Quizzes` related to `musical histories`.
- (TODO) Provides a `OAuth 2.0` login service so that a user can review their stats.
- (TODO) Provieds a dashboard of user's ranking.


### Purpose of this Project : 
- To *desperately* prove that I can implement `DRF Server` so that I can find a _proper_ job.
### Data I Used : 
- Quizzes created by `ChatGPT 3.5`.
- To see the prompt I made, you can navigate and see `/data/prompt.txt`.
- Data Example : 
```   
{
    "quiz": "Which Beatles album is often considered one of the greatest of all time?",
    "difficulty": "Medium",
    "genre": "Rock",
    "options": {
      "1": "Abbey Road",
      "2": "Sgt. Pepper's Lonely Hearts Club Band",
      "3": "Revolver",
      "4": "The White Album"
    },
    "answer": "2",
    "explanation": "Sgt. Pepper's Lonely Hearts Club Band is frequently regarded as one of the greatest albums in the history of music, with its innovative production and eclectic sound."
}
```
### Implemenetation :
- Backend : `Django Rest Framework (DRF)`
- Database : `Sqlite3`
- Frontend : `React`
- Deployment : `Docker`

### (TODO) To Run  : 
- if you have docker installed,
 ```
 $ docker build . 
 $ docker ` ...
 ```
 and then go localhost blahblah

- if not, 
```
asdfasdf
```

### (TODO) APIs :
- 