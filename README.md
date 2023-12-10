# Musical History Quiz App

## Author : 
- **김영후 (Kim Young Hoo)**

## Project Description : 
(TODO : should add an image or something here)
- A web application that provides a service of solving `Quizzes` related to `musical histories`.
- (TODO) Provides a `OAuth 2.0` login service so that a user can review their stats.
- (TODO) Provieds a dashboard of user's ranking.


## Purpose of this Project : 
- To *desperately* prove that I can implement `DRF Server` so that I can find a *proper* job.
## Data I Used : 
- Quizzes created by `ChatGPT 3.5`.
- To see the prompt I made, you can navigate and see `/data/prompt.txt`.

```json  
An example of data : 
  {
    "quiz": "Who was the lead guitarist for the rock band Queen?",
    "difficulty": "Easy",
    "genre": "Rock",
    "options": {
      "1": "Brian May",
      "2": "Jimmy Page",
      "3": "Eric Clapton",
      "4": "Jimi Hendrix"
    },
    "answer": "1",
    "explanation": "Brian May served as the lead guitarist for the legendary rock band Queen, contributing to their distinctive sound."
  }
```
## Implemenetation :
- Backend : `Django Rest Framework (DRF)`
- Database : `Sqlite3`
- Frontend : `React`
- Deployment : `Docker`

## (TODO) To Run  : 
- if you have docker installed,
 ```bash
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