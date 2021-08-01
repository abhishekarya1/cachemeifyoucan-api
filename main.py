from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Query, Response, status

from hashids import Hashids
from redis import Redis

#custom
import constants
from utils import get_html, validate_link, link_cleaner
from models import ShortlinkResponse, LinkResponse

api = FastAPI()

redis = Redis(host=constants.REDIS_HOST, port=constants.REDIS_PORT, db=0)


#routes
@api.post("/",
          response_model=ShortlinkResponse,
          response_model_exclude_unset=True)
#def gen_shortlink(link: str = Query(..., max_length=50)):  #required query param
def generate_shortlink(response: Response, link: Optional[str] = Query(None, max_length=50)):  #sets link to None if it is not available
    if link is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'msg': 'Please provide a link as query parameter.'}

    if validate_link(link) == False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'msg': 'Invalid link!'}
    else:
      #clean link to get rid of '/' or '?' at the end
        clean_link = link_cleaner(link)

        shortid = None
        #if a shortlink exists
        if redis.hexists('index', clean_link) is True:
            shortid = str(redis.hget('index', clean_link), 'utf-8')
            gen = "Existing shortlink returned."
        else:
            #generate shortid from current timestamp
            hashid = Hashids(salt=constants.HASHID_SALT, min_length=4)
            shortid = hashid.encode(int(datetime.today().timestamp()))

            #store field-value pair to key/hash(index) in Redis
            redis.hset('index', clean_link, shortid)
            redis.hset('Sindex', shortid, clean_link)
            gen = "New shortlink generated."

        #append shortid to baseUrl
        shortlink = constants.BASE_URL + "/" + shortid

        #send shortlink in response
        response.status_code = status.HTTP_201_CREATED
        return {'msg': gen, 'shortlink': shortlink}


@api.get("/{shortid}",
         response_model=LinkResponse,
         response_model_exclude_unset=True)
def expand_shortlink(shortid, response: Response):
    #if user provided invalid shorlink; not found in any hash keys
    link = redis.hget('Sindex', shortid)
    if link is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'msg': 'Invalid shortlink!'}
    else:
        response.status_code = status.HTTP_200_OK
        return {'msg': 'Link fetched from datastore.', 'link': link}