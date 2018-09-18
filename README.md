Learn you some Elasticsearch!
=============================

Hey there! This is Learn You Some Elasticsearch! This tutorial is for you if you've got some programming experience and if you're not too familiar with Elasticsearch (v5.6.11). It can still be useful if you're too good for that, as this tutorial progressively goes into more and more advanced topics.

If you prefer the soft touch of paper, the delicious smell of a real book, the possibility to physically hug a document, or just want to boast by padding your bookcase, you're out of luck!

If you want to contact me, check out my twitter account, find me on #apoclyps.

So what's Elasticsearch?
------------------------

> Elasticsearch is an open-source, broadly-distributable, readily-scalable, enterprise-grade search engine. Accessible through an extensive and elaborate API, Elasticsearch can power extremely fast searches that support your data discovery applications.

It is easy to get going with Elasticsearch. It ships with sensible defaults and hides complex search and distribution mechanics from beginners. It works quite well, right out of the box. With a short learning curve for grasping the basics, you can become productive very quickly.

Prerequisites
-------------

-	[Docker](https://www.docker.com/)
-	[JQ](https://stedolan.github.io/jq/)

Tutorials
---------

-	[Setup](docs/setup.md)
-	[Indices](docs/indexing.md)
-	[Searching](docs/searching.md)
-	[Filtering](docs/filtering.md)
-	[What's Next](docs/next.md)

Just want to start using it?
----------------------------

Running this command will start Elasticsearch in the background:

```sh
docker-compose up -d
```

Once the service has been started and is accessible on http://localhost:9200, you begin loading data into the service:

```sh
./scripts/load.sh
```

### Adapted from the following resources

-	[Elasticsearch 101](http://joelabrahamsson.com/elasticsearch-101/)
-	[Elasticsearch Docs - v5.6](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)
