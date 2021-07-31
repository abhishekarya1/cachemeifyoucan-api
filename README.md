# 📓 cachemeifyoucan! API Doc
Simple, powerful and efficient link shortener API.

<span style="display:inline-block;">
<img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="400px"> &emsp;&ensp;&emsp;&ensp;&emsp;
<img src="https://upload.wikimedia.org/wikipedia/en/6/6b/Redis_Logo.svg" width="295px">
</span>

### Built With
- [FastAPI](https://flask.palletsprojects.com/en/2.0.x/)

### API Endpoints
```http
POST /?link=https://www.example.org
```
| Parameter | Type | Description |
|  :---: | :---: | :---: |
| `link` | `string` | **Required**. Proper URL String. |

```json
{
	"msg":  "New shortlink generated.",
	"shortlink":  "http://localhost:8000/770r9Lg"
}
```

---
```http
GET /xDFr8a
```

```json
{
	"msg": "Link fetched from datastore.",
	"link":  "https://www.example.org"
}
```

### Status Codes

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |

### Run on local
```sh
$ uvicorn app:api --reload
```
### Heroku Setup
```sh
$ heroku apps
$ heroku git:remote -a cachemeifyoucan-api 	#run in git repo
```
#### Monitoring
```sh
$ heroku redis:info
$ heroku redis:maxmemory redis_instance_name --policy allkeys-lru
``` 

```sh
$ heroku redis:cli
$ flushall
```
### References
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [validators library](https://pypi.org/project/validators/)

### Acknowledgements
- [DIDN'T WORK in Python - Regex for URL matching](https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url)
- [Deploy FastAPI to Heroku](https://towardsdatascience.com/how-to-deploy-your-fastapi-app-on-heroku-for-free-8d4271a4ab9)
- [Repo for above](https://github.com/shinokada/fastapi-drag-and-drop)
- [Linking redis on Heroku](https://devcenter.heroku.com/articles/heroku-redis#connecting-in-python)
