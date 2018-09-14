### What you need to get started

What things you need to install the software and how to install them:

-	[Docker](https://docs.docker.com/install/) - Used to build, ship, and run all services

### Setting up a local Elasticsearch instance:

```sh
docker-compose up
```

### Installing Elasticsearch Head

elasticsearch-head is a web front end for browsing and interacting with an Elastic Search cluster. You can find more info : [elasticsearch-head chrome extension](https://chrome.google.com/webstore/detail/elasticsearch-head/ffmkiejjmecolpfloofpjologoblkegm)

### Loading Data

Running the following script in your terminal will populate your local elasticsearch with real event data from the `sample_data.json` seed file.

```sh
./load_data.sh
```

> Connect to you're local elasticsearch via HEAD, and confirm data is present by first connecting to '' and then running the following request under the `Any Request` tab:

### Running your first query

```json
{  
   "query":{  
      "match_all":{  

      }
   }
}
```

If you can successfully view data via the Elasticsearch head client, you are now ready to progress onto creating an index.

<span style="float: left;">[Previous: Overview](searching)</span>

<span style="float: right;">[Next: Indexing](indexing)</span>