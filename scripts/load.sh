#!/bin/sh

jq -c '.[]' data/events.json | HEAD -100 | while read event; do
    id=$(echo $event | jq ".id")
    echo "Posting /events/event/$id"
    curl -XPOST "http://localhost:9200/events/event/$id" -H 'Content-Type: application/json' -d "$event"
done
