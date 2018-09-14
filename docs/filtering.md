### Filtering

We've covered a couple of simple free text search queries above. Let's look at another one where we search for "farset labs" without explicitly specifying fields:

```json
curl -XPOST "http://localhost:9200/_search" -d'
{
    "query": {
        "query_string": {
            "query": "farset labs"
        }
    }
}'
```

As we have twenty one events in our index containing the word "farset labs" in the `_all` field (from the category field) we get twenty one hits for the above query. Now, imagine that we want to limit these hits to events released in "Farset Labs Dojo 2018". In order to do that we need to apply a filter requiring the "description" field to equal "Farset Labs Dojo 2018".

To add such a filter we modify our search request body so that our current top level query, the query string query, is wrapped in a filtered query:

```json
{
    "query": {
        "filtered": {
            "query": {
                "query_string": {
                    "query": "farset labs"
                }
            },
            "filter": {

            }
        }
    }
}
```

A filtered query is a query that has two properties, query and filter. When executed it filters the result of the query using the filter. To finalize the query we'll need to add a filter requiring the description field to have value "Farset Labs Dojo 2018".

ElasticSearch's query DSL has a wide range of filters to choose from. For this simple case where a certain field should match a specific value a term filter will work well.

```json
"filter": {
    "term": { "description": "Farset Labs Dojo 2018" }
}
```

The complete search request now looks like this:

```json
curl -XPOST "http://localhost:9200/_search" -d'
{
    "query": {
        "filtered": {
            "query": {
                "query_string": {
                    "query": "farset labs"
                }
            },
            "filter": {
                "term": { "description": "Farset Labs Dojo 2018" }
            }
        }
    }
}'
```

When we execute it we, as expected, only get two hits, both with description == ""Farset Labs Dojo 2018".

### Filtering without a query

In the above example we limit the results of a query string query using a filter. What if all we want to do is apply a filter? That is, we want all events matching a certain criteria.

In such cases we still use the "query" property in the search request body, which expects a query. In other words, we can't just add a filter, we need to wrap it in some sort of query.

One solution for doing this is to modify our current search request, replacing the query string query in the filtered query with a match_all query which is a query that simply matches everything. Like this:

```json
curl -XPOST "http://localhost:9200/_search" -d'
{
    "query": {
        "filtered": {
            "query": {
                "match_all": {
                }
            },
            "filter": {
                "term": { "description": "Farset Labs Dojo 2018" }
            }
        }
    }
}'
```

Another, simpler option is to use a constant score query:

```json
curl -XPOST "http://localhost:9200/_search" -d'
{
    "query": {
        "constant_score": {
            "filter": {
                "term": { "description": "Farset Labs Dojo 2018" }
            }
        }
    }
}'
```

<span style="float: left;">[Previous: Searching](searching)</span>

<span style="float: right;">[Next: Mapping](mapping)</span>
