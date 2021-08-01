# 📓 cachemeifyoucan! API Deployment Branch 🛠️

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
$ flushdb
$ quit
-> Ctrl + C
```

[Heroku Datacenter Link](https://data.heroku.com/)

### References
- [Deploy FastAPI to Heroku](https://towardsdatascience.com/how-to-deploy-your-fastapi-app-on-heroku-for-free-8d4271a4ab9)
- [Repo for above](https://github.com/shinokada/fastapi-drag-and-drop)
- [Linking redis on Heroku](https://devcenter.heroku.com/articles/heroku-redis#connecting-in-python)