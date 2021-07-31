import base64
from datetime import datetime
import urllib.request
from typing import Optional
import os

from fastapi import FastAPI, Query, Response, status

from hashids import Hashids
import redis

#custom
import constants
from utils import get_html, validate_link, link_cleaner
from models import ShortlinkResponse, LinkResponse

api = FastAPI()

r = redis.from_url(os.environ.get("REDIS_URL"))

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
        #scrape text
        webpage = urllib.request.urlopen(link).read()
        html = get_html(webpage)

        #base64encode html content
        b64_code = base64.b64encode(bytes(str(html), 'utf-8'))

        #clean link to get rid of '/' or '?' at the end
        clean_link = link_cleaner(link)

        shortid = None
        #if a shortlink exists
        if r.hexists('index', b64_code) is True:
            shortid = str(r.hget('index', b64_code), 'utf-8')
            gen = "Existing shortlink returned."
        else:
            #generate shortid from current timestamp
            hashid = Hashids(salt=constants.HASHID_SALT, min_length=4)
            shortid = hashid.encode(int(datetime.today().timestamp()))

            #store field-value pair to key/hash(shortid) in Redis
            r.hset(shortid, 'link', clean_link)
            r.hset(shortid, 'b64_code', b64_code)

            #set b64_code-shortid in index hash
            r.hset('index', b64_code, shortid)
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
    if len(r.keys(shortid)) == 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'msg': 'Invalid shortlink!'}
    #print(link_b)
    #print(type(link_b))
    #browser hits twice with GET :/
    else:
        link = str(r.hget(shortid, 'link'), 'utf-8')
        base64code = str(r.hget(shortid, 'b64_code'), 'utf-8')
        #if og_link is up: send og_link in response
        if urllib.request.urlopen(
                link).getcode() == 200:  #changed to != for debug
            response.status_code = status.HTTP_200_OK
            return {'msg': 'Link fetched from datastore.', 'link': link}
        #else: render cached version after decoding
        else:
            cached_html = str(base64.b64decode(base64code), 'utf-8')
            return cached_html
