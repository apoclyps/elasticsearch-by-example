### Indexing

In ElasticSearch indexing corresponds to both "Create" and "Update" in CRUD - if we index a document with a given type and ID that doesn't already exists it's inserted. If a document with the same type and ID already exists it's overwritten.

In order to index a first JSON object we make a PUT request to the REST API to a URL made up of the index name, type name and ID. That is: http://localhost:9200/index/type/id.

Index and type are required while the id part is optional. If we don't specify an ID ElasticSearch will generate one for us. However, if we don't specify an id we should use POST instead of PUT.

The index name is arbitrary. If there isn't an index with that name on the server already one will be created using default configuration.

As for the type name it too is arbitrary. It serves several purposes, including:

Each type has its own ID space. Different types can have different mappings ("schema" that defines how properties/fields should be indexed). Although it's possible, and common, to search over multiple types, it's easy to search only for one or more specific type(s). Let's index something! We can put just about anything into our index as long as it can be represented as a single JSON object. In this tutorial we'll be indexing and searching for movies. Here's a classic one:

**Example Event**

```json
{
  "category": "Open Industry Index Social",
  "created": "2018-07-29T13:52:43.892339",
  "deleted": null,
  "description": "<p>A general space for anybody interested in open technologies (open source, open data or otherwise), to catch up and relax after work on Friday fortnights. People of all backgrounds, interests, skillsets and disciplines welcome.</p> <p>The Open Industry concept itself is about the ability of microentities and small businesses to collaborate formally on projects large and small, facilitated by open technologies - so we are combining the twin aims of:</p> <p>- giving tech freelancers, contractors and indies of all walks of technology life a focal point for an end-of-week (we need one too...), and</p> <p>- helping independents (and those considering a future step out) to link up to get sustainable open projects off the ground.</p>",
  "duration": 10000,
  "end": "2018-08-31T17:45:00",
  "entry": [
    {
      "description": null,
      "id": "f2a30c3b-aec6-46d7-ab34-b6f5b27c7955",
      "type": "free"
    }
  ],
  "id": "613119d5-f9ea-47d9-a9a9-42a39abdd036",
  "meetup": [

  ],
  "name": "Fortnightly Social",
  "source": "meetup",
  "start": "2018-08-31T17:45:00",
  "topics": [

  ],
  "updated": "2018-07-29T13:52:43.892346",
  "url": "https://www.meetup.com/Open-Industry-Index-Social/events/xcbqjpyxlbpc/"
}
```

To index that we decide on an index name ("movies"), a type name ("movie") and an id ("1") and make a request following the pattern described above with the JSON object in the body.

```json
curl -XPUT "http://localhost:9200/events/event/613119d5-f9ea-47d9-a9a9-42a39abdd036" -d'
{
  "category": "Open Industry Index Social",
  "created": "2018-07-29T13:52:43.892339",
  "deleted": null,
  "description": "<p>A general space for anybody interested in open technologies (open source, open data or otherwise), to catch up and relax after work on Friday fortnights. People of all backgrounds, interests, skillsets and disciplines welcome.</p> <p>The Open Industry concept itself is about the ability of microentities and small businesses to collaborate formally on projects large and small, facilitated by open technologies - so we are combining the twin aims of:</p> <p>- giving tech freelancers, contractors and indies of all walks of technology life a focal point for an end-of-week (we need one too...), and</p> <p>- helping independents (and those considering a future step out) to link up to get sustainable open projects off the ground.</p>",
  "duration": 10000,
  "end": "2018-08-31T17:45:00",
  "entry": [
    {
      "description": null,
      "id": "f2a30c3b-aec6-46d7-ab34-b6f5b27c7955",
      "type": "free"
    }
  ],
  "id": "613119d5-f9ea-47d9-a9a9-42a39abdd036",
  "meetup": [

  ],
  "name": "Fortnightly Social",
  "source": "meetup",
  "start": "2018-08-31T17:45:00",
  "topics": [

  ],
  "updated": "2018-07-29T13:52:43.892346",
  "url": "https://www.meetup.com/Open-Industry-Index-Social/events/xcbqjpyxlbpc/"
}'
```

You can either run that using curl or use Sense. With Sense you can either populate the URL, method and body yourself or you can copy the above curl example, place the cursor in the body field in Sense and press Ctrl/Command + Shift + V and all of the fields will be populated for you.

After executing the request we receive a response from ElasticSearch in the form of a JSON object.

```json
{
  "_index": "events",
  "_type": "event",
  "_id": "613119d5-f9ea-47d9-a9a9-42a39abdd036",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "created": true
}
```
