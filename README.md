A basic flask based restful exchange service.

Starting the Containers:
------------------------

	docker-compose up

Grab and save:
--------------

	curl -d '{"currency":"eur", "amount":122.12345678}' -H "Content-Type: application/json" -X POST http://localhost:8082/grab_and_save

Get last exchange:
------------------

	curl localhost:8082/last

Get last exchange by currency:
------------------------------

	curl localhost:8082/last/eur

Get last n exchanges:
---------------------

	curl localhost:8082/last/3

Get last n exchanges by currency:
---------------------------------

	curl localhost:8082/last/eur/3


To-dos:
-------

1- Write unit tests
2- Set float precision to 8

