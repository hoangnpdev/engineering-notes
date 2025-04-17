# Restful API design

In my opinion, it is like a common language for every software developer to follow for better communication, 
instead of spontaneous naming.

## How?

All api represent for some certain resource in system.

/{version}/{service-name|product-name|project-name}/resources/

### Action
- GET: retrieve resource, condition: ?attribute1=value1&...
- POST: create a new resource
- PUT: update an existing resource
- DELETE: delete an existing resource
- CUSTOM: POST /{api-resource}:{custom-action}

### versioning
- /{version}/{api-resource}
