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
curl -XPUT "http://localhost:9200/movies/movie/1" -d'
{
    "title": "The Godfather",
    "director": "Francis Ford Coppola",
    "year": 1972,
    "genres": ["Crime", "Drama"]
}'

curl -XPUT "http://localhost:9200/movies/movie/2" -d'
{
    "title": "Lawrence of Arabia",
    "director": "David Lean",
    "year": 1962,
    "genres": ["Adventure", "Biography", "Drama"]
}'

curl -XPUT "http://localhost:9200/movies/movie/3" -d'
{
    "title": "To Kill a Mockingbird",
    "director": "Robert Mulligan",
    "year": 1962,
    "genres": ["Crime", "Drama", "Mystery"]
}'

curl -XPUT "http://localhost:9200/movies/movie/4" -d'
{
    "title": "Apocalypse Now",
    "director": "Francis Ford Coppola",
    "year": 1979,
    "genres": ["Drama", "War"]
}'

curl -XPUT "http://localhost:9200/movies/movie/5" -d'
{
    "title": "Kill Bill: Vol. 1",
    "director": "Quentin Tarantino",
    "year": 2003,
    "genres": ["Action", "Crime", "Thriller"]
}'

curl -XPUT "http://localhost:9200/movies/movie/6" -d'
{
    "title": "The Assassination of Jesse James by the Coward Robert Ford",
    "director": "Andrew Dominik",
    "year": 2007,
    "genres": ["Biography", "Crime", "Drama"]
}'

```

It's worth pointing out that ElasticSearch has and endpoint `_bulk` for indexing multiple documents with a single request however that's out of scope for this tutorial so we're keeping it simple and using six separate requests.

The `_search` endpoint Now that we have put some movies into our index, let's see if we can find them again by searching. In order to search with ElasticSearch we use the `_search` endpoint, optionally with an index and type. That is, we make requests to an URL following this pattern: `<index>/<type>/_search` where index and type are both optional.

In other words, in order to search for our movies we can make POST requests to either of the following URLs:

http://localhost:9200/_search - Search across all indexes and all types. http://localhost:9200/movies/_search - Search across all types in the movies index. http://localhost:9200/movies/movie/_search - Search explicitly for documents of type movie within the movies index. As we only have a single index and a single type which one we use doesn't matter. We'll use the first URL for the sake of brevity.

Search request body and ElasticSearch's query DSL If we simply send a request to one of the above URL's we'll get all of our movies back. In order to make a more useful search request we also need to supply a request body with a query. The request body should be a JSON object which, among other things, can contain a property named "query" in which we can use ElasticSearch's query DSL.

```json
{
    "query": {

    }
}
```

One may wonder what the query DSL is. It's ElasticSearch's own domain specific language based on JSON in which queries and filters can be expressed. Think of it like ElasticSearch's equivalent of SQL for a relational database. Here's part of how ElasticSearch's own documentation explains it:

Think of the Query DSL as an AST of queries. Certain queries can contain other queries (like the bool query), other can contain filters (like the constant_score), and some can contain both a query and a filter (like the filtered). Each of those can contain any query of the list of queries or any filter from the list of filters, resulting in the ability to build quite complex (and interesting) queries. Basic free text search The query DSL features a long list of different types of queries that we can use. For "ordinary" free text search we'll most likely want to use one called "query string query".

A query string query is an advanced query with a lot of different options that ElasticSearch will parse and transform into a tree of simpler queries. Still, it can be very easy to use if we ignore all of its optional parameters and simply feed it a string to search for.

Let's try a search for the word "kill" which is present in the title of two of our movies:

```json
curl -XPOST "http://localhost:9200/_search" -d'
{
    "query": {
        "query_string": {
            "query": "kill"
        }
    }
}'
```

Let's execute the request and take a look at the result.

As expected we're getting two hits, one for each of the movies with the word "kill" in the title. Let's look at another scenario, searching in specific fields.

Specifying fields to search in In the previous example we used a very simple query, a query string query with only a single property, "query". As mentioned before the query string query has a number of settings that we can specify and if we don't it will use sensible default values.

One such setting is called "fields" and can be used to specify a list of fields to search in. If we don't use that the query will default to searching in a special field called `_all` that ElasticSearch automatically generates based on all of the individual fields in a document.

Let's try to search for movies only by title. That is, if we search for "ford" we want to get a hit for "The Assassination of Jesse James by the Coward Robert Ford" but not for either of the movies directed by Francis Ford Coppola.

In order to do that we modify the previous search request body so that the query string query has a fields property with an array of fields we want to search in:

```json
curl -XPOST "http://localhost:9200/_search" -d'
{  
   "query":{  
      "query_string":{  
         "query":"ford",
         "fields":[  
            "title"
         ]
      }
   }
 }'
```

**Let's execute that and see what happens:**

As expected we get a single hit, the movie with the word "ford" in its title. Compare that to a request were we've removed the fields property from the query:
