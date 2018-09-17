Searching
=========

```json
curl -XPOST "http://localhost:9200/_search" -d '
{
  "query": {
    "match_all": {}
  }
}'
```

Searching So, we've covered the basics of working with data in an ElasticSearch index and it's time to move on to more exciting things - searching. However, considering the last thing we did was to delete the only document we had from our index we'll first need some sample data. Below is a number of indexing requests that we'll use.

```json
curl -XPUT "http://localhost:9200/events/event/09f469cc-3d93-4bf2-b07f-2bcaf47d9ca2" -d'
{
    "category": "ElasticSearch Training",
    "created": "2018-09-17T09:00:00",
    "deleted": null,
    "description": "A introduction to ElasticSearch by example",
    "duration": 10000,
    "end": "2018-09-17T09:30:00",
    "entry": [
      {
        "description": null,
        "id": "6e58dda0-8913-4387-8954-1a1dba9003b8",
        "type": "free"
      }
    ],
    "id": "09f469cc-3d93-4bf2-b07f-2bcaf47d9ca2",
    "meetup": [],
    "name": "Learn by Example",
    "source": "meetup",
    "start": "2018-09-17T09:00:00",
    "topics": [],
    "updated": "2018-09-17T09:00:00",
    "url": "https://www.meetup.com/learn-by-example"
  }'
```

It's worth pointing out that ElasticSearch has and endpoint `_bulk` for indexing multiple documents with a single request however that's out of scope for this tutorial so we're keeping it simple and using individual requests.

The `_search` endpoint
======================

Now that we have put some events into our index, let's see if we can find them again by searching. In order to search with ElasticSearch we use the `_search` endpoint, optionally with an index and type. That is, we make requests to an URL following this pattern: `<index>/<type>/_search` where index and type are both optional.

In other words, in order to search for our events we can make POST requests to either of the following URLs:

http://localhost:9200/_search - Search across all indexes and all types. http://localhost:9200/events/_search - Search across all types in the events index. http://localhost:9200/events/event/_search - Search explicitly for documents of type event within the events index. As we only have a single index and a single type which one we use doesn't matter. We'll use the first URL for the sake of brevity.

Search request body and ElasticSearch's query DSL If we simply send a request to one of the above URL's we'll get all of our events back. In order to make a more useful search request we also need to supply a request body with a query. The request body should be a JSON object which, among other things, can contain a property named "query" in which we can use ElasticSearch's query DSL.

```json
{
    "query": {

    }
}
```

One may wonder what the query DSL is. It's ElasticSearch's own domain specific language based on JSON in which queries and filters can be expressed. Think of it like ElasticSearch's equivalent of SQL for a relational database. Here's part of how ElasticSearch's own documentation explains it:

Think of the Query DSL as an AST of queries. Certain queries can contain other queries (like the bool query), other can contain filters (like the constant_score), and some can contain both a query and a filter (like the filtered). Each of those can contain any query of the list of queries or any filter from the list of filters, resulting in the ability to build quite complex (and interesting) queries. Basic free text search The query DSL features a long list of different types of queries that we can use. For "ordinary" free text search we'll most likely want to use one called "query string query".

A query string query is an advanced query with a lot of different options that ElasticSearch will parse and transform into a tree of simpler queries. Still, it can be very easy to use if we ignore all of its optional parameters and simply feed it a string to search for.

Let's try a search for the word "python" which is present in the title of two of our events:

```json
curl -XPOST "http://localhost:9200/_search" -d'
{
    "query": {
        "query_string": {
            "query": "python"
        }
    }
}'
```

Let's execute the request and take a look at the result.

As expected we're getting two hits, one for each of the events with the word "python" in the title. Let's look at another scenario, searching in specific fields.

Specifying fields to search in In the previous example we used a very simple query, a query string query with only a single property, "query". As mentioned before the query string query has a number of settings that we can specify and if we don't it will use sensible default values.

One such setting is called "fields" and can be used to specify a list of fields to search in. If we don't use that the query will default to searching in a special field called `_all` that ElasticSearch automatically generates based on all of the individual fields in a document.

Let's try to search for events only by title. That is, if we search for "Challenge" we want to get a hit for "Code Co-op: Halloween Cyber-Security Challenge" but not for any events that do not contain challenge in the description.

In order to do that we modify the previous search request body so that the query string query has a fields property with an array of fields we want to search in:

```json
curl -XPOST "http://localhost:9200/_search" -d'
{  
   "query":{  
      "query_string":{  
         "query":"Challenge",
         "fields":[  
            "description"
         ]
      }
   }
 }'
```

As expected we get several hits, events with the word "Challenge" in their descriptions.

<span style="float: left;">[Previous: Indexing](indexing.md)</span>

<span style="float: right;">[Next: Filtering](filtering.md)</span>
