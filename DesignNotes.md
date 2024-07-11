# PresentationJson

A half-hearted take on DisplayPostscript

Session creation:

```
@JSON@{sessionName}
```

After session creation, the client will create one or more views:

```json
{
  "type": "view",
  "name": "{the name of the view}",
  "title": "{title of the view's window}",
  "layout": [
    ...
  ]
}
```

A view indicates what events should be sent back to the client:

```json
{
  "type": "event",
  "name": "{the name of the view}",
  "events": [
    {
      "name": "{name of the control}",
      "event": "{name of the event}",
      ...
    },
    ...
  ]
}
```

A view may be changed by the client"

```json
{
  "type": "update",
  "name": "{the name of the view to update}",
  "updates": [
    ...
  ]
}
```

