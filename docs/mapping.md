### Mapping

Let's look at a search request similar to the last one, only this time we filter by author instead of year.

```json
curl -XPOST "http://localhost:9200/_search" -d'
{
    "query": {
        "constant_score": {
            "filter": {
                "term": { "director": "Francis Ford Coppola" }
            }
        }
    }
}'
```

As we have two movies directed by Francis Ford Coppola in our index it doesn't seem too far fetched that this request should result in two hits, right? That's not the case however.

What's going on here? We've obviously indexed two movies with "Francis Ford Coppola" as director and that's what we see in search results as well. Well, while ElasticSearch has a JSON object with that data that it returns to us in search results in the form of the `_source` property that's not what it has in its index.

When we index a document with ElasticSearch it (simplified) does two things: it stores the original data untouched for later retrieval in the form of `_source` and it indexes each JSON property into one or more fields in a Lucene index. During the indexing it processes each field according to how the field is mapped. If it isn't mapped default mappings depending on the fields type (string, number etc) is used.

As we haven't supplied any mappings for our index ElasticSearch uses the default mappings for strings for the director field. This means that in the index the director fields value isn't "Francis Ford Coppola". Instead it's something more like ["francis", "ford", "coppola"].

We can verify that by modifying our filter to instead match "francis" (or "ford" or "coppola"):

So, what to do if we want to filter by the exact name of the director? We modify how it's mapped. There are a number of ways to add mappings to ElasticSearch, through a configuration file, as part of a HTTP request that creates and index and by calling the `_mapping` endpoint.

Using the last approach we could in theory fix the above issue by adding a mapping for the "director" field instructing ElasticSearch not to analyze (tokenize etc.) the field at all when indexing it, like this:

```json
curl -XPUT "http://localhost:9200/movies/movie/_mapping" -d'
{
   "movie": {
      "properties": {
         "director": {
            "type": "string",
            "index": "not_analyzed"
        }
      }
   }
}'
```

There are however a couple of issues if we do this. First of all, it won't work as there already is a mapping for the field:

In many cases it's not possible to modify existing mappings. Often the easiest work around for that is to create a new index with the desired mappings and re-index all of the data into the new index.

The second problem with adding the above mapping is that, even if we could add it, we would have limited our ability to search in the director field. That is, while a search for the exact value in the field would match we wouldn't be able to search for single words in the field.

Luckily, there's a simple solution to our problem. We add a mapping that upgrades the field to a multi field. What that means is that we'll map the field multiple times for indexing. Given that one of the ways we map it match the existing mapping both by name and settings that will work fine and we won't have to create a new index.

**Here's a request that does that:**

```json
curl -XPUT "http://localhost:9200/movies/movie/_mapping" -d'
{
   "movie": {
      "properties": {
         "director": {
            "type": "multi_field",
            "fields": {
                "director": {"type": "string"},
                "original": {"type" : "string", "index" : "not_analyzed"}
            }
         }
      }
   }
}'
```

**This time when we try to add the mappings ElasticSearch is happy to do so.**

So, what did we just do? We told ElasticSearch that whenever it sees a property named "director" in a movie document that is about to be indexed in the movies index it should index it multiple times. Once into a field with the same name (director) and once into a field named "director.original" and the latter field should not be analyzed, maintaining the original value allowing is to filter by the exact director name.

With our new shiny mapping in place we can re-index one or both of the movies directed by Francis Ford Coppola (copy from the list of initial indexing requests above) and try the search request that filtered by author again. Only, this time we don't filter on the "director" field (which is indexed the same way as before) but instead on the "director.original" field:

```json
curl -XPOST "http://localhost:9200/_search" -d'
{
    "query": {
        "constant_score": {
            "filter": {
                "term": { "director.original": "Francis Ford Coppola" }
            }
        }
    }
}'
```

Executing it shows that it indeed works:
