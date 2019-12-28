# django-rest-api
A django Rest API endpoints to create a key-value store. Currently it support GET, POST, PATCH and DELETE


## Tested on

- OS : Ubunut 16.04 LTS
- Python version: python 3.6

### Packages need to install 
- pip install django==2.1
- pip install djangorestframework==3.11

## How to run

- git clone https://github.com/menon92/django-rest-api
- cd django-rest-api
- python manage.py runserver

Now visite http://127.0.0.1:8000/ and play with this api


# Some test result of this API
If you do not have `curl` just install it by using this command 
```bash
sudo apt-get install curl
```
Now you can use `curl` to make different HTTP requests 
## Make POST request
```bash
$curl -X POST  \
-H "Content-Type: application/json" \
-d '[{"key": "one", "value": "1"}]' \
http://127.0.0.1:8000/values/
```
```json
# response
[
   {
      "id":52,
      "url":"http://127.0.0.1:8000/values/52/",
      "key":"one",
      "value":"1",
      "ttl":"2019-12-28T21:52:11.340804+06:00"
   }
]
```

## Make POST Request request with multiple values
```bash
$curl -X POST  \
-H "Content-Type: application/json" \
-d '[{"key": "two", "value": "2"}, {"key": "three", "value": "3"}]' \
http://127.0.0.1:8000/values/
```
```json
# response
[
   {
      "id":53,
      "url":"http://127.0.0.1:8000/values/53/",
      "key":"two",
      "value":"2",
      "ttl":"2019-12-28T21:52:45.314503+06:00"
   },
   {
      "id":54,
      "url":"http://127.0.0.1:8000/values/54/",
      "key":"three",
      "value":"3",
      "ttl":"2019-12-28T21:52:45.371379+06:00"
   }
]
```

## Make a GET request on all values

```bash 
$curl http://127.0.0.1:8000/values/
```
```json
# response
[
   {
      "id":52,
      "url":"http://127.0.0.1:8000/values/52/",
      "key":"one",
      "value":"1",
      "ttl":"2019-12-28T21:53:33.608204+06:00"
   },
   {
      "id":53,
      "url":"http://127.0.0.1:8000/values/53/",
      "key":"two",
      "value":"2",
      "ttl":"2019-12-28T21:53:33.679996+06:00"
   },
   {
      "id":54,
      "url":"http://127.0.0.1:8000/values/54/",
      "key":"three",
      "value":"3",
      "ttl":"2019-12-28T21:53:33.812879+06:00"
   }
]
```

## Make a GET request on a single value

```bash
$curl http://127.0.0.1:8000/values/52/
```
```json
# response
{
   "id":52,
   "url":"http://127.0.0.1:8000/values/52/",
   "key":"one",
   "value":"1",
   "ttl":"2019-12-28T21:54:12.043945+06:00"
}
```

## Make a GET request on specified values
```bash
$http://127.0.0.1:8000/values/?key=one,three
```
```json
# response
[
   {
      "id":52,
      "url":"http://127.0.0.1:8000/values/52/",
      "key":"one",
      "value":"1",
      "ttl":"2019-12-28T21:54:42.945754+06:00"
   },
   {
      "id":54,
      "url":"http://127.0.0.1:8000/values/54/",
      "key":"three",
      "value":"3",
      "ttl":"2019-12-28T21:54:43.064592+06:00"
   }
]
```

## Make a PATCH request

```bash
$curl -X PATCH \
-H "Content-Type: application/json" \
-d '{"value": "11111"}' \
http://127.0.0.1:8000/values/52/
```
```json
# response
{
   "id":52,
   "url":"http://127.0.0.1:8000/values/52/",
   "key":"one",
   "value":"11111",
   "ttl":"2019-12-28T21:55:35.050087+06:00"
}
```

## GET after TTL expire
```bash
curl http://127.0.0.1:8000/values/
```
```json
[]
```
