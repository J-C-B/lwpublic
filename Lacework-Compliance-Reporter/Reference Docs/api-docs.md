Download OpenAPI specification:[Download](https://docs.lacework.net/redocusaurus/plugin-redoc-0.yaml)

The Lacework API documentation is available directly from your Lacework application at the following URI: `https://YourLacework.lacework.net/api/v2/docs`, where `YourLacework` is your Lacework application.

No login to the Lacework Console is required. However, there is a link to the Lacework API 2.0 documentation from the Lacework Console. From the **Help** drop-down, select **API Documentation** and then **API 2.0 Documentation**.

All the Lacework API operations listed below require an API Access Token to allow access to the Lacework API. For more information about getting a temporary API Access Token to pass into these operations as a header, see [https://docs.lacework.com/generate-api-access-keys-and-tokens](https://docs.lacework.com/generate-api-access-keys-and-tokens).

You can run the Lacework APIs using your favorite REST API tools, such as curl or Postman. You can also run the Lacework API from the **Lacework CLI**. For more information, see [Get Started with the Lacework CLI](https://docs.lacework.com/cli).

## [](https://docs.lacework.net/api/v2/docs#tag/OVERVIEW)Overview

### Conventions

1.  **Parameters:** Parameters follow the JSON conventions, i.e., camelcase or lowerCamelcase notation, for all parameter names in the query, request and response bodies, for example, `startTime`, `endTime`.
    
2.  **Data Types:** For the constant types of data sets, integrations, assets, and other resources, the convention is to use UpperCamelcase notation, for example, `AlertChannels`, `AuditLogs`, `CloudActivities`.
    
3.  **Response Schema:** A successful response returns either the HTTP 200 or 201 Status Code and a top-level property called `data`, which contains the result in the JSON format. A response returning the HTTP 4xx or 5xx Status Code returns the top-level property called `message`, which contains an error message.
    
4.  `additionalProperties` **Keyword**: For all response schemas, the `additionalProperties` keyword is set to `true`. This means additional fields or properties can be added to responses in the future. For information about the `additionalProperties` keyword, see the [JSON Schema online documentation](http://json-schema.org/understanding-json-schema/reference/object.html#additional-properties).
    

### Simple & Advanced Search

The Lacework API provides simple and advanced searches for retrieving information.

For simple searches, specify a HTTP GET method with simple query parameters, for example, `startTime`, `endTime`.

For advanced searches, specify a HTTP POST method with filters in the request body. For a given endpoint, you can see what fields are available to filter on by viewing the response schema for the endpoint. The filters in requests that have multiple filters are `AND`'d, that is, all filters conditions must be met to satisfy a match.

There are 16 filter types consisting of seven pairs and two unique operators, which are similar to the SQL comparison operators for database queries. The pairs are:

-   The `eq` operator allows you to specify a value that the field values of the result must be equal to. The `ne` operator means not equal to. Note the `value` field of the `filters` must be used; the `values` field of the `filters` cannot be used for `eq` and `ne`.
    
-   The `in` operator allows you to specify multiple values in the `values` field of the `filters`. The field values of the result must match one of the values. The `not_in` operator is the opposite of `in`. Note the `value` field of the `filters` cannot be used for `in` and `not_in`.
    
-   The `like` operator allows you to specify a pattern that the field values of the result must match. The `not_like` operator is the opposite of `like`. Note the `values` field of the `filters` cannot be used for `like` and `not_like`.
    
-   The `ilike` operator works similar to `like` but it makes the match case insensitive. The `not_ilike` operator is the opposite of `ilike`. Note the `values` field of the `filters` cannot be used for `ilike` and `not_ilike`.
    
-   The `rlike` operator matches the specified pattern represented by regular expressions (more info on [RLIKE — Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/functions/rlike.html)). You can use `rlike` to filter object values in arrays, to return only those values that match a regular expression. The `not_rlike` operator is the opposite of `rlike`. Note the `values` field of the `filters` cannot be used for `rlike` and `not_rlike`.
    
-   The `gt` operator allows you to specify a value that the field values of the result must be `greater than`. The `lt` (less-than) operator is the opposite of `gt`. Note the `values` field of the `filters` cannot be used for `gt` and `lt`.
    
-   The `ge` operator allows you to specify a value that the field values of the result must be `greater than or equal to`. The `le` (less-than-or-equal-to) operator is the opposite of `ge`. Note the `values` field of the `filters` cannot be used for `ge` and `le`.
    

The unique operators are:

-   The `between` operator allows you to specify a range that the field values of the result must be within. The specified upper boundary must be larger/greater than the lower boundary. The two values of upper and lower boundaries must be set in the `values` field of the `filters`. Note the `value` field of the `filters` cannot be used for `between`.
    
-   The `expr` operator is reserved for future use.
    

### Date & Time Formats

For date and time parameters, the time zone is always UTC and the following formats are supported:

-   `yyyy-MM-dd` for example, `2020-12-18`
    
-   `yyyy-MM-ddTHH` for example, `2020-12-18T08`
    
-   `yyyy-MM-ddTHH:mm:ssZ` for example `2020-12-18T08:00:00Z`
    
-   `yyyy-MM-ddTHH:mm:ss.SSSZ` for example, `2020-12-18T08:00:00.000Z`
    

### Organization Level Access

An organization may have a primary account and multiple sub-accounts. An access token generated for the primary account and used as the authorization token can also be used for one of the sub-accounts, with the additional header called `Account-Name` (case insensitive).

For example, if the primary account is `xyz` and the sub-account is `xyz-sub1`, set the `Account-Name` header to `xyz-sub1`.

**Note:** Multiple sub-account and organizational-level access is limited to access tokens generated with regular user API keys. A service user has access to individual accounts only.

To access organization-level data sets, you can use a header called `Org-Access` (case insensitive). If this header is set to `true` (case insensitive) and the authorization token has the proper permissions (org admin), if specified, the `Account-Name` header is ignored. If the `Org-Access` header is not set to `true`, the `Account-Name` header is used, if specified.

### Pagination

Making calls to Lacework APIs could return a lot of results. Pagination of the results helps manage overall performance and makes the responses easier for you to handle by dividing the results into separate pages, each with a subset of the results.

The following row limits apply:

-   Row limit per page: 5,000 rows
    
-   Row limit of all pages of one result set: 500,000 rows
    

Pagination is available for some datasets, such as those that are searched with the `/api/v2/Vulnerabilities/Containers/search` or `/api/v2/Entities/Machines/search` endpoints.

Pagination metadata is located within the response's `paging` field, which contains information for `rows`, `totalRows`, and `urls`. The `urls` field contains the `nextPage` field with the Next Page URL. The Next Page URLs stay valid for 24 hours. No pagination is available for an API if the `paging` field is missing from a response.

To get the next page of the result, use the entire Next Page URL and send a GET request with the two required HTTP headers: "Authorization: Bearer {YourAPIToken}" and "Content-Type: application/json".

Example:

> `GET https://YourLacework.lacework.net/api/v2/Vulnerabilities/Containers/abcxyz...`

See the right panel for response examples.

### Rate Limiting

The current rate limit is 480 API requests per hour per user. When the total number of API requests on a one-hour rolling window exceeds the rate limit, the HTTP 429 Too Many Requests response status code is returned.

Lacework uses the token bucket algorithm to apply request rate limiting. Each API v2 functionality has its own bucket with 480 tokens and each request that you make removes one token from the bucket. For example, performing a `GET /api/v2/AgentAccessTokens` or a `GET /api/v2/AgentAccessTokens/{ID}` are both part of one functionality, which gets an agent access token, so each request removes one token from the same bucket. Similarly, updating an agent access token (`PATCH /api/v2/AgentAccessTokens/{ID}`) is a different functionality and disregards the ID to use the same bucket, so a token is removed from a different bucket.

Each request sends back three response headers following standard HTTP naming conventions for rate limiting. `RateLimit-Limit` is the total number of requests you can make in an hour, `RateLimit-Remaining` is the number of remaining requests, and `RateLimit-Reset` is how much time it will take (in seconds) before you can make another request once the limit is reached. For more information about `RateLimit` header fields, see [IETF Draft 05](https://tools.ietf.org/id/draft-polli-ratelimit-headers-05.html).

### POST Body Size Limit

Many Lacework API endpoints accept data as POST body content. POST body content is limited to 1 MB. Requests that exceed the 1 MB limit result in a 400 Bad Request error.

### Response Status Codes

The Lacework API endpoints return the following HTTP response status codes.

| Status Code | Definition | Description |
| --- | --- | --- |
| 200 | OK | The request has succeeded. |
| 201 | Created | The request has been fulfilled and resulted in a new resource being created. |
| 204 | No Content | The server has fulfilled the request but does not need to return an entity-body. |
| 400 | Bad Request | The request could not be understood by the server due to malformed syntax. The client SHOULD NOT repeat the request without modifications. |
| 401 | Unauthorized | The request requires user authentication. If the request already included Authorization credentials, then the 401 response indicates that authorization has been refused for those credentials. |
| 403 | Forbidden | The server understood the request, but is refusing to fulfill it. Authorization will not fix the issue and the request SHOULD NOT be repeated. |
| 404 | Not Found | The server has not found anything matching the Request-URI. |
| 405 | Method Not Allowed | The method specified in the Request-Line is not allowed for the resource identified by the Request-URI. |
| 409 | Conflict | The request could not be completed due to a conflict with the current state of the resource. |
| 429 | Too Many Requests | Too many requests occurred during the allotted time period and rate limiting was applied. |
| 500 | Internal Server Error | The request did not complete due to an internal error on the server side. The server encountered an unexpected condition which prevented it from fulfilling the request. |
| 503 | Service Unavailable | The server is currently unable to handle the request due to a temporary overloading or maintenance of the server. |

## [](https://docs.lacework.net/api/v2/docs#tag/ACCESS_TOKENS)Access Tokens

## [](https://docs.lacework.net/api/v2/docs#tag/ACCESS_TOKENS/paths/~1api~1v2~1access~1tokens/post)Generate Access Tokens

Get access tokens for the API requests by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/access/tokens`

After creating a secret key, administrators can generate Temporary API access (bearer) tokens that clients and client applications use to access the Lacework API. Create temporary API access (bearer) tokens by invoking the `POST https://YourLacework.lacework.net/api/v2/access/tokens` endpoint.

##### header Parameters

<table><tbody><tr><td kind="field" title="X-LW-UAKS"><span></span><span>X-LW-UAKS</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="keyId"><span></span><span>keyId</span><p>required</p></td><td></td></tr><tr><td kind="field" title="expiryTime"><span></span><span>expiryTime</span><p>required</p></td><td><div><p><span></span><span>integer</span></p><div><p>The access token's expiration (in seconds) that you want to set. Maximum value: 86400 (24 hours).</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"keyId": "YourSecretKey",`
    
-   `"expiryTime": 3600`
    

`}`

### Response samples

-   201
-   4XX
-   5XX

Content type

application/json

`{`

-   `"expiresAt": "2021-08-18T08:00:00.000Z",`
    
-   `"token": "string"`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/SCHEMAS)Schemas

Get details about the available Lacework schemas.

## [](https://docs.lacework.net/api/v2/docs#tag/SCHEMAS/paths/~1api~1v2~1schemas~1{type}/get)Schema Details

Get a list of available Lacework schema types by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/schemas`

Get details about a Lacework schema by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/schemas/{type}`

Here is an example invocation:

> `GET https://YourLacework.lacework.net/api/v2/schemas/AuditLogs`

##### path Parameters

<table><tbody><tr><td kind="field" title="type"><span></span><span>type</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Example: </span><span>AuditLogs</span></p><div><p>When sending a request, use this parameter to specify the schema type. If not specified, the response returns all schema types. If specified, the response returns details of the requested schema.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`[`

-   `{`
    
    -   `"name": "accountName",`
        
    -   `"type": "string"`
        
    
    `},`
    
-   `{`
    
    -   `"name": "createdTime",`
        
    -   `"type": "integer"`
        
    
    `},`
    
-   `{`
    
    -   `"name": "eventDescription",`
        
    -   `"type": "string"`
        
    
    `},`
    
-   `{`
    
    -   `"name": "eventName",`
        
    -   `"type": "string"`
        
    
    `},`
    
-   `{`
    
    -   `"name": "userAction",`
        
    -   `"type": "string"`
        
    
    `},`
    
-   `{`
    
    -   `"name": "userName",`
        
    -   `"type": "string"`
        
    
    `}`
    

`]`

## [](https://docs.lacework.net/api/v2/docs#tag/SCHEMAS/paths/~1api~1v2~1schemas~1{type}~1{subtype}/get)Schema Details of Subtype

Get details about a Lacework schema by specifying a schema type and subtype when invoking the endpoint.

> `GET https://YourLacework.lacework.net/api/v2/schemas/{type}/{subtype}`

Here is an example invocation:

> `GET https://YourLacework.lacework.net/api/v2/schemas/AlertChannels/SlackChannel`

##### path Parameters

<table><tbody><tr><td kind="field" title="type"><span></span><span>type</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Example: </span><span>AlertChannels</span></p><div><p>When sending a request, use this parameter to specify the schema type. If not specified, the response returns all schema types. If specified, the response returns details of the requested schema.</p></div></div></td></tr><tr><td kind="field" title="subtype"><span></span><span>subtype</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Example: </span><span>SlackChannel</span></p><div><p>The schema's subtype. If a type is subordinate to another type, it is called a subtype.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`[`

-   `{`
    
    -   `"required": [],`
        
    -   `"properties": {}`
        
    
    `}`
    

`]`

## [](https://docs.lacework.net/api/v2/docs#tag/Activities)Activities

Get information about network activities detected through the agent.

## [](https://docs.lacework.net/api/v2/docs#tag/Activities/paths/~1api~1v2~1Activities~1ChangedFiles~1search/post)Search Changed Files

Search for changed files in your environment by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Activities/ChangedFiles/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned changed files by start time, end time, machine ID, file path, and more. For more information, see [CHANGE\_FILES\_V View](https://docs.lacework.com/changefilesv-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "48011" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "48011" }, { "field": "filePath", "expression": "eq", "value": "/usr/bin/curl" } ],`  
    `"returns": [ "filePath", "filedataHash", "mid" ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 654455,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Activities/paths/~1api~1v2~1Activities~1Connections~1search/post)Search Connections

Search for connections in your environment by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Activities/Connections/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned connections by start time, end time, created time, machine ID, and more. For more information, see [CONNECTIONS\_V View](https://docs.lacework.com/connectionsv-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2022-08-18T00:00:00Z", "endTime": "2022-08-18T02:00:00Z"},` `"filters": [ { "field": "dstEntityId.mid", "expression": "eq", "value": "116018" } ] }`
-   `{ "timeFilter": { "startTime": "2022-08-18T00:00:00Z", "endTime": "2022-08-18T02:00:00Z"},` `"filters": [ { "field": "srcEntityId.mid", "expression": "eq", "value": "123456" }, { "field": "dstInBytes", "expression": "le", "value": "300000" } ],`  
    `"returns": [ "dstEntityId", "dstEntityType", "srcEntityId", "srcEntityType" ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 1233301,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Activities/paths/~1api~1v2~1Activities~1DNSs~1search/post)Search DNS Summaries

Search for DNS summaries in your environment by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Activities/DNSs/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned DNS summaries by start time, end time, created time, machine ID, and more. For more information, see [DNS\_QUERY\_V View](https://docs.lacework.com/dnsqueryv-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "48011" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "48011" }, { "field": "fqdn", "expression": "eq", "value": "sqs.us-west-2.amazonaws.com" } ],`  
    `"returns": [ "fqdn", "hostIpAddr", "mid" ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 17519,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Activities/paths/~1api~1v2~1Activities~1UserLogins~1search/post)Search User Logins

Search for user logins in your environment by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Activities/UserLogins/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned login activities by start time, end time, created time, machine ID, and more. For more information, see [USER\_LOGIN\_V View](https://docs.lacework.com/userloginv-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "48011" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "48011" }, { "field": "username", "expression": "eq", "value": "ec2-user" } ],`  
    `"returns": [ "username", "activityType", "activityTime" ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 5050,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AgentAccessTokens)Agent Access Tokens

## [](https://docs.lacework.net/api/v2/docs#tag/AgentAccessTokens/paths/~1api~1v2~1AgentAccessTokens/post)Create Agent Access Token

Create a new agent access token that an agent can use to connect and send data to your Lacework instance by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/AgentAccessTokens`

Here is an example `body` payload:

> `{ "tokenAlias": "prod", "tokenEnabled": "1" }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="props"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The access token's properties, including <code>createdTime</code> and <code>description</code>.</p></div></div></td></tr><tr><td kind="field" title="tokenEnabled"><span></span><span>tokenEnabled</span><p>required</p></td><td><div><p><span></span><span>string</span><span> <span>non-empty</span></span></p><div><p>The <code>tokenEnabled</code> property determines if an edit control is a "Text token" edit control. When the <code>tokenEnabled</code> property is set to <code>1</code>, if the user enters a separator character or a carriage return (CR), a token is automatically added and the user can continue entering values in the control.</p></div></div></td></tr><tr><td kind="field" title="tokenAlias"><span></span><span>tokenAlias</span><p>required</p></td><td><div><p><span></span><span>string</span><span> <span>non-empty</span></span></p><div><p>The token's alias such as Ops Agent. Aliases help communicate the intended purpose of a token and are effective when a value with a single intent appears in multiple places.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"props": {`
    
    -   `"description": "string",`
        
    -   `"os": "string",`
        
    -   `"subscription": "standard"`
        
    
    `},`
    
-   `"tokenEnabled": "string",`
    
-   `"tokenAlias": "string"`
    

`}`

### Response samples

-   201
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"accessToken": "47d102752b57caa18b...",`
        
    -   `"createdTime": "2020-12-16T16:43:37.915Z",`
        
    -   `"props": {},`
        
    -   `"tokenAlias": "Ops Agent",`
        
    -   `"tokenEnabled": "1",`
        
    -   `"version": "0.1"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AgentAccessTokens/paths/~1api~1v2~1AgentAccessTokens/get)List All Agent Access Tokens

Get a list of currently enabled agent access tokens in your Lacework instance by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/AgentAccessTokens`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AgentAccessTokens/paths/~1api~1v2~1AgentAccessTokens~1search/post)Search Agent Access Tokens

Search all enabled agent access tokens in your Lacework instance by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/AgentAccessTokens/search`

To limit the returned result, optionally specify one or more filters in the request body. For more information about using filters, see the [Simple & Advanced Search section](https://docs.lacework.net/api/v2/docs/#tag/OVERVIEW).

You can filter on the following fields:

-   `accessToken`
    
-   `createdTime`
    
-   `tokenAlias`
    
-   `tokenEnabled`
    
-   `version`
    

Here is an example `body` payload:

> `{ "filters" : [ { "expression": "eq", "field": "tokenAlias", "value": "Eng" } ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AgentAccessTokens/paths/~1api~1v2~1AgentAccessTokens~1{id}/get)Agent Access Token Details

Get details about an agent access token by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/AgentAccessTokens/{id}`

You can get the `{id}` by invoking the `GET /api/v2/AgentAccessTokens` endpoint. Replace `{id}` with the long hexadecimal access token identifier returned in the `accessToken` field of the `GET /api/v2/AgentAccessTokens` endpoint response.

##### path Parameters

<table><tbody><tr><td kind="field" title="id"><span></span><span>id</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"accessToken": "47d102752b57caa18b...",`
        
    -   `"createdTime": "2020-12-16T16:43:37.915Z",`
        
    -   `"props": {},`
        
    -   `"tokenAlias": "Ops Agent",`
        
    -   `"tokenEnabled": "1",`
        
    -   `"version": "0.1"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AgentAccessTokens/paths/~1api~1v2~1AgentAccessTokens~1{id}/patch)Update Agent Access Token

Optionally update the `tokenEnabled` settings of the passed in agent access token. Update these settings by invoking the following endpoint:

> `PATCH https://YourLacework.lacework.net/api/v2/AgentAccessTokens/{id}`

Get the agent access token id by calling the `GET /api/v2/AgentAccessTokens` endpoint.

Replace `{id}` with the long hexadecimal access token identifier returned in the `accessToken` field of the `GET /api/v2/AgentAccessTokens` endpoint response.

Here is an example `body` payload:

> `{ "tokenEnabled": "1" }`

##### path Parameters

<table><tbody><tr><td kind="field" title="id"><span></span><span>id</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="props"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The access token's properties, including <code>createdTime</code> and <code>description</code>.</p></div></div></td></tr><tr><td kind="field" title="tokenEnabled"><span></span><span>tokenEnabled</span></td><td><div><p><span></span><span>string</span><span> <span>non-empty</span></span></p><div><p>The <code>tokenEnabled</code> property determines if an edit control is a "Text token" edit control. When the <code>tokenEnabled</code> property is set to <code>1</code>, if the user enters a separator character or a carriage return (CR), a token is automatically added and the user can continue entering values in the control.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"props": {`
    
    -   `"description": "string",`
        
    -   `"os": "string",`
        
    -   `"subscription": "standard"`
        
    
    `},`
    
-   `"tokenEnabled": "string"`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"accessToken": "47d102752b57caa18b...",`
        
    -   `"createdTime": "2020-12-16T16:43:37.915Z",`
        
    -   `"props": {},`
        
    -   `"tokenAlias": "Ops Agent",`
        
    -   `"tokenEnabled": "1",`
        
    -   `"version": "0.1"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AgentInfo)Agent Information

View and verify information about all agents, including:

-   The hostname
-   The number of active and inactive agents
-   Machine tags information associated with the agents
-   The agent version

## [](https://docs.lacework.net/api/v2/docs#tag/AgentInfo/paths/~1api~1v2~1AgentInfo~1search/post)Search Agent Information

The Agent Information API enables you to retrieve information about all agents by invoking the following endpoint:

> `POST /api/v2/AgentInfo/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the information returned by agent status, agent version, IP address, and more. For details about what agent information is available, see [AGENT\_MANAGEMENT\_V View](https://docs.lacework.com/console/agentmanagementv-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime" : "2022-04-28T00:00:00Z", "endTime": "2022-04-28T18:00:00Z"},`
-   `{ "timeFilter": { "startTime": " 2022-04-28T00:00:00Z", "endTime": "2022-04-28T18:00:00Z"},` `"filters" : [ { "field": "status", "expression": "eq", "value": "ACTIVE" }, { "field": "tags.VmProvider", "expression": "eq", "value" : "AWS" } ],`  
    `"returns": [ "hostname", "ipAddr", "os" , "agentVersion", "status" ] }`

Within request bodies, nested field names that contain one or more special characters—e.g., dot ("."), colon (":"), or slash ("/")—must be enclosed in **escaped double quotes**. For example, the field name `aws:ec2launchtemplate:version` nested under the `tags` field would be rendered as follows:

`"tags.\"aws:ec2launchtemplate:version\""`

In a filter, the example would appear as follows:

`{ "field": "tags.\"aws:ec2launchtemplate:version\"", "expression": "eq", "value": "3" }`

In addition, forward slash characters within field names must be escaped with a backslash, as in the following example:

`"tags.\"kubernetes.io\/cluster\/prod1\""`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 5060,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertChannels)Alert Channels

Lacework combines [alert channels](https://docs.lacework.com/about-alert-channels) with [alert rules](https://docs.lacework.com/alert-rules) or [report rules](https://docs.lacework.com/report-rules) to provide a flexible method for routing alerts and reports.

-   For [alert channels](https://docs.lacework.com/about-alert-channels), you define where to send alerts or reports, such as to Jira, Slack, or email.
-   For [alert rules](https://docs.lacework.com/alert-rules), you define information about which alert types to send, such as critical and high severity compliance alerts.
-   For [report rules](https://docs.lacework.com/report-rules), you define information about which reports to send.

## [](https://docs.lacework.net/api/v2/docs#tag/AlertChannels/paths/~1api~1v2~1AlertChannels/post)Create Alert Channels

Create an alert channel by specifying parameters in the request body when invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/AlertChannels`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="name"><span></span><span>name</span><p>required</p></td><td><div><p><span></span><span>string</span><span> (Name) </span><span><span>non-empty </span></span><span>(?!^ +$)^.+$</span></p><div><p>When sending a request, use this attribute to specify an integration’s name. When included in a response, this attribute returns the specified integration’s name.</p></div></div></td></tr><tr><td kind="field" title="type"><span></span><span>type</span><p>required</p></td><td><div><p><span></span><span>string</span><span> (Type)</span></p><div><p>When sending a request, use this attribute to specify the type of integration, from the following options. When included in a response, this attribute returns the specified integration’s type.</p></div><p><label>AwsS3</label></p></div></td></tr><tr><td kind="field" title="enabled"><span></span><span>enabled</span><p>required</p></td><td><div><p><span></span><span>number</span><span> (Enabled) </span><span><span>[ 0 .. 1 ]</span></span></p><div><p>When sending a request, use this attribute to enable or disable an integration. When included in a response, returns <code>1</code> for an enabled integration or <code>0</code> for a disabled integration.</p></div></div></td></tr><tr><td kind="field" title="data"><span></span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"name": "string",`
    
-   `"type": "AwsS3",`
    
-   `"enabled": 1,`
    
-   `"data": {`
    
    -   `"s3CrossAccountCredentials": {}`
        
    
    `}`
    

`}`

### Response samples

-   201
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"createdOrUpdatedBy": "user@example.com",`
        
    -   `"createdOrUpdatedTime": "2021-02-08T08:28:18Z",`
        
    -   `"enabled": 1,`
        
    -   `"intgGuid": "LWXYZ...",`
        
    -   `"isOrg": 0,`
        
    -   `"name": "Support",`
        
    -   `"props": "{object}",`
        
    -   `"state": "{object}",`
        
    -   `"type": "AwsS3",`
        
    -   `"data": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertChannels/paths/~1api~1v2~1AlertChannels/get)List All Alert Channels

Get a list of alert channels for the current user by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/AlertChannels`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertChannels/paths/~1api~1v2~1AlertChannels~1{type}/get)List Alert Channels by Type

Get a list of alert channels of the specified type by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/AlertChannels/{type}`

Here is an example invocation:

> `GET https://YourLacework.lacework.net/api/v2/AlertChannels/SlackChannel`

##### path Parameters

<table><tbody><tr><td kind="field" title="type"><span></span><span>type</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"AwsS3"</span> <span>"CiscoSparkWebhook"</span> <span>"CloudwatchEb"</span> <span>"Datadog"</span> <span>"EmailUser"</span> <span>"GcpPubsub"</span> <span>"IbmQradar"</span> <span>"Jira"</span> <span>"MicrosoftTeams"</span> <span>"NewRelicInsights"</span> <span>"PagerDutyApi"</span> <span>"ServiceNowRest"</span> <span>"SlackChannel"</span> <span>"SplunkHec"</span> <span>"VictorOps"</span> <span>"Webhook"</span></p></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertChannels/paths/~1api~1v2~1AlertChannels~1search/post)Search Alert Channels

Search alert channels by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/AlertChannels/search`

To limit the returned result, optionally specify one or more filters in the request body. For more information about using filters, see the [Simple & Advanced Search section](https://docs.lacework.net/api/v2/docs/#tag/OVERVIEW).

In the request body, optionally specify the list of fields to return in the response by specifying the list in the `returns` array, for example, `"returns":[ "name", "type", "enabled" ]`.

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertChannels/paths/~1api~1v2~1AlertChannels~1{intgGuid}~1test/post)Test Alert Channels

Test the integration of an alert channel by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/AlertChannels/{intgGuid}/test`

##### path Parameters

<table><tbody><tr><td kind="field" title="intgGuid"><span></span><span>intgGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertChannels/paths/~1api~1v2~1AlertChannels~1{intgGuid}/get)Alert Channel Details

Get details about an alert channel by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/AlertChannels/{intgGuid}`

##### path Parameters

<table><tbody><tr><td kind="field" title="intgGuid"><span></span><span>intgGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"createdOrUpdatedBy": "user@example.com",`
        
    -   `"createdOrUpdatedTime": "2021-02-08T08:28:18Z",`
        
    -   `"enabled": 1,`
        
    -   `"intgGuid": "LWXYZ...",`
        
    -   `"isOrg": 0,`
        
    -   `"name": "Support",`
        
    -   `"props": "{object}",`
        
    -   `"state": "{object}",`
        
    -   `"type": "AwsS3",`
        
    -   `"data": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertChannels/paths/~1api~1v2~1AlertChannels~1{intgGuid}/patch)Update Alert Channels

Update an alert channel by specifying parameters in the request body when invoking the following endpoint:

> `PATCH https://YourLacework.lacework.net/api/v2/AlertChannels/{intgGuid}`

In the request body, only specify the parameter(s) that you want to update, for example, `{ "enabled" : 0 }`.

##### path Parameters

<table><tbody><tr><td kind="field" title="intgGuid"><span></span><span>intgGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

Only specify the parameter(s) that you want to update, for example, `{ "enabled" : 0 }`.

<table><tbody><tr><td kind="field" title="name"><span></span><span>name</span></td><td><div><p><span></span><span>string</span><span> (Name) </span><span><span>non-empty </span></span><span>(?!^ +$)^.+$</span></p><div><p>When sending a request, use this attribute to specify an integration’s name. When included in a response, this attribute returns the specified integration’s name.</p></div></div></td></tr><tr><td kind="field" title="type"><span></span><span>type</span></td><td><div><p><span></span><span>string</span><span> (Type)</span></p><div><p>When sending a request, use this attribute to specify the type of integration, from the following options. When included in a response, this attribute returns the specified integration’s type.</p></div><p><label>AwsS3</label></p></div></td></tr><tr><td kind="field" title="enabled"><span></span><span>enabled</span></td><td><div><p><span></span><span>number</span><span> (Enabled) </span><span><span>[ 0 .. 1 ]</span></span></p><div><p>When sending a request, use this attribute to enable or disable an integration. When included in a response, returns <code>1</code> for an enabled integration or <code>0</code> for a disabled integration.</p></div></div></td></tr><tr><td kind="field" title="data"><span></span></td><td></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"name": "string",`
    
-   `"type": "AwsS3",`
    
-   `"enabled": 1,`
    
-   `"data": {`
    
    -   `"s3CrossAccountCredentials": {}`
        
    
    `}`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"createdOrUpdatedBy": "user@example.com",`
        
    -   `"createdOrUpdatedTime": "2021-02-08T08:28:18Z",`
        
    -   `"enabled": 1,`
        
    -   `"intgGuid": "LWXYZ...",`
        
    -   `"isOrg": 0,`
        
    -   `"name": "Support",`
        
    -   `"props": "{object}",`
        
    -   `"state": "{object}",`
        
    -   `"type": "AwsS3",`
        
    -   `"data": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertChannels/paths/~1api~1v2~1AlertChannels~1{intgGuid}/put)Update Alert Channels

Update an alert channel by specifying the entire object in the request body when invoking the following endpoint:

> `PUT https://YourLacework.lacework.net/api/v2/AlertChannels/{intgGuid}`

In the request body, specify the entire object that you want to update, for example,

> `{"name": "string","type": "AwsS3", "enabled": 1, "data": {"s3CrossAccountCredentials": {"externalId": "string", "roleArn": "string", "bucketArn":"string"}} }`.

##### path Parameters

<table><tbody><tr><td kind="field" title="intgGuid"><span></span><span>intgGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="name"><span></span><span>name</span><p>required</p></td><td><div><p><span></span><span>string</span><span> (Name) </span><span><span>non-empty </span></span><span>(?!^ +$)^.+$</span></p><div><p>When sending a request, use this attribute to specify an integration’s name. When included in a response, this attribute returns the specified integration’s name.</p></div></div></td></tr><tr><td kind="field" title="type"><span></span><span>type</span><p>required</p></td><td><div><p><span></span><span>string</span><span> (Type)</span></p><div><p>When sending a request, use this attribute to specify the type of integration, from the following options. When included in a response, this attribute returns the specified integration’s type.</p></div><p><label>AwsS3</label></p></div></td></tr><tr><td kind="field" title="enabled"><span></span><span>enabled</span><p>required</p></td><td><div><p><span></span><span>number</span><span> (Enabled) </span><span><span>[ 0 .. 1 ]</span></span></p><div><p>When sending a request, use this attribute to enable or disable an integration. When included in a response, returns <code>1</code> for an enabled integration or <code>0</code> for a disabled integration.</p></div></div></td></tr><tr><td kind="field" title="data"><span></span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"name": "string",`
    
-   `"type": "AwsS3",`
    
-   `"enabled": 1,`
    
-   `"data": {`
    
    -   `"s3CrossAccountCredentials": {}`
        
    
    `}`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"createdOrUpdatedBy": "user@example.com",`
        
    -   `"createdOrUpdatedTime": "2021-02-08T08:28:18Z",`
        
    -   `"enabled": 1,`
        
    -   `"intgGuid": "LWXYZ...",`
        
    -   `"isOrg": 0,`
        
    -   `"name": "Support",`
        
    -   `"props": "{object}",`
        
    -   `"state": "{object}",`
        
    -   `"type": "AwsS3",`
        
    -   `"data": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertChannels/paths/~1api~1v2~1AlertChannels~1{intgGuid}/delete)Delete Alert Channels

Delete an alert channel by invoking the following endpoint:

> `DELETE https://YourLacework.lacework.net/api/v2/AlertChannels/{intgGuid}`

##### path Parameters

<table><tbody><tr><td kind="field" title="intgGuid"><span></span><span>intgGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertProfiles)Alert Profiles

An alert profile is a set of metadata that defines how your LQL queries get consumed into events and alerts.

Alert profiles exist as a system. Lacework provides a set of predefined alert profiles to ensure that policy evaluation gives you useful results out of the box. To create your own customized profiles, you extend an existing alert profile and add your custom definitions to it. The predefined alert profiles and operations for defining and editing your own are exposed via Lacework API calls.

## [](https://docs.lacework.net/api/v2/docs#tag/AlertProfiles/paths/~1api~1v2~1AlertProfiles/post)Create Alert Profiles

Create an alert profile that extends off of a current alert profile by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/AlertProfiles`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="alerts"><span></span><p>required</p></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>An alert is a definition of content to create from the results of a resource's policy violation. The event name, subject, and description contained in the alert appear in pushed alerts and in the Lacework Console.</p></div></div></td></tr><tr><td kind="field" title="alertProfileId"><span></span><span>alertProfileId</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Unique id within customer account for Alert Profile</p></div></div></td></tr><tr><td kind="field" title="extends"><span></span><span>extends</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Base Lacework defined Alert Profile to inherit properties</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"alerts": [`
    
    -   `{}`
        
    
    `],`
    
-   `"alertProfileId": "string",`
    
-   `"extends": "string"`
    

`}`

### Response samples

-   201
-   4XX
-   5XX

Content type

application/json

`[`

-   `{`
    
    -   `"alertProfileId": "Custom_HE_Machines_AlertProfile",`
        
    -   `"extends": "LW_HE_Machines",`
        
    -   `"fields": [],`
        
    -   `"descriptionKeys": [],`
        
    -   `"alerts": []`
        
    
    `}`
    

`]`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertProfiles/paths/~1api~1v2~1AlertProfiles/get)List All Alert Profiles

Get all the alert profiles for the current user by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/AlertProfiles`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`[`

-   `{`
    
    -   `"alertProfileId": "Custom_HE_Machines_AlertProfile",`
        
    -   `"extends": "LW_HE_Machines",`
        
    -   `"fields": [],`
        
    -   `"descriptionKeys": [],`
        
    -   `"alerts": []`
        
    
    `}`
    

`]`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertProfiles/paths/~1api~1v2~1AlertProfiles~1{id}/get)Alert Profiles Details

Get the details to the specified alert profile by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/AlertProfiles/{alertProfileId}`

##### path Parameters

<table><tbody><tr><td kind="field" title="id"><span></span><span>id</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`[`

-   `{`
    
    -   `"alertProfileId": "Custom_HE_Machines_AlertProfile",`
        
    -   `"extends": "LW_HE_Machines",`
        
    -   `"fields": [],`
        
    -   `"descriptionKeys": [],`
        
    -   `"alerts": []`
        
    
    `}`
    

`]`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertProfiles/paths/~1api~1v2~1AlertProfiles~1{id}/patch)Update Alert Profiles

Update the alert templates of the specified alert profile by invoking the following endpoint:

> `PATCH https://YourLacework.lacework.net/api/v2/AlertProfiles/{alertProfileId}`

##### path Parameters

<table><tbody><tr><td kind="field" title="id"><span></span><span>id</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="alerts"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>An alert is a definition of content to create from the results of a resource's policy violation. The event name, subject, and description contained in the alert appear in pushed alerts and in the Lacework Console.</p></div></div></td></tr><tr><td colspan="2"><div><p>Array</p><div><table><tbody><tr><td kind="field" title="name"><span></span><span>name</span></td><td><div><p><span></span><span>string</span></p><div><p>A name that policies can use to refer to this definition when generating alerts</p></div></div></td></tr><tr><td kind="field" title="eventName"><span></span><span>eventName</span></td><td><div><p><span></span><span>string</span></p><div><p>The name of the resulting alert</p></div></div></td></tr><tr><td kind="field" title="description"><span></span><span>description</span></td><td><div><p><span></span><span>string</span></p><div><p>Summary of the resulting alert</p></div></div></td></tr><tr><td kind="field" title="subject"><span></span><span>subject</span></td><td><div><p><span></span><span>string</span></p><div><p>A high-level observation of the resulting alert</p></div></div></td></tr></tbody></table></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"alerts": [`
    
    -   `{}`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`[`

-   `{`
    
    -   `"alertProfileId": "Custom_HE_Machines_AlertProfile",`
        
    -   `"extends": "LW_HE_Machines",`
        
    -   `"fields": [],`
        
    -   `"descriptionKeys": [],`
        
    -   `"alerts": []`
        
    
    `}`
    

`]`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertProfiles/paths/~1api~1v2~1AlertProfiles~1{id}/delete)Delete Alert Profiles

Delete the specified alert profile by invoking the following endpoint:

> `DELETE https://YourLacework.lacework.net/api/v2/AlertProfiles/{alertProfileId}`

##### path Parameters

<table><tbody><tr><td kind="field" title="id"><span></span><span>id</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertProfiles/paths/~1api~1v2~1AlertProfiles~1{id}~1AlertTemplates/post)Create Alert Templates

Create a new alert template for a specified alert profile by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/AlertProfiles/{alertProfileId}/AlertTemplates`

##### path Parameters

<table><tbody><tr><td kind="field" title="id"><span></span><span>id</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="name"><span></span><span>name</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>A name that policies can use to refer to this definition when generating alerts</p></div></div></td></tr><tr><td kind="field" title="eventName"><span></span><span>eventName</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>The name of the resulting alert</p></div></div></td></tr><tr><td kind="field" title="description"><span></span><span>description</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Summary of the resulting alert</p></div></div></td></tr><tr><td kind="field" title="subject"><span></span><span>subject</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>A high-level observation of the resulting alert</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"name": "string",`
    
-   `"eventName": "string",`
    
-   `"description": "string",`
    
-   `"subject": "string"`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`[`

-   `{`
    
    -   `"alertProfileId": "Custom_HE_Machines_AlertProfile",`
        
    -   `"extends": "LW_HE_Machines",`
        
    -   `"fields": [],`
        
    -   `"descriptionKeys": [],`
        
    -   `"alerts": []`
        
    
    `}`
    

`]`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertProfiles/paths/~1api~1v2~1AlertProfiles~1{id}~1AlertTemplates~1{alertTemplateName}/patch)Update Alert Templates

Update an alert template for a specified alert profile by invoking the following endpoint:

> `PATCH https://YourLacework.lacework.net/api/v2/AlertProfiles/{alertProfileId}/AlertTemplates/{alertTemplateName}`

##### path Parameters

<table><tbody><tr><td kind="field" title="id"><span></span><span>id</span><p>required</p></td><td></td></tr><tr><td kind="field" title="alertTemplateName"><span></span><span>alertTemplateName</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="eventName"><span></span><span>eventName</span></td><td><div><p><span></span><span>string</span></p><div><p>The name of the resulting alert</p></div></div></td></tr><tr><td kind="field" title="description"><span></span><span>description</span></td><td><div><p><span></span><span>string</span></p><div><p>Summary of the resulting alert</p></div></div></td></tr><tr><td kind="field" title="subject"><span></span><span>subject</span></td><td><div><p><span></span><span>string</span></p><div><p>A high-level observation of the resulting alert</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"eventName": "string",`
    
-   `"description": "string",`
    
-   `"subject": "string"`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`[`

-   `{`
    
    -   `"alertProfileId": "Custom_HE_Machines_AlertProfile",`
        
    -   `"extends": "LW_HE_Machines",`
        
    -   `"fields": [],`
        
    -   `"descriptionKeys": [],`
        
    -   `"alerts": []`
        
    
    `}`
    

`]`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertProfiles/paths/~1api~1v2~1AlertProfiles~1{id}~1AlertTemplates~1{alertTemplateName}/delete)Delete Alert Templates

Delete an alert template for a specified alert profile by invoking the following endpoint:

> `DELETE https://YourLacework.lacework.net/api/v2/AlertProfiles/{alertProfileId}/AlertTemplates/{alertTemplateName}`

##### path Parameters

<table><tbody><tr><td kind="field" title="id"><span></span><span>id</span><p>required</p></td><td></td></tr><tr><td kind="field" title="alertTemplateName"><span></span><span>alertTemplateName</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertRules)Alert Rules

Lacework combines [alert channels](https://docs.lacework.com/about-alert-channels) and [alert rules](https://docs.lacework.com/alert-rules) to provide a flexible method for routing alerts. For [alert channels](https://docs.lacework.com/about-alert-channels), you define information about where to send alerts, such as to Jira, Slack, or email. For [alert rules](https://docs.lacework.com/alert-rules), you define information about which alert types to send, such as critical and high severity compliance alerts.

## [](https://docs.lacework.net/api/v2/docs#tag/AlertRules/paths/~1api~1v2~1AlertRules/post)Create Alert Rules

Create an alert rule by specifying parameters in the request body when invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/AlertRules`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span><p>required</p></td><td><div><p><span></span><span>object</span></p><div><p>When sending a request, use this object to define the new alert rule. When included in a response, this object contains details of an alert rule. You can use these attributes when searching for existing alert rules by invoking a GET request.</p></div></div></td></tr><tr><td kind="field" title="intgGuidList"><span></span><span>intgGuidList</span><p>required</p></td><td><div><p><span>Array of </span><span>strings</span><span> <span>non-empty </span><span>unique</span></span></p><div><p>The alert channels for the rule to access.</p></div></div></td></tr><tr><td kind="field" title="type"><span></span><span>type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": {`
    
    -   `"name": "string",`
        
    -   `"description": "string",`
        
    -   `"enabled": 1,`
        
    -   `"resourceGroups": [],`
        
    -   `"eventCategory": [],`
        
    -   `"source": [],`
        
    -   `"sources": [],`
        
    -   `"category": [],`
        
    -   `"subCategory": [],`
        
    -   `"severity": []`
        
    
    `},`
    
-   `"intgGuidList": [`
    
    -   `"string"`
        
    
    `],`
    
-   `"type": "Event"`
    

`}`

### Response samples

-   201
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"mcGuid": "QA42F6C8_97...",`
        
    -   `"filters": {},`
        
    -   `"intgGuidList": [],`
        
    -   `"type": "Event"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertRules/paths/~1api~1v2~1AlertRules/get)List All Alert Rules

List all alert rules in your Lacework instance by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/AlertRules`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertRules/paths/~1api~1v2~1AlertRules~1search/post)Search Alert Rules

Search alert rules by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/AlertRules/search`

To limit the returned result, optionally specify one or more filters in the request body. For more information about using filters, see the [Simple & Advanced Search section](https://docs.lacework.net/api/v2/docs/#tag/OVERVIEW).

Here are some example `body` payloads:

-   `{ "filters": [ { "field": "mcGuid", "expression": "rlike", "value": "123ABC" } ] }`
    
-   `{ "filters": [ { "field": "mcGuid", "expression": "between", "values": [ "ABC_123", "DEC_456" ] } ] }`
    
-   `{ "filters": [ { "field": "intgGuidList", "expression": "eq", "value": "ABC_123" } ] }`
    
-   `{ "filters": [ { "field": "intgGuidList", "expression": "in", "values": [ "ABC_123", "DEF_456" ] } ] }`
    
-   `{ "filters": [ { "field": "filters.name", "expression": "ilike", "value": "slack" } ] }`
    
-   `{ "filters": [ { "field": "filters.resourceGroups", "expression": "eq", "value": "ABC_123" } ] }`
    
-   `{ "filters": [ { "field": "filters.severity", "expression": "eq", "value": "5" } ] }`
    
-   `{ "filters": [ { "field": "filters.eventCategory", "expression": "eq", "value": "App" } ] }`
    
-   `{ "filters": [ { "field": "reportNotificationTypes.agentEvents", "expression": "eq", "value": "false" } ] }`
    

In the request body, optionally specify the list of fields to return in the response by specifying the list in the `returns` array.

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertRules/paths/~1api~1v2~1AlertRules~1{mcGuid}/get)Alert Rule Details

Get details about an alert rule by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/AlertRules/{mcGuid}`

Replace `{mcGuid}` with the `mcGuid` value returned for an alert rule in the response when the `GET /api/v2/AlertRules` endpoint is invoked.

##### path Parameters

<table><tbody><tr><td kind="field" title="mcGuid"><span></span><span>mcGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"mcGuid": "QA42F6C8_97...",`
        
    -   `"filters": {},`
        
    -   `"intgGuidList": [],`
        
    -   `"type": "Event"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertRules/paths/~1api~1v2~1AlertRules~1{mcGuid}/patch)Update Alert Rules

Update an alert rule by specifying parameters in the request body when invoking the following endpoint:

> `PATCH https://YourLacework.lacework.net/api/v2/AlertRules/{mcGuid}`

Replace `{mcGuid}` with the `mcGuid` value returned for an alert rule in the response when the `GET /api/v2/AlertRules` endpoint is invoked. In the request body, only specify the parameters that you want to update.

##### path Parameters

<table><tbody><tr><td kind="field" title="mcGuid"><span></span><span>mcGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>When sending a request, use this object to define the new alert rule. When included in a response, this object contains details of an alert rule. You can use these attributes when searching for existing alert rules by invoking a GET request.</p></div></div></td></tr><tr><td kind="field" title="intgGuidList"><span></span><span>intgGuidList</span></td><td><div><p><span>Array of </span><span>strings</span><span> <span>non-empty </span><span>unique</span></span></p><div><p>The alert channels for the rule to access.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": {`
    
    -   `"name": "string",`
        
    -   `"description": "string",`
        
    -   `"enabled": 1,`
        
    -   `"resourceGroups": [],`
        
    -   `"eventCategory": [],`
        
    -   `"source": [],`
        
    -   `"sources": [],`
        
    -   `"category": [],`
        
    -   `"subCategory": [],`
        
    -   `"severity": []`
        
    
    `},`
    
-   `"intgGuidList": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"mcGuid": "QA42F6C8_97...",`
        
    -   `"filters": {},`
        
    -   `"intgGuidList": [],`
        
    -   `"type": "Event"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AlertRules/paths/~1api~1v2~1AlertRules~1{mcGuid}/delete)Delete Alert Rules

Delete an alert rule by invoking the following endpoint:

> `DELETE https://YourLacework.lacework.net/api/v2/AlertRules/{mcGuid}`

Replace `{mcGuid}` with the `mcGuid` value returned for an alert rule in the response when the `GET /api/v2/AlertRules` endpoint is invoked.

##### path Parameters

<table><tbody><tr><td kind="field" title="mcGuid"><span></span><span>mcGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Alerts)Alerts

Lacework provides real-time alerts that are interactive and manageable. Each alert contains various metadata information, such as severity level, type, status, alert category, and associated tags.

You can also post a comment to an [alert's timeline](https://docs.lacework.com/console/view-alerts#timeline); or change an [alert status](https://docs.lacework.com/console/view-alerts#status) from Open to Closed.

## [](https://docs.lacework.net/api/v2/docs#tag/Alerts/paths/~1api~1v2~1Alerts/get)List Alerts

Get a list of alerts during the specified date range by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/Alerts?startTime={startTime}&endTime={endTime}`

Use the following formats to specify the `startTime` and `endTime`:

-   `yyyy-MM-dd` for example, `2022-06-28`
    
-   `yyyy-MM-ddTHH` for example, `2022-06-28T08`
    
-   `yyyy-MM-ddTHH:mm:ssZ` for example, `2022-06-28T08:00:00Z`
    
-   `yyyy-MM-ddTHH:mm:ss.SSSZ` for example, `2022-06-28T08:00:00.000Z`
    

Here is an example invocation:

> `GET https://YourLacework.lacework .net/api/v2/Alerts?startTime=2022-06-30T00:00:00Z&endTime=2022-06-30T08:00:00Z`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days.

Pagination metadata is located within the response's `paging` field, which contains information for `rows`, `totalRows`, and `urls`. The `urls` field contains the `nextPage` field with the Next Page URL. The Next Page URLs stay valid for 24 hours.

To get the next page of the result, use the entire Next Page URL and send a GET request with the two required HTTP headers: "Authorization: Bearer {YourAPIToken}" and "Content-Type: application/json".

Example:

> `GET https://YourLacework.lacework.net/api/v2/Alerts/abcxyz123...`

##### query Parameters

<table><tbody><tr><td kind="field" title="startTime"><span></span><span>startTime</span></td><td><div><p><span></span><span>string</span></p><div><p>Returns only recorded actions that occurred after this timestamp.</p></div></div></td></tr><tr><td kind="field" title="endTime"><span></span><span>endTime</span></td><td><div><p><span></span><span>string</span></p><div><p>Returns only recorded actions that occurred before this timestamp. If empty or missing, the current time is used.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 1000,`
        
    -   `"totalRows": 3120,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Alerts/paths/~1api~1v2~1Alerts~1search/post)Search Alerts

Search alerts by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Alerts/search`

Optionally specify filters in the request body. For more information about using filters, see the [Simple & Advanced Search section](https://docs.lacework.net/api/v2/docs/#tag/OVERVIEW).

For the `timeFilter` filter, these are the supported time formats:

-   `yyyy-MM-dd` for example, `2022-07-08`
    
-   `yyyy-MM-ddTHH` for example, `2022-07-08T08`
    
-   `yyyy-MM-ddTHH:mm:ssZ` for example, `2022-07-08T08:00:00Z`
    
-   `yyyy-MM-ddTHH:mm:ss.SSSZ` for example, `2022-07-08T08:00:00.000Z`
    

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

To limit the returned result, optionally specify one or more filters in the request body. These fields can be set in the filters: `alertId`, `alertType`, `severity`, `status`, `subCategory`, `category`, and `source`. In the filter, specify the field on which to filter, the `eq` operator, and the value against which the field value is compared.

You can optionally filter the returned alerts by one or more of the top-level fields. See [Filter Alerts](https://docs.lacework.com/console/filter-alerts) for the filter values.

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2022-07-08T00:00:00Z", "endTime": "2022-07-08T08:00:00Z"},` `"filters": [ { "field": "alertType", "expression": "eq", "value": "SuspiciousUserFailedLogin" } ] }`
-   `{ "timeFilter": { "startTime": "2022-07-08T00:00:00Z", "endTime": "2022-07-08T08:00:00Z"},` `"filters": [ { "field": "severity", "expression": "eq", "value": "Critical" }, { "field": "status", "expression": "eq", "value": "Open" } ],`  
    `"returns": [ "alertId", "alertName", "alertType", "alertInfo" ] }`

Pagination metadata is located within the response's `paging` field, which contains information for `rows`, `totalRows`, and `urls`. The `urls` field contains the `nextPage` field with the Next Page URL. The Next Page URLs stay valid for 24 hours.

To get the next page of the result, use the entire Next Page URL and send a GET request with the two required HTTP headers: "Authorization: Bearer {YourAPIToken}" and "Content-Type: application/json".

Example:

> `GET https://YourLacework.lacework.net/api/v2/Alerts/abcxyz123...`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 1000,`
        
    -   `"totalRows": 3120,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Alerts/paths/~1api~1v2~1Alerts~1{alertId}/get)Alert Details

Get details about an alert by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/Alerts/{alertId}?scope={scope}`

You must specify a scope, as one of these options: `Details`, `Investigation`, `Events`, `RelatedAlerts`, `Integrations`, or `Timeline`.

##### path Parameters

<table><tbody><tr><td kind="field" title="alertId"><span></span><span>alertId</span><p>required</p></td><td></td></tr></tbody></table>

##### query Parameters

<table><tbody><tr><td kind="field" title="scope"><span></span><span>scope</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"Details"</span> <span>"Investigation"</span> <span>"Events"</span> <span>"RelatedAlerts"</span> <span>"Integrations"</span> <span>"Timeline"</span></p><div><p>You must specify a scope, as one of these options.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"alertId": 813628,`
        
    -   `"startTime": "2022-06-30T00:00:00.000Z",`
        
    -   `"alertType": "CloudActivityLogIngestionFailed",`
        
    -   `"severity": "High",`
        
    -   `"endTime": "2022-06-30T01:00:00.000Z",`
        
    -   `"lastUserUpdatedTime": "",`
        
    -   `"status": "Open",`
        
    -   `"alertName": "Clone of Cloud Activity log ingestion failure detected",`
        
    -   `"alertInfo": {},`
        
    -   `"entityMap": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Alerts/paths/~1api~1v2~1Alerts~1Entities~1{alertId}/get)Alert Entities

List all entities associated with a given alert ID for which additional context is available. The entity can be any non-compliant resource, such as a machine or IP address.

##### path Parameters

<table><tbody><tr><td kind="field" title="alertId"><span></span><span>alertId</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Alerts/paths/~1api~1v2~1Alerts~1EntityDetails~1{alertId}/get)Alert Entity Details

Get details about an entity associated with a given alert ID for which additional context is available by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/Alerts/EntityDetails/{alertId}?contextEntityType={entityType}&entityValue={entityValue}`

You must specify a `contextEntityType` and `entityValue`. (Currently, additional context support is available for IpAddress entities only, so `contextEntityType` must be `Machine` or `IpAddress`.) If any item of information about this entity is not available, partial information is returned.

##### path Parameters

<table><tbody><tr><td kind="field" title="alertId"><span></span><span>alertId</span><p>required</p></td><td></td></tr></tbody></table>

##### query Parameters

<table><tbody><tr><td kind="field" title="contextEntityType"><span></span><span>contextEntityType</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"IpAddress"</span> <span>"Machine"</span></p><div><p>You must specify a context entity type from the available options. (Currently, only <code>Machine</code> and <code>IpAddress</code> is available.)</p></div></div></td></tr><tr><td kind="field" title="entityValue"><span></span><span>entityValue</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>You must specify a context entity value, such as the Machine identifier (MID) or IP address.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"isAgentInstalled": false,`
        
    -   `"isInternalIp": false,`
        
    -   `"laceworkLabs": {},`
        
    -   `"virusTotal": {},`
        
    -   `"ipAddressSummary": {},`
        
    -   `"resolvedIpInformation": {},`
        
    -   `"uniqueProcessDetails": {},`
        
    -   `"networkActivityOverview": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Alerts/paths/~1api~1v2~1Alerts~1{alertId}~1close/post)Close Alerts

Change the status of an alert to closed by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Alerts/{alertId}/close`

The body of the request should contain the reason for closing, from these options:

-   Other
-   False positive
-   Not enough information
-   Malicious and have resolution in place
-   Expected because of routine testing
-   Expected behavior

If you choose `Other`, the message field is required and should contain a brief explanation of why the alert is closed.

Note that a closed alert cannot be reopened.

For details about alert statuses, see [Status](https://docs.lacework.com/console/view-alerts#status).

##### path Parameters

<table><tbody><tr><td kind="field" title="alertId"><span></span><span>alertId</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="reason"><span></span><span>reason</span><p>required</p></td><td><div><p><span></span><span>number</span></p><p><span>Enum:</span> <span>0</span> <span>1</span> <span>2</span> <span>3</span> <span>4</span> <span>5</span></p><div><p>0 - Other</p><p>1 - False positive</p><p>2 - Not enough information</p><p>3 - Malicious and have resolution in place</p><p>4 - Expected because of routine testing</p><p>5 - Expected behavior</p></div></div></td></tr><tr><td kind="field" title="comment"><span></span><span>comment</span></td><td><div><p><span></span><span>string</span></p><div><p>If you choose <code>0</code> (<code>Other</code>), the comment field is required and should contain a brief explanation of why the alert is closed.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"reason": 0,`
    
-   `"comment": "string"`
    

`}`

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AuditLogs)Audit Logs

Audit logs let you view the history of all actions performed within a Lacework account so you know who made changes to the system and when. For example, you can see who suppressed certain alerts, what time an authentication setting was modified, etc. For more information, see [Audit Logs](https://docs.lacework.com/audit-logs).

## [](https://docs.lacework.net/api/v2/docs#tag/AuditLogs/paths/~1api~1v2~1AuditLogs/get)Audit Logs

Get audit logs by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/AuditLogs`

Optionally specify the `startTime` and `endTime` time range filters using the following formats:

-   `yyyy-MM-dd` for example, `2020-12-18`
    
-   `yyyy-MM-ddTHH` for example, `2020-12-18T08`
    
-   `yyyy-MM-ddTHH:mm:ssZ` for example, `2020-12-18T08:00:00Z`
    
-   `yyyy-MM-ddTHH:mm:ss.SSSZ` for example, `2020-12-18T08:00:00.000Z`
    

To use the current time as the end time, exclude the endTime parameter.

Here is an example invocation:

> `GET https://YourLacework.lacework.net/api/v2/AuditLogs?startTime=2020-12-11T08:00:00Z&endTime=2020-12-18T08:00:00Z`

##### query Parameters

<table><tbody><tr><td kind="field" title="startTime"><span></span><span>startTime</span></td><td><div><p><span></span><span>string</span></p><div><p>Returns only recorded actions that occurred after this timestamp.</p></div></div></td></tr><tr><td kind="field" title="endTime"><span></span><span>endTime</span></td><td><div><p><span></span><span>string</span></p><div><p>Returns only recorded actions that occurred before this timestamp. If empty or missing, the current time is used.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/AuditLogs/paths/~1api~1v2~1AuditLogs~1search/post)Search Audit Logs

Search the audit logs by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/AuditLogs/search`

Optionally specify filters in the request body. For more information about using filters, see the [Simple & Advanced Search section](https://docs.lacework.net/api/v2/docs/#tag/OVERVIEW).

For the `timeFilter` filter, these are the supported time formats:

-   `yyyy-MM-dd` for example, `2020-12-18`
    
-   `yyyy-MM-ddTHH` for example, `2020-12-18T08`
    
-   `yyyy-MM-ddTHH:mm:ssZ` for example, `2020-12-18T08:00:00Z`
    
-   `yyyy-MM-ddTHH:mm:ss.SSSZ`, for example, `2020-12-18T08:00:00.000Z`
    

To use the current time as the end time, exclude the endTime field.

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

Filters in the request body

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/CloudAccounts)Cloud Accounts

Cloud accounts are integrations between Lacework and cloud providers such as Amazon Web Services, Microsoft Azure, and Google Cloud Platform.

## [](https://docs.lacework.net/api/v2/docs#tag/CloudAccounts/paths/~1api~1v2~1CloudAccounts/post)Create Cloud Accounts

Create a cloud account by specifying parameters in the request body when invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/CloudAccounts`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="name"><span></span><span>name</span><p>required</p></td><td><div><p><span></span><span>string</span><span> (Name) </span><span><span>non-empty </span></span><span>(?!^ +$)^.+$</span></p><div><p>When sending a request, use this attribute to specify an integration’s name. When included in a response, this attribute returns the specified integration’s name.</p></div></div></td></tr><tr><td kind="field" title="type"><span></span><span>type</span><p>required</p></td><td><div><p><span></span><span>string</span><span> (Type)</span></p><div><p>When sending a request, use this attribute to specify the type of integration, from the following options. When included in a response, this attribute returns the specified integration’s type.</p></div><p><label>AwsCfg</label></p></div></td></tr><tr><td kind="field" title="enabled"><span></span><span>enabled</span><p>required</p></td><td><div><p><span></span><span>number</span><span> (Enabled) </span><span><span>[ 0 .. 1 ]</span></span></p><div><p>When sending a request, use this attribute to enable or disable an integration. When included in a response, returns <code>1</code> for an enabled integration or <code>0</code> for a disabled integration.</p></div></div></td></tr><tr><td kind="field" title="data"><span></span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"name": "string",`
    
-   `"type": "AwsCfg",`
    
-   `"enabled": 1,`
    
-   `"data": {`
    
    -   `"awsAccountId": "string",`
        
    -   `"crossAccountCredentials": {}`
        
    
    `}`
    

`}`

### Response samples

-   201
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"createdOrUpdatedBy": "user@example.com",`
        
    -   `"createdOrUpdatedTime": "2021-02-08T08:28:18Z",`
        
    -   `"enabled": 1,`
        
    -   `"intgGuid": "LWXYZ...",`
        
    -   `"isOrg": 0,`
        
    -   `"name": "Support",`
        
    -   `"props": "{object}",`
        
    -   `"state": "{object}",`
        
    -   `"type": "AwsCfg",`
        
    -   `"data": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/CloudAccounts/paths/~1api~1v2~1CloudAccounts/get)List All Cloud Accounts

Get a list of cloud accounts for the current user by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/CloudAccounts`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/CloudAccounts/paths/~1api~1v2~1CloudAccounts~1{type}/get)List Cloud Accounts by Type

Get a list of cloud accounts of the specified type by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/CloudAccounts/{type}`

Here is an example invocation:

> `GET https://YourLacework.lacework.net/api/v2/CloudAccounts/AwsCfg`

##### path Parameters

<table><tbody><tr><td kind="field" title="type"><span></span><span>type</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"AwsCfg"</span> <span>"AwsCtSqs"</span> <span>"AwsEksAudit"</span> <span>"AwsUsGovCfg"</span> <span>"AwsUsGovCtSqs"</span> <span>"AzureAlSeq"</span> <span>"AzureCfg"</span> <span>"GcpAtSes"</span> <span>"GcpCfg"</span></p></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/CloudAccounts/paths/~1api~1v2~1CloudAccounts~1search/post)Search Cloud Accounts

Search cloud accounts by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/CloudAccounts/search`

To limit the returned result, optionally specify one or more filters in the request body. For more information about using filters, see the [Simple & Advanced Search section](https://docs.lacework.net/api/v2/docs/#tag/OVERVIEW).

In the request body, optionally specify the list of fields to return in the response by specifying the list in the `returns` array, for example, `"returns":[ "name", "type", "enabled" ]`.

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/CloudAccounts/paths/~1api~1v2~1CloudAccounts~1{intgGuid}/get)Cloud Accounts Details

Get details about a cloud account by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/CloudAccounts/{intgGuid}`

##### path Parameters

<table><tbody><tr><td kind="field" title="intgGuid"><span></span><span>intgGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"createdOrUpdatedBy": "user@example.com",`
        
    -   `"createdOrUpdatedTime": "2021-02-08T08:28:18Z",`
        
    -   `"enabled": 1,`
        
    -   `"intgGuid": "LWXYZ...",`
        
    -   `"isOrg": 0,`
        
    -   `"name": "Support",`
        
    -   `"props": "{object}",`
        
    -   `"state": "{object}",`
        
    -   `"type": "AwsCfg",`
        
    -   `"data": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/CloudAccounts/paths/~1api~1v2~1CloudAccounts~1{intgGuid}/patch)Update Cloud Accounts

Update a cloud account by specifying parameters in the request body when invoking the following endpoint:

> `PATCH https://YourLacework.lacework.net/api/v2/CloudAccounts/{intgGuid}`

In the request body, only specify the parameters that you want to update, for example, `{ "enabled" : 0 }`.

##### path Parameters

<table><tbody><tr><td kind="field" title="intgGuid"><span></span><span>intgGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="name"><span></span><span>name</span></td><td><div><p><span></span><span>string</span><span> (Name) </span><span><span>non-empty </span></span><span>(?!^ +$)^.+$</span></p><div><p>When sending a request, use this attribute to specify an integration’s name. When included in a response, this attribute returns the specified integration’s name.</p></div></div></td></tr><tr><td kind="field" title="type"><span></span><span>type</span></td><td><div><p><span></span><span>string</span><span> (Type)</span></p><div><p>When sending a request, use this attribute to specify the type of integration, from the following options. When included in a response, this attribute returns the specified integration’s type.</p></div><p><label>AwsCfg</label></p></div></td></tr><tr><td kind="field" title="enabled"><span></span><span>enabled</span></td><td><div><p><span></span><span>number</span><span> (Enabled) </span><span><span>[ 0 .. 1 ]</span></span></p><div><p>When sending a request, use this attribute to enable or disable an integration. When included in a response, returns <code>1</code> for an enabled integration or <code>0</code> for a disabled integration.</p></div></div></td></tr><tr><td kind="field" title="data"><span></span></td><td></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"name": "string",`
    
-   `"type": "AwsCfg",`
    
-   `"enabled": 1,`
    
-   `"data": {`
    
    -   `"awsAccountId": "string",`
        
    -   `"crossAccountCredentials": {}`
        
    
    `}`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"createdOrUpdatedBy": "user@example.com",`
        
    -   `"createdOrUpdatedTime": "2021-02-08T08:28:18Z",`
        
    -   `"enabled": 1,`
        
    -   `"intgGuid": "LWXYZ...",`
        
    -   `"isOrg": 0,`
        
    -   `"name": "Support",`
        
    -   `"props": "{object}",`
        
    -   `"state": "{object}",`
        
    -   `"type": "AwsCfg",`
        
    -   `"data": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/CloudAccounts/paths/~1api~1v2~1CloudAccounts~1{intgGuid}/put)Update Cloud Accounts

Update a cloud account by specifying the entire object in the request body when invoking the following endpoint:

> `PUT https://YourLacework.lacework.net/api/v2/CloudAccounts/{intgGuid}`

In the request body, specify the entire object that you want to update, for example,

> `{"name": "string","type": "AwsCfg", "enabled": 1, "data": { "awsAccountId": "string", "crossAccountCredentials": {"externalId": "string", "roleArn": "string"}} }`.

##### path Parameters

<table><tbody><tr><td kind="field" title="intgGuid"><span></span><span>intgGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="name"><span></span><span>name</span><p>required</p></td><td><div><p><span></span><span>string</span><span> (Name) </span><span><span>non-empty </span></span><span>(?!^ +$)^.+$</span></p><div><p>When sending a request, use this attribute to specify an integration’s name. When included in a response, this attribute returns the specified integration’s name.</p></div></div></td></tr><tr><td kind="field" title="type"><span></span><span>type</span><p>required</p></td><td><div><p><span></span><span>string</span><span> (Type)</span></p><div><p>When sending a request, use this attribute to specify the type of integration, from the following options. When included in a response, this attribute returns the specified integration’s type.</p></div><p><label>AwsCfg</label></p></div></td></tr><tr><td kind="field" title="enabled"><span></span><span>enabled</span><p>required</p></td><td><div><p><span></span><span>number</span><span> (Enabled) </span><span><span>[ 0 .. 1 ]</span></span></p><div><p>When sending a request, use this attribute to enable or disable an integration. When included in a response, returns <code>1</code> for an enabled integration or <code>0</code> for a disabled integration.</p></div></div></td></tr><tr><td kind="field" title="data"><span></span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"name": "string",`
    
-   `"type": "AwsCfg",`
    
-   `"enabled": 1,`
    
-   `"data": {`
    
    -   `"awsAccountId": "string",`
        
    -   `"crossAccountCredentials": {}`
        
    
    `}`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"createdOrUpdatedBy": "user@example.com",`
        
    -   `"createdOrUpdatedTime": "2021-02-08T08:28:18Z",`
        
    -   `"enabled": 1,`
        
    -   `"intgGuid": "LWXYZ...",`
        
    -   `"isOrg": 0,`
        
    -   `"name": "Support",`
        
    -   `"props": "{object}",`
        
    -   `"state": "{object}",`
        
    -   `"type": "AwsCfg",`
        
    -   `"data": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/CloudAccounts/paths/~1api~1v2~1CloudAccounts~1{intgGuid}/delete)Delete Cloud Accounts

Delete a cloud account by invoking the following endpoint:

> `DELETE https://YourLacework.lacework.net/api/v2/CloudAccounts/{intgGuid}`

##### path Parameters

<table><tbody><tr><td kind="field" title="intgGuid"><span></span><span>intgGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/CloudActivities)Cloud Activities

Get information about cloud activities for the integrated AWS cloud accounts in your Lacework instance.

## [](https://docs.lacework.net/api/v2/docs#tag/CloudActivities/paths/~1api~1v2~1CloudActivities/get)Cloud Activities

Get cloud activity details by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/CloudActivities`

Optionally filter by specifying the `startTime` and `endTime` of a time range using the following formats:

-   `yyyy-MM-dd` for example, `2020-12-18`
    
-   `yyyy-MM-ddTHH` for example, `2020-12-18T08`
    
-   `yyyy-MM-ddTHH:mm:ssZ` for example, `2020-12-18T08:00:00Z`
    
-   `yyyy-MM-ddTHH:mm:ss.SSSZ` for example, `2020-12-18T08:00:00.000Z`
    

To use the current time as the end time, exclude the endTime parameter.

Here is an example invocation:

> `GET https://YourLacework.lacework.net/api/v2/CloudActivities?startTime=2020-12-11T08:00:00Z&endTime=2020-12-18T08:00:00Z`

To use the current time as the end time, exclude the endTime parameter.

##### query Parameters

<table><tbody><tr><td kind="field" title="startTime"><span></span><span>startTime</span></td><td><div><p><span></span><span>string</span></p><div><p>Returns only recorded actions that occurred after this timestamp.</p></div></div></td></tr><tr><td kind="field" title="endTime"><span></span><span>endTime</span></td><td><div><p><span></span><span>string</span></p><div><p>Returns only recorded actions that occurred before this timestamp. If empty or missing, the current time is used.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 5020,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/CloudActivities/paths/~1api~1v2~1CloudActivities~1search/post)Search Cloud Activities

Search cloud activities by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/CloudActivities/search`

Optionally specify filters in the request body. For more information about using filters, see the [Simple & Advanced Search section](https://docs.lacework.net/api/v2/docs/#tag/OVERVIEW).

For the `timeFilter` filter, these are the supported time formats:

-   `yyyy-MM-dd` for example, `2021-12-18`
    
-   `yyyy-MM-ddTHH` for example, `2021-12-18T08`
    
-   `yyyy-MM-ddTHH:mm:ssZ` for example, `2021-12-18T08:00:00Z`
    
-   `yyyy-MM-ddTHH:mm:ss.SSSZ` for example, `2021-12-18T08:00:00.000Z`
    

The `rlike` and `not_rlike` operators are useful for filtering results. For example, the following expression limits results to the `CreateTags` API:

> `"filters": [ { "expression": "rlike", "field": "entityMap.API", "value": ".CreateTags." } ]`

Here is another example that shows how to limit results to those with the numeric pattern specified as the resource ID:

> `"filters": [ { "expression": "rlike", "field": "entityMap.Resource", "value": ".3\.0\.529\.0." } ]`

Here are some additional example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-12-11T00:00:00Z", "endTime": "2021-12-12T00:00:00Z"},` `"filters": [ { "field": "eventType", "expression": "eq", "value": "NewUser" } ] }`
-   `{ "timeFilter": { "startTime": "2021-12-11T00:00:00Z", "endTime": "2021-12-12T00:00:00Z"},` `"filters": [ { "field": "eventType", "expression": "eq", "value": "NewUser" },`  
    `{ "field": "eventModel", "expression": "eq", "value": "AwsApiTracker" } ],`  
    `"returns":[ "startTime", "endTime", "eventType", "eventActor", "eventModel" ] }`

To use the current time as the end time, exclude the endTime field.

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 5020,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Configs)Configurations

Get information about compliance configurations.

## [](https://docs.lacework.net/api/v2/docs#tag/Configs/paths/~1api~1v2~1Configs~1ComplianceEvaluations~1search/post)Search Compliance Evaluations

Search for compliance evaluations (with details such as compliance status, violated resources, reason, recommendation, account info, etc.) for a specified cloud provider within the last 90 days by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Configs/ComplianceEvaluations/search`

The search results include details about compliance violations identified by cloud assessments for all supported and configured cloud provider types: AWS, Azure, and GCP.

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days.

You must specify a dataset. The possible datasets are `AwsCompliance`, `AzureCompliance`, `GcpCompliance`, and `K8sCompliance`. You can optionally filter the compliance evaluations by report time, account, section, ID, and more. For more information, see [CLOUD\_COMPLIANCE\_V View](https://docs.lacework.com/cloudcompliancev-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"dataset": "AwsCompliance" }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "status", "expression": "eq", "value": "NonCompliant" }, { "field": "account.AccountId", "expression": "eq", "value": "812212113623" } ],`  
    `"returns": [ "account", "id", "recommendation", "severity", "status" ],`  
    `"dataset": "AzureCompliance" }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr><tr><td kind="field" title="dataset"><span></span><span>dataset</span><p>required</p></td><td><div><p><span></span><span>any</span></p><p><span>Enum:</span> <span>"AwsCompliance"</span> <span>"AzureCompliance"</span> <span>"GcpCompliance"</span> <span>"K8sCompliance"</span></p></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `],`
    
-   `"dataset": "AwsCompliance"`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 9838,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Configs/paths/~1api~1v2~1Configs~1AzureSubscriptions/get)Azure Subscriptions

Get a list of Azure subscription IDs for an entire account or for a specific Azure tenant.

To list all Azure subscription IDs for an account, invoke the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/Configs/AzureSubscriptions`

To get a list of Azure subscription IDs for a specific tenant, pass the tenant ID as a parameter to the endpoint:

> `GET https://YourLacework.lacework.net/api/v2/Configs/AzureSubscriptions?tenantId={tenantId}`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Configs/paths/~1api~1v2~1Configs~1GcpProjects/get)GCP Projects

Get a list of GCP project IDs for an entire account or for a specific organization.

To list all GCP project IDs for an account, invoke the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/Configs/GcpProjects`

To get a list of GCP project IDs for a specific organization, pass the organization ID as a parameter to the endpoint:

> `GET https://YourLacework.lacework.net/api/v2/Configs/GcpProjects?orgId={orgId}`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ContainerRegistries)Container Registries

Lacework provides the ability to assess, identify, and report vulnerabilities found in the operating system software packages in a Docker container image. After integrating a container registry in Lacework, Lacework finds all container images in the registry repositories, assesses those container images for software packages with known vulnerabilities, and reports them.

In addition to online container registry integrations, Lacework helps secure containers that are not connected to the Internet through the use of [proxy scanners](https://docs.lacework.com/onboarding/category/integrate-proxy-scanner) and [inline scanners](https://docs.lacework.com/onboarding/category/integrate-inline-scanner). Container registries that are of type proxy scanner (`PROXY_SCANNER`) or inline scanner (`INLINE_SCANNER`) may not include all fields shown below, such as `state`.

**Note:** If the `state` property is missing for any type other than `PROXY_SCANNER` or `INLINE_SCANNER`, the state of the integration is **Pending**.

## [](https://docs.lacework.net/api/v2/docs#tag/ContainerRegistries/paths/~1api~1v2~1ContainerRegistries/post)Create Container Registries

Create a container registry by specifying parameters in the request body when invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/ContainerRegistries`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="name"><span></span><span>name</span><p>required</p></td><td><div><p><span></span><span>string</span><span> (Name) </span><span><span>non-empty </span></span><span>(?!^ +$)^.+$</span></p><div><p>When sending a request, use this attribute to specify an integration’s name. When included in a response, this attribute returns the specified integration’s name.</p></div></div></td></tr><tr><td kind="field" title="type"><span></span><span>type</span><p>required</p></td><td><div><p><span></span><span>string</span><span> (Type)</span></p><div><p>When sending a request, use this attribute to specify the type of integration, from the following options. When included in a response, this attribute returns the specified integration’s type.</p></div><p><label>ContVulnCfg</label></p></div></td></tr><tr><td kind="field" title="enabled"><span></span><span>enabled</span><p>required</p></td><td><div><p><span></span><span>number</span><span> (Enabled) </span><span><span>[ 0 .. 1 ]</span></span></p><div><p>When sending a request, use this attribute to enable or disable an integration. When included in a response, returns <code>1</code> for an enabled integration or <code>0</code> for a disabled integration.</p></div></div></td></tr><tr><td kind="field" title="data"><span></span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"name": "string",`
    
-   `"type": "ContVulnCfg",`
    
-   `"enabled": 1,`
    
-   `"data": {`
    
    -   `"crossAccountCredentials": {},`
        
    -   `"awsAuthType": "AWS_IAM",`
        
    -   `"registryType": "AWS_ECR",`
        
    -   `"registryDomain": "string",`
        
    -   `"limitNumImg": 5,`
        
    -   `"limitByRep": [ ],`
        
    -   `"nonOsPackageEval": true,`
        
    -   `"limitByTag": [ ],`
        
    -   `"limitByLabel": [ ]`
        
    
    `}`
    

`}`

### Response samples

-   201
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"createdOrUpdatedBy": "user@example.com",`
        
    -   `"createdOrUpdatedTime": "2021-02-08T08:28:18Z",`
        
    -   `"enabled": 1,`
        
    -   `"intgGuid": "LWXYZ...",`
        
    -   `"isOrg": 0,`
        
    -   `"name": "Support",`
        
    -   `"props": "{object}",`
        
    -   `"state": "{object}",`
        
    -   `"type": "ContVulnCfg",`
        
    -   `"data": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ContainerRegistries/paths/~1api~1v2~1ContainerRegistries/get)List All Container Registries

Get a list of container registries for the current user by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/ContainerRegistries`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ContainerRegistries/paths/~1api~1v2~1ContainerRegistries~1{type}~1{subtype}/get)List Container Registries by Type

Get a list of container registries of the specified type by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/ContainerRegistries/{type}/{subtype}`

Here is an example invocation:

> `GET https://YourLacework.lacework.net/api/v2/ContainerRegistries/ContVulnCfg/AWS_ECR`

##### path Parameters

<table><tbody><tr><td kind="field" title="type"><span></span><span>type</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Value:</span> <span>"ContVulnCfg"</span></p></div></td></tr><tr><td kind="field" title="subtype"><span></span><p>required</p></td><td><div><p><span></span><span>ContVulnCfg (string)</span><span> (ContainerRegistriesSubtype)</span></p><div><p>Container Registry Subtype</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ContainerRegistries/paths/~1api~1v2~1ContainerRegistries~1search/post)Search Container Registries

Search container registries by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/ContainerRegistries/search`

To limit the returned result, optionally specify one or more filters in the request body. For more information about using filters, see the [Simple & Advanced Search section](https://docs.lacework.net/api/v2/docs/#tag/OVERVIEW).

In the request body, optionally specify the list of fields to return in the response by specifying the list in the `returns` array, for example, `"returns":[ "name", "type", "enabled" ]`.

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ContainerRegistries/paths/~1api~1v2~1ContainerRegistries~1{intgGuid}~1mapPolicies/post)Map policies to Container Registries

Map specific policies to a container registry by invoking the following endpoint: `POST https://YourLacework.lacework.net/api/v2/ContainerRegistries/{intgGuid}/mapPolicies`

##### path Parameters

<table><tbody><tr><td kind="field" title="intgGuid"><span></span><span>intgGuid</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>The container registry's ID.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="evaluate"><span></span><span>evaluate</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Set to <code>True</code> if you want to evaluate all policies for this integration. Otherwise, set to <code>False</code>.</p></div></div></td></tr><tr><td kind="field" title="policyGuids"><span></span><span>policyGuids</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>A list of all policy IDs to map to this integration.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"evaluate": true,`
    
-   `"policyGuids": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"createdOrUpdatedBy": "user@example.com",`
        
    -   `"createdOrUpdatedTime": "2021-02-08T08:28:18Z",`
        
    -   `"enabled": 1,`
        
    -   `"intgGuid": "LWXYZ...",`
        
    -   `"isOrg": 0,`
        
    -   `"name": "Support",`
        
    -   `"props": "{object}",`
        
    -   `"state": "{object}",`
        
    -   `"type": "ContVulnCfg",`
        
    -   `"data": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ContainerRegistries/paths/~1api~1v2~1ContainerRegistries~1{intgGuid}/get)Container Registry Details

Get details about a container registry by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/ContainerRegistries/{intgGuid}`

##### path Parameters

<table><tbody><tr><td kind="field" title="intgGuid"><span></span><span>intgGuid</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>The container registry's ID.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"createdOrUpdatedBy": "user@example.com",`
        
    -   `"createdOrUpdatedTime": "2021-02-08T08:28:18Z",`
        
    -   `"enabled": 1,`
        
    -   `"intgGuid": "LWXYZ...",`
        
    -   `"isOrg": 0,`
        
    -   `"name": "Support",`
        
    -   `"props": "{object}",`
        
    -   `"state": "{object}",`
        
    -   `"type": "ContVulnCfg",`
        
    -   `"data": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ContainerRegistries/paths/~1api~1v2~1ContainerRegistries~1{intgGuid}/patch)Update Container Registries

Update a container registry by specifying parameters in the request body when invoking the following endpoint:

> `PATCH https://YourLacework.lacework.net/api/v2/ContainerRegistries/{intgGuid}`

In the request body, only specify the parameters that you want to update, for example, `{ "enabled" : 0 }`.

##### path Parameters

<table><tbody><tr><td kind="field" title="intgGuid"><span></span><span>intgGuid</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>The container registry's ID.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="name"><span></span><span>name</span></td><td><div><p><span></span><span>string</span><span> (Name) </span><span><span>non-empty </span></span><span>(?!^ +$)^.+$</span></p><div><p>When sending a request, use this attribute to specify an integration’s name. When included in a response, this attribute returns the specified integration’s name.</p></div></div></td></tr><tr><td kind="field" title="type"><span></span><span>type</span></td><td><div><p><span></span><span>string</span><span> (Type)</span></p><div><p>When sending a request, use this attribute to specify the type of integration, from the following options. When included in a response, this attribute returns the specified integration’s type.</p></div><p><label>ContVulnCfg</label></p></div></td></tr><tr><td kind="field" title="enabled"><span></span><span>enabled</span></td><td><div><p><span></span><span>number</span><span> (Enabled) </span><span><span>[ 0 .. 1 ]</span></span></p><div><p>When sending a request, use this attribute to enable or disable an integration. When included in a response, returns <code>1</code> for an enabled integration or <code>0</code> for a disabled integration.</p></div></div></td></tr><tr><td kind="field" title="data"><span></span></td><td></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"name": "string",`
    
-   `"type": "ContVulnCfg",`
    
-   `"enabled": 1,`
    
-   `"data": {`
    
    -   `"crossAccountCredentials": {},`
        
    -   `"awsAuthType": "AWS_IAM",`
        
    -   `"registryType": "AWS_ECR",`
        
    -   `"registryDomain": "string",`
        
    -   `"limitNumImg": 5,`
        
    -   `"limitByRep": [ ],`
        
    -   `"nonOsPackageEval": true,`
        
    -   `"limitByTag": [ ],`
        
    -   `"limitByLabel": [ ]`
        
    
    `}`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"createdOrUpdatedBy": "user@example.com",`
        
    -   `"createdOrUpdatedTime": "2021-02-08T08:28:18Z",`
        
    -   `"enabled": 1,`
        
    -   `"intgGuid": "LWXYZ...",`
        
    -   `"isOrg": 0,`
        
    -   `"name": "Support",`
        
    -   `"props": "{object}",`
        
    -   `"state": "{object}",`
        
    -   `"type": "ContVulnCfg",`
        
    -   `"data": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ContainerRegistries/paths/~1api~1v2~1ContainerRegistries~1{intgGuid}/delete)Delete Container Registries

Delete a container registry by invoking the following endpoint:

> `DELETE https://YourLacework.lacework.net/api/v2/ContainerRegistries/{intgGuid}`

##### path Parameters

<table><tbody><tr><td kind="field" title="intgGuid"><span></span><span>intgGuid</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>The container registry's ID.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ContractInfo)Contract Info

Get Lacework contract information.

## [](https://docs.lacework.net/api/v2/docs#tag/ContractInfo/paths/~1api~1v2~1ContractInfo/get)Contract Info

Return contract details about the Lacework licenses found in the Lacework instance by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/ContractInfo`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/DataExportRules)Data Export Rules

S3 data export allows you to export data collected from your Lacework account and send it to an S3 bucket of your choice. You can extend Lacework processed/normalized data to report/visualize alone or combine with other business/security data to get insights and make meaningful business decisions.

## [](https://docs.lacework.net/api/v2/docs#tag/DataExportRules/paths/~1api~1v2~1DataExportRules/post)Create Data Export Rules

Create a data export rule by specifying parameters in the request body when invoking the following endpoint:

`POST https://YourLacework.lacework.net/api/v2/DataExportRules`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span><p>required</p></td><td><div><p><span></span><span>object</span></p><div><p>When sending a request, use this object to define the new data export rule. When included in a response, this object contains details of a data export rule.<br>You can use these attributes when searching for existing data export rules by invoking a POST request.</p></div></div></td></tr><tr><td kind="field" title="intgGuidList"><span></span><span>intgGuidList</span><p>required</p></td><td><div><p><span>Array of </span><span>strings</span><span> <span>non-empty </span><span>unique</span></span></p><div><p>The alert channels for the rule to use.</p></div></div></td></tr><tr><td kind="field" title="type"><span></span><span>type</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Value:</span> <span>"Dataexport"</span></p><div><p>The data export rule's type such as <code>Dataexport</code>.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": {`
    
    -   `"name": "string",`
        
    -   `"description": "string",`
        
    -   `"enabled": 1,`
        
    -   `"profileVersions": []`
        
    
    `},`
    
-   `"intgGuidList": [`
    
    -   `"string"`
        
    
    `],`
    
-   `"type": "Dataexport"`
    

`}`

### Response samples

-   201
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"mcGuid": "QA42F6C8_97...",`
        
    -   `"filters": {},`
        
    -   `"intgGuidList": [],`
        
    -   `"type": "Dataexport"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/DataExportRules/paths/~1api~1v2~1DataExportRules/get)List All Data Export Rules

List all data export rules in your Lacework Application by invoking the following endpoint:

`GET https://YourLacework.lacework.net/api/v2/DataExportRules`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/DataExportRules/paths/~1api~1v2~1DataExportRules~1search/post)Search Data Export Rules

Search data export rules by invoking the following endpoint:

`POST https://YourLacework.lacework.net/api/v2/DataExportRules/search`

To limit the returned result, optionally specify one or more filters in the request body.

Here are some example `body` payloads:

-   `{ "filters": [ { "field": "mcGuid", "expression": "rlike", "value": "123ABC" } ] }`
    
-   `{ "filters": [ { "field": "mcGuid", "expression": "between", "values": [ "ABC_123", "DEC_456" ] } ] }`
    
-   `{ "filters": [ { "field": "intgGuidList", "expression": "eq", "value": "ABC_123" } ] }`
    
-   `{ "filters": [ { "field": "intgGuidList", "expression": "in", "values": [ "ABC_123", "DEF_456" ] } ] }`
    
-   `{ "filters": [ { "field": "filters.name", "expression": "ilike", "value": "slack" } ] }`
    
-   `{ "filters": [ { "field": "filters.profileVersions", "expression": "eq", "value": "V1" } ] }`
    

In the request body, optionally specify the list of fields to return in the response by specifying the list in the `returns` array.

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/DataExportRules/paths/~1api~1v2~1DataExportRules~1{mcGuid}/get)Data Export Rule Details

Get details about a data export rule by invoking the following endpoint:

`GET https://YourLacework.lacework.net/api/v2/DataExportRules/{mcGuid}`

Replace `{mcGuid}` with the `mcGuid` value returned for a data export rule in the response when the `GET /api/v2/DataExportRules` endpoint is invoked.

##### path Parameters

<table><tbody><tr><td kind="field" title="mcGuid"><span></span><span>mcGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"mcGuid": "QA42F6C8_97...",`
        
    -   `"filters": {},`
        
    -   `"intgGuidList": [],`
        
    -   `"type": "Dataexport"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/DataExportRules/paths/~1api~1v2~1DataExportRules~1{mcGuid}/patch)Update Data Export Rules

Update a data export rule by specifying parameters in the request body when invoking the following endpoint:

`PATCH https://YourLacework.lacework.net/api/v2/DataExportRules/{mcGuid}`

Replace `{mcGuid}` with the `mcGuid` value returned for a data export rule in the response when the `GET /api/v2/DataExportRules` endpoint is invoked.

In the request body, only specify the parameters that you want to update, for example, `{ "enabled" : 0 }`.

##### path Parameters

<table><tbody><tr><td kind="field" title="mcGuid"><span></span><span>mcGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>When sending a request, use this object to define the new data export rule. When included in a response, this object contains details of a data export rule.<br>You can use these attributes when searching for existing data export rules by invoking a POST request.</p></div></div></td></tr><tr><td kind="field" title="intgGuidList"><span></span><span>intgGuidList</span></td><td><div><p><span>Array of </span><span>strings</span><span> <span>non-empty </span><span>unique</span></span></p><div><p>The alert channels for the rule to use.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": {`
    
    -   `"name": "string",`
        
    -   `"description": "string",`
        
    -   `"enabled": 1,`
        
    -   `"profileVersions": []`
        
    
    `},`
    
-   `"intgGuidList": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"mcGuid": "QA42F6C8_97...",`
        
    -   `"filters": {},`
        
    -   `"intgGuidList": [],`
        
    -   `"type": "Dataexport"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/DataExportRules/paths/~1api~1v2~1DataExportRules~1{mcGuid}/put)Update Data Export Rules

Update a data export rule by specifying the entire object in the request body when invoking the following endpoint:

`PUT https://YourLacework.lacework.net/api/v2/DataExportRules/{mcGuid}`

In the request body, specify the entire object that you want to update, for example,

> `{"mcGuid": "string", "filters": {"name": "string", "description": "string", "enabled": 1, "profileVersions": ["V1"]}, "intgGuidList": ["string"], "type": "Dataexport"}`.

##### path Parameters

<table><tbody><tr><td kind="field" title="mcGuid"><span></span><span>mcGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span><p>required</p></td><td><div><p><span></span><span>object</span></p><div><p>When sending a request, use this object to define the new data export rule. When included in a response, this object contains details of a data export rule.<br>You can use these attributes when searching for existing data export rules by invoking a POST request.</p></div></div></td></tr><tr><td kind="field" title="intgGuidList"><span></span><span>intgGuidList</span><p>required</p></td><td><div><p><span>Array of </span><span>strings</span><span> <span>non-empty </span><span>unique</span></span></p><div><p>The alert channels for the rule to use.</p></div></div></td></tr><tr><td kind="field" title="type"><span></span><span>type</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Value:</span> <span>"Dataexport"</span></p><div><p>The data export rule's type such as <code>Dataexport</code>.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": {`
    
    -   `"name": "string",`
        
    -   `"description": "string",`
        
    -   `"enabled": 1,`
        
    -   `"profileVersions": []`
        
    
    `},`
    
-   `"intgGuidList": [`
    
    -   `"string"`
        
    
    `],`
    
-   `"type": "Dataexport"`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"mcGuid": "QA42F6C8_97...",`
        
    -   `"filters": {},`
        
    -   `"intgGuidList": [],`
        
    -   `"type": "Dataexport"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/DataExportRules/paths/~1api~1v2~1DataExportRules~1{mcGuid}/delete)Delete DataExportRules

Delete a data export rule by invoking the following endpoint:

`DELETE https://YourLacework.lacework.net/api/v2/DataExportRules/{mcGuid}`

##### path Parameters

<table><tbody><tr><td kind="field" title="mcGuid"><span></span><span>mcGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Datasources)Datasources

Get schema details for all datasources that you can query using LQL.

## [](https://docs.lacework.net/api/v2/docs#tag/Datasources/paths/~1api~1v2~1Datasources/get)List All Datasources

List all available datasources in your Lacework instance by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/Datasources`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Datasources/paths/~1api~1v2~1Datasources~1{datasource}/get)Datasource Details

Get details about a single datasource by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/Datasources/{datasource}`

Replace `{datasource}` with the `name` value returned for a datasource in the response when invoking the following endpoint: `GET /api/v2/Datasources`.

##### path Parameters

<table><tbody><tr><td kind="field" title="datasource"><span></span><span>datasource</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"name": "LW_DATASOURCE_1",`
        
    -   `"description": "Details about datasource",`
        
    -   `"resultSchema": [],`
        
    -   `"sourceRelationships": []`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Datasources/paths/~1api~1v2~1Datasources~1search/post)Search Datasources

Search for datasources by specifying parameters in the request body when invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Datasources/search`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p><p>To use wildcards with the <code>LIKE</code>, <code>ILIKE</code> <code>NOT_LIKE</code> OR <code>NOT_ILIKE</code> filters, use the % symbol to match any string. This allows you to perform more flexible and broad searches for text data.</p><ul><li><code>%</code> represents a wildcard to match zero or more characters</li><li><code>_</code> (underscore) represents a wildcard match for a single character</li></ul></div></div></td></tr><tr><td colspan="2"><div><p>Array</p><div><table><tbody><tr><td kind="field" title="expression"><span></span><span>expression</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"eq"</span> <span>"ne"</span> <span>"in"</span> <span>"not_in"</span> <span>"like"</span> <span>"ilike"</span> <span>"not_like"</span> <span>"not_ilike"</span> <span>"gt"</span> <span>"ge"</span> <span>"lt"</span> <span>"le"</span> <span>"between"</span></p><div><p>The comparison operator for the filter condition.</p></div></div></td></tr><tr><td kind="field" title="field"><span></span><span>field</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>The name of the data field to which the condition applies.</p></div></div></td></tr><tr><td kind="field" title="value"><span></span><span>value</span></td><td><div><p><span></span><span>string</span></p><div><p>The value that the condition checks for in the specified field. Use this attribute when specifying a single value.</p></div></div></td></tr><tr><td kind="field" title="values"><span></span><span>values</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>The values that the condition checks for in the specified field. Use this attribute when specifying multiple values.</p></div></div></td></tr></tbody></table></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": [`
    
    -   `{}`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"name": "LW_DATASOURCE_1",`
        
    -   `"description": "Details about datasource",`
        
    -   `"resultSchema": [],`
        
    -   `"sourceRelationships": []`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Entities)Entities

Lacework continuously monitors machines in your environment and maintains data on both running and non-running virtual machines.

## [](https://docs.lacework.net/api/v2/docs#tag/Entities/paths/~1api~1v2~1Entities~1Applications~1search/post)Search Applications

Search for applications running on the machine with an agent within the last 90 days. Get details such as the application name, username, machine, etc. by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Entities/Applications/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned applications by application name, username, machine, and more. For more information, see [APPLICATIONS\_V View](https://docs.lacework.com/console/applicationsv-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"}}`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" }, { "field": "containerInfo.pod_type", "expression": "eq", "value": "lacework-agent" } ],`  
    `"returns": [ "appName", "exePath", "containerInfo", "mid", "username" ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 8368,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Entities/paths/~1api~1v2~1Entities~1CommandLines~1search/post)Search Command Line Invocations

Search for active command line invocations in your environment across machines. Get details such as the created time, command line hash, and name of the command line executable by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Entities/CommandLines/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned command line invocations by the created time, command line hash, and name of the command line executable. For more information, see [CMDLINE\_V View](https://docs.lacework.com/cmdlinev-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"}}`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "cmdlineHash", "expression": "eq", "value": "12345sdlfkhk54l5..." } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "cmdlineHash", "expression": "eq", "value": "12345sdlfkhk54l5..." }, { "field": "cmdline", "expression": "eq", "value": "some command" } ],`  
    `"returns": [ "cmdline", "cmdlineHash" ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 8368,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Entities/paths/~1api~1v2~1Entities~1Containers~1search/post)Search Containers

Search for containers in your environment. Get details, such as the container name, pod name, tags, and so on, by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Entities/Containers/search`

The results reflect containers that were active within the specified time frame. Containers that were not active do not appear in the results.

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned containers by the container name, pod name, tags, and more. For more information, see [CONTAINER\_SUMMARY\_V View](https://docs.lacework.com/containersummaryv-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"}}`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" }, { "field": "propsContainer.IMAGE_TAG", "expression": "eq", "value": "v1.7.0-eksbuild.1" } ],`  
    `"returns": [ "containerName", "imageId", "podName", "propsContainer", "tags" ] }`

Within request bodies, nested field names that contain one or more special characters—e.g., dot ("."), colon (":"), or slash ("/")—must be enclosed in **escaped double quotes**. For example, the field name `io.codefresh.repo.name` nested under the `PROPS_LABEL` of the `propsContainer` field would be rendered as follows:

`"propsContainer.PROPS_LABEL.\"io.codefresh.repo.name\""`

In a filter, the example would appear as follows:

`{ "field": "propsContainer.PROPS_LABEL.\"io.codefresh.repo.name\"", "expression": "eq", "value": "modelservice" }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 5698,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Entities/paths/~1api~1v2~1Entities~1Files~1search/post)Search Files

Search for files in your environment. Get details such as the path to the file, file size, date of file modification, etc. by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Entities/Files/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned files by the path to the file, file size, date of file modification, and more. For more information, see [ALL\_FILES\_V View](https://docs.lacework.com/allfilesv-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"}}`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" }, { "field": "filePath", "expression": "eq", "value": "somePath" } ],`  
    `"returns": [ "filePath", "filedataHash", "mid", "size" ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 5698,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Entities/paths/~1api~1v2~1Entities~1Images~1search/post)Search Images

Search for container images in your environment. Get details such as the image id, image size, repository name, etc. by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Entities/Images/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned images by image id, image size, repository name, and more. For more information, see [IMAGE\_V View](https://docs.lacework.com/imagev-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"}}`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" }, { "field": "size", "expression": "eq", "value": "434" } ],`  
    `"returns": [ "imageId", "mid", "repo", "size" ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 6298,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Entities/paths/~1api~1v2~1Entities~1InternalIPAddresses~1search/post)Search Internal IP Addresses

Search for internal IP addresses in your environment. Get details such as the start time, IP address, machine ID, etc. by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Entities/InternalIPAddresses/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned addresses by the start time, IP address, machine ID, and more. For more information, see [INTERNAL\_IPA\_V View](https://docs.lacework.com/internalipav-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"}}`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" }, { "field": "ipAddr", "expression": "eq", "value": "10.123.456.1" } ],`  
    `"returns": [ "ipAddr" ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 6298,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Entities/paths/~1api~1v2~1Entities~1K8sPods~1search/post)Search K8s Pods

Search for Kubernetes pods in your environment. Get details such as the pod name, IP address assigned to the pod, and other pod statistics by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Entities/K8sPods/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned pods by machine ID, pod name, primary IP address, and more. For more information, see [POD\_SUMMARY\_V View](https://docs.lacework.com/podsummaryv-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"}}`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" }, { "field": "propsContainer.IMAGE_ID", "expression": "eq", "value": "sha256:9e862c010bf39766f9821926848754adccf58225aa652cc18a97fccba273df39" } ],`  
    `"returns": [ "mid", "podName", "propsContainer" ] }`

Within request bodies, nested field names that contain one or more special characters—e.g., dot ("."), colon (":"), or slash ("/")—must be enclosed in **escaped double quotes**. For example, the field name `io.kubernetes.pod.namespace` nested under the `PROPS_LABEL` of the `propsContainer` field would be rendered as follows:

`"propsContainer.PROPS_LABEL.\"io.kubernetes.pod.namespace\""`

In a filter, the example would appear as follows:

`{ "field": "propsContainer.PROPS_LABEL.\"io.kubernetes.pod.namespace\"", "expression": "eq", "value": "codefresh" }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 12398,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Entities/paths/~1api~1v2~1Entities~1Machines~1search/post)Search Machines

Search for machines in your environment. Get details such as the machine ID, host name of the machine, and other machine statistics by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Entities/Machines/search`

The results reflect the online machines for the specified time frame. Machines that were not online do not appear in the results.

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned machines by machine ID, host name, primary IP address, and more. For more information, see [MACHINE\_SUMMARY\_V View](https://docs.lacework.com/machinesummaryv-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"}}`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" }, { "field": "machineTags.ExternalIp", "expression": "eq", "value": "35.163.78.148" } ],`  
    `"returns": [ "hostname", "machineTags", "mid", "primaryIpAddr" ] }`

Within request bodies, nested field names that contain one or more special characters—e.g., dot ("."), colon (":"), or slash ("/")—must be enclosed in **escaped double quotes**. For example, the field name `spotinst:aws:ec2:group:createdBy` nested under the `machineTags` field would be rendered as follows:

`"machineTags.\"spotinst:aws:ec2:group:createdBy\""`

In a filter, the example would appear as follows:

`{ "field": "machineTags.\"spotinst:aws:ec2:group:createdBy\"", "expression": "eq", "value": "spotinst" }`

In addition, forward slash characters within field names must be escaped with a backslash, as in the following example:

`"machineTags.\"kubernetes.io\/cluster\/prod1\""`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 6318,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Entities/paths/~1api~1v2~1Entities~1MachineDetails~1search/post)Search Machine Details

Search for machine details in your environment. Get details such as the machine ID, host name of the machine, domain associated with the machine, kernel type of the machine, and other machine statistics by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Entities/MachineDetails/search`

Machine details are available only for machines that were online for the specified time frame. Details for machines that were not online are not available.

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned machines by machine ID, host name, domain, os, os version, and more. For more information, see [MACHINE\_DETAILS\_V View](https://docs.lacework.com/machinedetailsv-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"}}`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" }, { "field": "tags.AmiId", "expression": "eq", "value": "ami-0b83c6233cdbe5c3e" } ],`  
    `"returns": [ "hostname", "mid", "awsInstanceId", "awsZone", "tags" ] }`

Within request bodies, nested field names that contain one or more special characters—e.g., dot ("."), colon (":"), or slash ("/")—must be enclosed in **escaped double quotes**. For example, the field name `spotinst:aws:ec2:group:createdBy` nested under the `tags` field would be rendered as follows:

`"tags.\"spotinst:aws:ec2:group:createdBy\""`

In a filter, the example would appear as follows:

`{ "field": "tags.\"spotinst:aws:ec2:group:createdBy\"", "expression": "eq", "value": "spotinst" }`

In addition, forward slash characters within field names must be escaped with a backslash, as in the following example:

`"tags.\"kubernetes.io\/cluster\/prod1\""`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 6138,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Entities/paths/~1api~1v2~1Entities~1NetworkInterfaces~1search/post)Search Network Interfaces

Search for network interfaces in your environment. Get details such as the interface name, machine ID, hardware address associated with the interface, etc. by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Entities/NetworkInterfaces/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned interfaces by the interface name, machine ID, the hardware address associated with the interface, and more. For more information, see [INTERFACES\_V View](https://docs.lacework.com/interfacesv-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"}}`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" }, { "field": "name", "expression": "eq", "value": "someName" } ],`  
    `"returns": [ "name", "mid", "hwAddr", "ipAddr" ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 23680,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Entities/paths/~1api~1v2~1Entities~1NewFileHashes~1search/post)Search New File Hashes

Search for new file hashes in your environment. Get details such as the file hash, start time, and end time by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Entities/NewFileHashes/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned file hashes by the file hash, start time, or end time. For more information, see [NEW\_HASHES\_V View](https://docs.lacework.com/newhashesv-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"}}`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "filedataHash", "expression": "eq", "value": "2394832980909eoifjof3209032840i39r02390" } ],`  
    `"returns": [ "filedataHash" ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 123456,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Entities/paths/~1api~1v2~1Entities~1Packages~1search/post)Search Packages

Search for package in your environment. Get details such as the machine ID that contains the package, package name, package version, and other package statistics by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Entities/Packages/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned packages by machine ID, version, package architecture type, and more. For more information, see [PACKAGE\_V View](https://docs.lacework.com/packagev-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"}}`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" }, { "field": "packageName", "expression": "eq", "value": "package-1" } ],`  
    `"returns": [ "packageName", "mid", "version" ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 123680,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Entities/paths/~1api~1v2~1Entities~1Processes~1search/post)Search Processes

Search for processes in your environment. Get details such as the process ID, username that started the process, path to the file, parent process ID, etc., by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Entities/Processes/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned processes by the process id, username that started the process, path to the file, parent process ID, and more. For more information, see [PROCESS\_SUMMARY\_V View](https://docs.lacework.com/processsummaryv-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"}}`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" }, { "field": "ppid", "expression": "eq", "value": "0044" } ],`  
    `"returns": [ "pid", "ppid", "cmdlineHash", "mid", "uid", "username" ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 123680,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Entities/paths/~1api~1v2~1Entities~1Users~1search/post)Search Users

Search for users in your environment. Get details such as the username, machine ID, user ID, etc. by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Entities/Users/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned users by username, machine ID, user ID, and more. For more information, see [USER\_DETAILS\_V View](https://docs.lacework.com/userdetailsv-view).

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"}}`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "mid", "expression": "eq", "value": "12345" }, { "field": "username", "expression": "eq", "value": "someUser" } ],`  
    `"returns": [ "username", "uid", "mid" ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 12345,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Events)Events

View and verify the evidence or observation details of individual events.

## [](https://docs.lacework.net/api/v2/docs#tag/Events/paths/~1api~1v2~1Events~1search/post)Search Events

The Events API enables you to retrieve the evidence or observation details by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Events/search`

Lacework highly recommends specifying a time range in the request to narrow the search. If no time range is specified, the request uses the default time range of 24 hours before the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter the returned users by `eventType`, `srcType`, and more.

Here are some example `body` payloads:

-   `{ "timeFilter": { "startTime": "2022-03-18T00:00:00Z", "endTime": "2022-03-18T12:00:00Z"}}`
-   `{ "timeFilter": { "startTime": "2022-03-18T00:00:00Z", "endTime": "2022-03-18T12:00:00Z"},` `"filters": [ { "field": "eventType", "expression": "eq", "value": "CloudTrailDefaultAlert" } ] }`
-   `{ "timeFilter": { "startTime": "2022-03-18T00:00:00Z", "endTime": "2022-03-18T12:00:00Z"},` `"filters": [ { "field": "srcType", "expression": "eq", "value": "AwsResource" }, { "field": "srcEvent.awsRegion", "expression": "eq", "value": "us-west-2" } ],`  
    `"returns": [ "id", "srcEvent", "srcType" ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Exceptions)Policy Exceptions

Policy exceptions are a mechanism used to maintain the policies but allow you to circumvent one or more restrictions.

## [](https://docs.lacework.net/api/v2/docs#tag/Exceptions/paths/~1api~1v2~1Exceptions/post)Create Policy Exceptions

Create exceptions for a specific policy by specifying the exception metadata when invoking the following endpoint:

> `POST /api/v2/Exceptions?policyId={policyId}`

Replace `{policyId}` with the `policyId` value returned for an LQL policy in the response when invoking the following endpoint:

> `GET /api/v2/Policies`

##### query Parameters

<table><tbody><tr><td kind="field" title="policyId"><span></span><span>policyId</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="description"><span></span><span>description</span></td><td><div><p><span></span><span>string</span></p><div><p>A brief description of the new exception.</p></div></div></td></tr><tr><td kind="field" title="constraints"><span></span><p>required</p></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>The detailed constraints applied to the exception.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"description": "string",`
    
-   `"constraints": [`
    
    -   `{}`
        
    
    `]`
    

`}`

### Response samples

-   201
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"exceptionId": "510c8bc5-f06b-8afb-8028-0203d6e582de",`
        
    -   `"description": "wildcard exception",`
        
    -   `"constraints": [],`
        
    -   `"lastUpdateTime": "2022-04-05T01:53:11.809Z",`
        
    -   `"lastUpdateUser": "info@example.com"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Exceptions/paths/~1api~1v2~1Exceptions/get)List All Policy Exceptions

Get all existing exceptions by invoking the following endpoint:

> `GET /api/v2/Exceptions`

Get all existing exceptions of a specific policy by invoking the following endpoint:

> `GET /api/v2/Exceptions?policyId={policyId}`

Replace `{policyId}` with the `policyId` value returned for an LQL policy in the response when invoking the following endpoint:

> `GET /api/v2/Policies`

##### query Parameters

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Exceptions/paths/~1api~1v2~1Exceptions~1{exceptionId}/get)Policy Exception Details

Get details about an existing exception applied to a specific policy by invoking the following endpoint:

> `GET /api/v2/Exceptions/{exceptionId}?policyId={policyId}`

Replace `{policyId}` with the `policyId` value returned for an LQL policy in the response when when invoking the following endpoint:

> `GET /api/v2/Policies`

Replace `{exceptionId}` with the `exceptionId` value returned for an LQL policy in the response when invoking the following endpoint:

> `GET /api/v2/Exceptions?policyId={policyId}`

##### path Parameters

<table><tbody><tr><td kind="field" title="exceptionId"><span></span><span>exceptionId</span><p>required</p></td><td></td></tr></tbody></table>

##### query Parameters

<table><tbody><tr><td kind="field" title="policyId"><span></span><span>policyId</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"exceptionId": "510c8bc5-f06b-8afb-8028-0203d6e582de",`
        
    -   `"description": "wildcard exception",`
        
    -   `"constraints": [],`
        
    -   `"lastUpdateTime": "2022-04-05T01:53:11.809Z",`
        
    -   `"lastUpdateUser": "info@example.com"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Exceptions/paths/~1api~1v2~1Exceptions~1{exceptionId}/patch)Update Policy Exceptions

Update an existing exception applied to a specific policy by invoking the following endpoint:

> `PATCH /api/v2/Exceptions/{exceptionId}?policyId={policyId}`

Replace `{policyId}` with the `policyId` value returned for an LQL policy in the response when invoking the following endpoint:

> `GET /api/v2/Policies`

Replace `{exceptionId}` with the `exceptionId` value returned for an LQL policy in the response when invoking the following endpoint:

> `GET /api/v2/Exceptions?policyId={policyId}`

##### path Parameters

<table><tbody><tr><td kind="field" title="exceptionId"><span></span><span>exceptionId</span><p>required</p></td><td></td></tr></tbody></table>

##### query Parameters

<table><tbody><tr><td kind="field" title="policyId"><span></span><span>policyId</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="description"><span></span><span>description</span></td><td><div><p><span></span><span>string</span></p><div><p>A brief description of the new exception.</p></div></div></td></tr><tr><td kind="field" title="constraints"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>The detailed constraints applied to the exception.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"description": "string",`
    
-   `"constraints": [`
    
    -   `{}`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"exceptionId": "510c8bc5-f06b-8afb-8028-0203d6e582de",`
        
    -   `"description": "wildcard exception",`
        
    -   `"constraints": [],`
        
    -   `"lastUpdateTime": "2022-04-05T01:53:11.809Z",`
        
    -   `"lastUpdateUser": "info@example.com"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Exceptions/paths/~1api~1v2~1Exceptions~1{exceptionId}/delete)Delete Policy Exceptions

Delete an existing exception applied to a specific policy by invoking the following endpoint:

> `DELETE /api/v2/Exceptions/{exceptionId}?policyId={policyId}`

Replace `{policyId}` with the `policyId` value returned for an LQL policy in the response when invoking the following endpoint:

> `GET /api/v2/Policies`

Replace `{exceptionId}` with the `exceptionId` value returned for an LQL policy in the response when invoking the following endpoint:

> `GET /api/v2/Exceptions?policyId={policyId}`

##### path Parameters

<table><tbody><tr><td kind="field" title="exceptionId"><span></span><span>exceptionId</span><p>required</p></td><td></td></tr></tbody></table>

##### query Parameters

<table><tbody><tr><td kind="field" title="policyId"><span></span><span>policyId</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Inventory)Inventory

View and monitor in-use cloud resources' risk, compliance, and configuration changes.

For more details about snapshots of resources, see [Resource Inventory](https://docs.lacework.com/category/resource-inventory).

## [](https://docs.lacework.net/api/v2/docs#tag/Inventory/paths/~1api~1v2~1Inventory~1search/post)Search Inventory

The Inventory API enables you to retrieve information about resources in your cloud integrations, such as virtual machines, S3 buckets, security groups, and more, using the following endpoint:

> `POST /api/v2/Inventory/search`

By default, Lacework collects resource information once a day. You can view and modify when resource collection starts using the Compliance Report Schedule [setting](https://docs.lacework.com/console/general-settings#resource-management-collection-schedule).

The time filter allows you to see your resource inventory at a specific point of time. When using the Inventory API, keep in mind that the information returned reflects the inventory when the resource collector last ran within the specified time range. If you use a recent time range that does not encompass the last time inventory collection occurred, the query returns an empty array. In this case, expand the time span to include the last collection time.

For details about what cloud resource information is available, see [CLOUD\_CONFIGURATION\_V View](https://docs.lacework.com/console/cloudconfigurationv-view).

The `rlike` and `not_rlike` operators are useful for filtering results. For example, if the result contains the security group ID `sg-0a1b2c3d4e5f6g7h` in the path `resourceConfig.SecurityGroups.GroupId`, and `SecurityGroups` is an array, you can filter by ID for that pattern as follows:

> `"filters" : [ {"field":"resourceConfig","expression": "rlike", "value":".*sg-0a1b2c3d4e5f6g7h.*" } ]`

Here are additional example `body` payloads:

-   `{ "timeFilter": { "startTime" : "2022-06-08T00:00:00Z", "endTime": "2022-06-10T12:00:00Z"},` `"csp": "AWS" }`
-   `{ "timeFilter": { "startTime": "2022-06-08T00:00:00Z", "endTime": "2022-06-10T12:00:00Z"},` `"filters" : [ { "field": "resourceConfig.Architecture", "expression": "eq", "value": "x86_64" }, { "field": "resourceRegion", "expression": "eq", "value" : "us-east-2" } ],`  
    `"returns": [ "cloudDetails", "csp", "resourceConfig" , "resourceId", "resourceType" ],`  
    `"csp": "GCP" }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr><tr><td kind="field" title="csp"><span></span><span>csp</span></td><td><div><p><span></span><span>any</span></p><p><span>Enum:</span> <span>"AWS"</span> <span>"Azure"</span> <span>"GCP"</span></p><div><p>Cloud service provider. You must specify either <code>csp</code> or <code>dataset</code> in the request.</p></div></div></td></tr><tr><td kind="field" title="dataset"><span></span><span>dataset</span></td><td><div><p><span></span><span>any</span></p><p><span type="warning">Deprecated</span></p><p><span>Enum:</span> <span>"AwsCompliance"</span> <span>"GcpCompliance"</span></p><div><p>You must specify either <code>csp</code> or <code>dataset</code> in the request.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `],`
    
-   `"csp": "AWS",`
    
-   `"dataset": "AwsCompliance"`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 78623,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Inventory/paths/~1api~1v2~1Inventory~1scan/post)Scan Inventory

Trigger a [resource scan](https://docs.lacework.com/console/resource-explorer). By default, Lacework scans cloud integrations in order to generate or update its resource inventory [once a day](https://docs.lacework.com/console/general-settings#resource-management-collection-schedule). This endpoint lets you trigger scans manually. This endpoint is useful, for example, after you have onboarded a new cloud integration and want to start collecting and evaluating resources from the system immediately. Manual scans can be run one hour after the last scan has completed.

Usage Example:

> `curl -X POST -H 'Content-Type: application/json' "https://YourLacework.lacework.net/api/v2/Inventory/scan?csp=AWS" -H "Authorization: Bearer YourAPIToken"`

##### query Parameters

<table><tbody><tr><td kind="field" title="csp"><span></span><span>csp</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"AWS"</span> <span>"GCP"</span> <span>"Azure"</span></p></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"status": "available",`
        
    -   `"details": "Scan is available"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Inventory/paths/~1api~1v2~1Inventory~1scan/get)Track Inventory Scan Status

Check the status of a [resource scan](https://docs.lacework.com/console/resource-explorer). A resource scan may take an hour or more to complete. This endpoint lets you check the progress of a running scan.

Usage Example:

> `curl -X GET -H 'Content-Type: application/json' "https://YourLacework.lacework .net/api/v2/Inventory/scan?csp=AWS" -H "Authorization: Bearer YourAPIToken"`

##### query Parameters

<table><tbody><tr><td kind="field" title="csp"><span></span><span>csp</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"AWS"</span> <span>"GCP"</span> <span>"Azure"</span></p></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"status": "available",`
        
    -   `"details": "Scan is available"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/OrganizationInfo)Organization Info

Return information about whether the Lacework account is an organization account and, if it is, what the organization account URL is by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/OrganizationInfo`

## [](https://docs.lacework.net/api/v2/docs#tag/OrganizationInfo/paths/~1api~1v2~1OrganizationInfo/get)Organization Info

Return information about whether the Lacework account is an organization account and, if it is, what the organization account URL is by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/OrganizationInfo`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`[`

-   `{`
    
    -   `"orgAccount": true,`
        
    -   `"orgAccountUrl": "YourLacework.lacework.net"`
        
    
    `}`
    

`]`

## [](https://docs.lacework.net/api/v2/docs#tag/Policies)Policies

Policies are a mechanism used to add annotated metadata to queries for improving the context of alerts, reports, and information displayed in the Lacework Console. You can fully customize policies.

## [](https://docs.lacework.net/api/v2/docs#tag/Policies/paths/~1api~1v2~1Policies/post)Create Policies

Create a Lacework Query Language (LQL) policy by specifying parameters in the request body when invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Policies`

This creates the LQL policy in your Lacework instance so you can view it in the Lacework Console. You can get the unique identifiers for the LQL policies (`policyIdList`) array by invoking the `GET /api/v2/Policies` endpoint.

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="policyType"><span></span><span>policyType</span></td><td><div><p><span></span><span>string</span></p><p><span>Value:</span> <span>"Violation"</span></p><div><p>The policy type such as <code>Violation</code>.</p></div></div></td></tr><tr><td kind="field" title="queryId"><span></span><span>queryId</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Identifier of the query that executes while running the policy.</p></div></div></td></tr><tr><td kind="field" title="title"><span></span><span>title</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>The policy's title.</p></div></div></td></tr><tr><td kind="field" title="enabled"><span></span><span>enabled</span><p>required</p></td><td><div><p><span></span><span>boolean</span></p><div><p>When sending a request, use this attribute to enable or disable a policy. When included in a response, returns <code>True</code> for enabled policies, or returns <code>False</code> for disabled policies.</p></div></div></td></tr><tr><td kind="field" title="description"><span></span><span>description</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Information about the new policy.</p></div></div></td></tr><tr><td kind="field" title="remediation"><span></span><span>remediation</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Remediation strategy for the events triggered by the policy.</p></div></div></td></tr><tr><td kind="field" title="severity"><span></span><span>severity</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"info"</span> <span>"low"</span> <span>"medium"</span> <span>"high"</span> <span>"critical"</span></p><div><p>The severity of an event triggered by the policy.</p></div></div></td></tr><tr><td kind="field" title="limit"><span></span><span>limit</span></td><td><div><p><span></span><span>number</span><span> <span>&gt;= 1</span></span></p><p><span>Default: </span><span>1000</span></p><div><p>The maximum number of records that each policy will return. The default value is 1000.</p></div></div></td></tr><tr><td kind="field" title="evalFrequency"><span></span><span>evalFrequency</span></td><td><div><p><span></span><span>string</span></p><p><span type="warning">Deprecated</span></p><p><span>Enum:</span> <span>"Hourly"</span> <span>"Daily"</span></p><div><p>Frequency at which the policy will be evaluated</p></div></div></td></tr><tr><td kind="field" title="alertEnabled"><span></span><span>alertEnabled</span><p>required</p></td><td><div><p><span></span><span>boolean</span></p><div><p>When sending a request, set to <code>True</code> if you want to send alerts to an alert profile when the policy is triggered. Set to <code>False</code> if you want to mute alerts when the policy is triggered.</p></div></div></td></tr><tr><td kind="field" title="alertProfile"><span></span><span>alertProfile</span></td><td><div><p><span></span><span>string</span></p><div><p>The alert profile to use for sending alerts when the policy is triggered.</p></div></div></td></tr><tr><td kind="field" title="tags"><span></span><span>tags</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>A list of policy tags.</p></div></div></td></tr><tr><td kind="field" title="policyId"><span></span><span>policyId</span></td><td><div><p><span></span><span>string</span></p><div><p>Policy ID. The convention for policy ID creation is <code>accountName-remainder</code>, for example, lws-special-100. When sending a request, you can simply provide <code>$account-&lt;remainder&gt;</code>, and Lacework will substitute the <code>$account</code> prefix with your actual account name. <strong>Note:</strong> The <code>-remainder</code> must use the regex pattern (<code>^[a-z]{1,16}(-\d{1,8})?$</code>), and cannot be <code>default</code> or start with <code>default-</code>.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"policyType": "Violation",`
    
-   `"queryId": "string",`
    
-   `"title": "string",`
    
-   `"enabled": true,`
    
-   `"description": "string",`
    
-   `"remediation": "string",`
    
-   `"severity": "info",`
    
-   `"limit": 1000,`
    
-   `"evalFrequency": "Hourly",`
    
-   `"alertEnabled": true,`
    
-   `"alertProfile": "string",`
    
-   `"tags": [`
    
    -   `"string"`
        
    
    `],`
    
-   `"policyId": "string"`
    

`}`

### Response samples

-   201
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"evaluatorId": "Cloudtrail",`
        
    -   `"policyId": "lacework...",`
        
    -   `"policyType": "Violation",`
        
    -   `"queryId": "LW_Custom_AWS_CTA_AuroraPasswordChange",`
        
    -   `"queryText": "LW_Custom_AWS_CTA_AuroraPasswordChange { SOURCE { CloudTrailRawEvents } FILTER ...",`
        
    -   `"title": "Cloudtrail Policy 2",`
        
    -   `"enabled": false,`
        
    -   `"description": "Cloudtrail Policy 2",`
        
    -   `"remediation": "Policy remediation 2",`
        
    -   `"severity": "medium",`
        
    -   `"limit": 100,`
        
    -   `"evalFrequency": "Hourly",`
        
    -   `"alertEnabled": true,`
        
    -   `"alertProfile": "LW_CloudTrail_Alerts.CloudTrailDefaultAlert_AwsResource",`
        
    -   `"owner": "user@example.com",`
        
    -   `"lastUpdateTime": "2022-10-03T16:23:38.915Z",`
        
    -   `"lastUpdateUser": "user@example.com",`
        
    -   `"tags": []`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Policies/paths/~1api~1v2~1Policies/get)List All Policies

List all registered LQL policies in your Lacework instance, by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/Policies`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Policies/paths/~1api~1v2~1Policies~1search/post)Search Policies

Search for policies by specifying parameters in the request body when invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Policies/search`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p><p>To use wildcards with the <code>LIKE</code>, <code>ILIKE</code> <code>NOT_LIKE</code> OR <code>NOT_ILIKE</code> filters, use the % symbol to match any string. This allows you to perform more flexible and broad searches for text data.</p><ul><li><code>%</code> represents a wildcard to match zero or more characters</li><li><code>_</code> (underscore) represents a wildcard match for a single character</li></ul></div></div></td></tr><tr><td colspan="2"><div><p>Array</p><div><table><tbody><tr><td kind="field" title="expression"><span></span><span>expression</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"eq"</span> <span>"ne"</span> <span>"in"</span> <span>"not_in"</span> <span>"like"</span> <span>"ilike"</span> <span>"not_like"</span> <span>"not_ilike"</span> <span>"gt"</span> <span>"ge"</span> <span>"lt"</span> <span>"le"</span> <span>"between"</span></p><div><p>The comparison operator for the filter condition.</p></div></div></td></tr><tr><td kind="field" title="field"><span></span><span>field</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>The name of the data field to which the condition applies.</p></div></div></td></tr><tr><td kind="field" title="value"><span></span><span>value</span></td><td><div><p><span></span><span>string</span></p><div><p>The value that the condition checks for in the specified field. Use this attribute when specifying a single value.</p></div></div></td></tr><tr><td kind="field" title="values"><span></span><span>values</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>The values that the condition checks for in the specified field. Use this attribute when specifying multiple values.</p></div></div></td></tr></tbody></table></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": [`
    
    -   `{}`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"evaluatorId": "Cloudtrail",`
        
    -   `"policyId": "lacework...",`
        
    -   `"policyType": "Violation",`
        
    -   `"queryId": "LW_Custom_AWS_CTA_AuroraPasswordChange",`
        
    -   `"queryText": "LW_Custom_AWS_CTA_AuroraPasswordChange { SOURCE { CloudTrailRawEvents } FILTER ...",`
        
    -   `"title": "Cloudtrail Policy 2",`
        
    -   `"enabled": false,`
        
    -   `"description": "Cloudtrail Policy 2",`
        
    -   `"remediation": "Policy remediation 2",`
        
    -   `"severity": "medium",`
        
    -   `"limit": 100,`
        
    -   `"evalFrequency": "Hourly",`
        
    -   `"alertEnabled": true,`
        
    -   `"alertProfile": "LW_CloudTrail_Alerts.CloudTrailDefaultAlert_AwsResource",`
        
    -   `"owner": "user@example.com",`
        
    -   `"lastUpdateTime": "2022-10-03T16:23:38.915Z",`
        
    -   `"lastUpdateUser": "user@example.com",`
        
    -   `"tags": []`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Policies/paths/~1api~1v2~1Policies~1{policyId}/get)Policy Details

Get details about a single LQL policy by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/Policies/{policyId}`

Replace `{policyId}` with the `policyId` value returned for an LQL policy in the response when the `GET /api/v2/Policies` endpoint is invoked.

##### path Parameters

<table><tbody><tr><td kind="field" title="policyId"><span></span><span>policyId</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"evaluatorId": "Cloudtrail",`
        
    -   `"policyId": "lacework...",`
        
    -   `"policyType": "Violation",`
        
    -   `"queryId": "LW_Custom_AWS_CTA_AuroraPasswordChange",`
        
    -   `"queryText": "LW_Custom_AWS_CTA_AuroraPasswordChange { SOURCE { CloudTrailRawEvents } FILTER ...",`
        
    -   `"title": "Cloudtrail Policy 2",`
        
    -   `"enabled": false,`
        
    -   `"description": "Cloudtrail Policy 2",`
        
    -   `"remediation": "Policy remediation 2",`
        
    -   `"severity": "medium",`
        
    -   `"limit": 100,`
        
    -   `"evalFrequency": "Hourly",`
        
    -   `"alertEnabled": true,`
        
    -   `"alertProfile": "LW_CloudTrail_Alerts.CloudTrailDefaultAlert_AwsResource",`
        
    -   `"owner": "user@example.com",`
        
    -   `"lastUpdateTime": "2022-10-03T16:23:38.915Z",`
        
    -   `"lastUpdateUser": "user@example.com",`
        
    -   `"tags": []`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Policies/paths/~1api~1v2~1Policies~1{policyId}/patch)Update Policies

Update an existing LQL policy registered in your Lacework instance by specifying parameters in the request body when invoking the following endpoint:

> `PATCH https://YourLacework.lacework.net/api/v2/Policies/{policyId}`

Replace `{policyId}` with the `policyId` value returned for an LQL policy in the response when the `GET /api/v2/Policies` endpoint is invoked.

##### path Parameters

<table><tbody><tr><td kind="field" title="policyId"><span></span><span>policyId</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="policyType"><span></span><span>policyType</span></td><td><div><p><span></span><span>string</span></p><p><span>Value:</span> <span>"Violation"</span></p><div><p>The policy type such as <code>Violation</code>.</p></div></div></td></tr><tr><td kind="field" title="queryId"><span></span><span>queryId</span></td><td><div><p><span></span><span>string</span></p><div><p>Identifier of the query that executes while running the policy.</p></div></div></td></tr><tr><td kind="field" title="title"><span></span><span>title</span></td><td><div><p><span></span><span>string</span></p><div><p>The policy's title.</p></div></div></td></tr><tr><td kind="field" title="enabled"><span></span><span>enabled</span></td><td><div><p><span></span><span>boolean</span></p><div><p>When sending a request, use this attribute to enable or disable a policy. When included in a response, returns <code>True</code> for enabled policies, or returns <code>False</code> for disabled policies.</p></div></div></td></tr><tr><td kind="field" title="description"><span></span><span>description</span></td><td><div><p><span></span><span>string</span></p><div><p>Information about the new policy.</p></div></div></td></tr><tr><td kind="field" title="remediation"><span></span><span>remediation</span></td><td><div><p><span></span><span>string</span></p><div><p>Remediation strategy for the events triggered by the policy.</p></div></div></td></tr><tr><td kind="field" title="severity"><span></span><span>severity</span></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"info"</span> <span>"low"</span> <span>"medium"</span> <span>"high"</span> <span>"critical"</span></p><div><p>The severity of an event triggered by the policy.</p></div></div></td></tr><tr><td kind="field" title="limit"><span></span><span>limit</span></td><td><div><p><span></span><span>number</span><span> <span>&gt;= 1</span></span></p><p><span>Default: </span><span>1000</span></p><div><p>The maximum number of records that each policy will return. The default value is 1000.</p></div></div></td></tr><tr><td kind="field" title="evalFrequency"><span></span><span>evalFrequency</span></td><td><div><p><span></span><span>string</span></p><p><span type="warning">Deprecated</span></p><p><span>Enum:</span> <span>"Hourly"</span> <span>"Daily"</span></p><div><p>Frequency at which the policy will be evaluated</p></div></div></td></tr><tr><td kind="field" title="alertEnabled"><span></span><span>alertEnabled</span></td><td><div><p><span></span><span>boolean</span></p><div><p>When sending a request, set to <code>True</code> if you want to send alerts to an alert profile when the policy is triggered. Set to <code>False</code> if you want to mute alerts when the policy is triggered.</p></div></div></td></tr><tr><td kind="field" title="alertProfile"><span></span><span>alertProfile</span></td><td><div><p><span></span><span>string</span></p><div><p>The alert profile to use for sending alerts when the policy is triggered.</p></div></div></td></tr><tr><td kind="field" title="tags"><span></span><span>tags</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>A list of policy tags.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"policyType": "Violation",`
    
-   `"queryId": "string",`
    
-   `"title": "string",`
    
-   `"enabled": true,`
    
-   `"description": "string",`
    
-   `"remediation": "string",`
    
-   `"severity": "info",`
    
-   `"limit": 1000,`
    
-   `"evalFrequency": "Hourly",`
    
-   `"alertEnabled": true,`
    
-   `"alertProfile": "string",`
    
-   `"tags": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"evaluatorId": "Cloudtrail",`
        
    -   `"policyId": "lacework...",`
        
    -   `"policyType": "Violation",`
        
    -   `"queryId": "LW_Custom_AWS_CTA_AuroraPasswordChange",`
        
    -   `"queryText": "LW_Custom_AWS_CTA_AuroraPasswordChange { SOURCE { CloudTrailRawEvents } FILTER ...",`
        
    -   `"title": "Cloudtrail Policy 2",`
        
    -   `"enabled": false,`
        
    -   `"description": "Cloudtrail Policy 2",`
        
    -   `"remediation": "Policy remediation 2",`
        
    -   `"severity": "medium",`
        
    -   `"limit": 100,`
        
    -   `"evalFrequency": "Hourly",`
        
    -   `"alertEnabled": true,`
        
    -   `"alertProfile": "LW_CloudTrail_Alerts.CloudTrailDefaultAlert_AwsResource",`
        
    -   `"owner": "user@example.com",`
        
    -   `"lastUpdateTime": "2022-10-03T16:23:38.915Z",`
        
    -   `"lastUpdateUser": "user@example.com",`
        
    -   `"tags": []`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Policies/paths/~1api~1v2~1Policies~1{policyId}/delete)Delete Policies

Delete an LQL custom policy registered in your Lacework instance by invoking the following endpoint:

> `DELETE https://YourLacework.lacework.net/api/v2/Policies/{policyId}`

Replace `{policyId}` with the `policyId` value returned for an LQL policy in the response when the `GET /api/v2/Policies` endpoint is invoked.

##### path Parameters

<table><tbody><tr><td kind="field" title="policyId"><span></span><span>policyId</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Queries)Queries

Queries are the mechanism used to interactively request information from a specific curated datasource. Queries have a defined structure for authoring detections.

## [](https://docs.lacework.net/api/v2/docs#tag/Queries/paths/~1api~1v2~1Queries/post)Create Queries

Create a Lacework Query Language (LQL) query by specifying parameters in the request body when invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Queries`

This creates the LQL query in your Lacework instance so you can use it in an LQL custom policy and view it in the Lacework Console. You can get the unique identifiers for the LQL queries (`queryIdList`) array by invoking the `GET /api/v2/Queries` endpoint.

For information on creating queries, including information on specifying data sources, filtering, and returning data with the DISTINCT operator, see [LQL Overview](https://docs.lacework.net/lql/restricted/lql-overview).

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="queryText"><span></span><span>queryText</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>When sending a request, provide a human-readable text syntax for specifying selection, filtering, and manipulation of data.</p></div></div></td></tr><tr><td kind="field" title="queryId"><span></span><span>queryId</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Identifier of the query that executes while running the policy.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"queryText": "string",`
    
-   `"queryId": "string"`
    

`}`

### Response samples

-   201
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"evaluatorId": "Cloudtrail",`
        
    -   `"queryId": "LW_Global_...",`
        
    -   `"queryText": "Query...",`
        
    -   `"owner": "user@example.com",`
        
    -   `"lastUpdateTime": "2020-12-16T16:43:37.915Z",`
        
    -   `"lastUpdateUser": "user@example.com",`
        
    -   `"resultSchema": []`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Queries/paths/~1api~1v2~1Queries/get)List All Queries

List all registered LQL queries in your Lacework instance by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/Queries`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Queries/paths/~1api~1v2~1Queries~1execute/post)Execute Queries

Run an LQL query by specifying parameters in the request body by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Queries/execute`

The response is the data that the query finds in the datasource for the specified time period. To specify a time period, use the `StartTimeRange` and `EndTimeRange` arguments. For an example of how to specify a time frame, see [Example Queries](https://docs.lacework.net/lql/restricted/lql-query-examples).

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="query"><span></span><p>required</p></td><td></td></tr><tr><td kind="field" title="options"><span></span></td><td><div><p><span></span><span>object</span><span> (Query_Execute_Options)</span></p></div></td></tr><tr><td kind="field" title="arguments"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"query": {`
    
    -   `"queryText": "string"`
        
    
    `},`
    
-   `"options": {`
    
    -   `"limit": 1`
        
    
    `},`
    
-   `"arguments": [`
    
    -   `{}`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{ }`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Queries/paths/~1api~1v2~1Queries~1{queryId}~1execute/post)Execute Queries by ID

Run an existing LQL query registered in your Lacework instance by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Queries/{queryId}/execute`

Replace `{queryId}` with the `queryId` value returned for an LQL query in the response when the `GET /api/v2/Queries` endpoint is invoked. The response is the data that the query finds in the datasource for the specified time period. For an example of how to specify a time frame, see [Example Queries](https://docs.lacework.net/lql/restricted/lql-query-examples).

##### path Parameters

<table><tbody><tr><td kind="field" title="queryId"><span></span><span>queryId</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Identifier of the query that executes while running the policy.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="options"><span></span></td><td><div><p><span></span><span>object</span><span> (Query_Execute_Options)</span></p></div></td></tr><tr><td kind="field" title="arguments"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"options": {`
    
    -   `"limit": 1`
        
    
    `},`
    
-   `"arguments": [`
    
    -   `{}`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{ }`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Queries/paths/~1api~1v2~1Queries~1validate/post)Validate Queries

Validate an LQL query by specifying parameters in the request body by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Queries/validate`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="queryText"><span></span><span>queryText</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>When sending a request, provide a human-readable text syntax for specifying selection, filtering, and manipulation of data.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"queryText": "string"`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"evaluatorId": "Cloudtrail",`
        
    -   `"queryId": "LW_Global_...",`
        
    -   `"queryText": "Query...",`
        
    -   `"resultSchema": []`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Queries/paths/~1api~1v2~1Queries~1search/post)Search Queries

Search for queries by specifying parameters in the request body when invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Queries/search`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p><p>To use wildcards with the <code>LIKE</code>, <code>ILIKE</code> <code>NOT_LIKE</code> OR <code>NOT_ILIKE</code> filters, use the % symbol to match any string. This allows you to perform more flexible and broad searches for text data.</p><ul><li><code>%</code> represents a wildcard to match zero or more characters</li><li><code>_</code> (underscore) represents a wildcard match for a single character</li></ul></div></div></td></tr><tr><td colspan="2"><div><p>Array</p><div><table><tbody><tr><td kind="field" title="expression"><span></span><span>expression</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"eq"</span> <span>"ne"</span> <span>"in"</span> <span>"not_in"</span> <span>"like"</span> <span>"ilike"</span> <span>"not_like"</span> <span>"not_ilike"</span> <span>"gt"</span> <span>"ge"</span> <span>"lt"</span> <span>"le"</span> <span>"between"</span></p><div><p>The comparison operator for the filter condition.</p></div></div></td></tr><tr><td kind="field" title="field"><span></span><span>field</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>The name of the data field to which the condition applies.</p></div></div></td></tr><tr><td kind="field" title="value"><span></span><span>value</span></td><td><div><p><span></span><span>string</span></p><div><p>The value that the condition checks for in the specified field. Use this attribute when specifying a single value.</p></div></div></td></tr><tr><td kind="field" title="values"><span></span><span>values</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>The values that the condition checks for in the specified field. Use this attribute when specifying multiple values.</p></div></div></td></tr></tbody></table></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": [`
    
    -   `{}`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"evaluatorId": "Cloudtrail",`
        
    -   `"queryId": "LW_Global_...",`
        
    -   `"queryText": "Query...",`
        
    -   `"owner": "user@example.com",`
        
    -   `"lastUpdateTime": "2020-12-16T16:43:37.915Z",`
        
    -   `"lastUpdateUser": "user@example.com",`
        
    -   `"resultSchema": []`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Queries/paths/~1api~1v2~1Queries~1{queryId}/get)Query Details

Get details about a single LQL query by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/Queries/{queryId}`

Replace `{queryId}` with the `queryId` value returned for an LQL query in the response when the `GET /api/v2/Queries` endpoint is invoked.

##### path Parameters

<table><tbody><tr><td kind="field" title="queryId"><span></span><span>queryId</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Identifier of the query that executes while running the policy.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"evaluatorId": "Cloudtrail",`
        
    -   `"queryId": "LW_Global_...",`
        
    -   `"queryText": "Query...",`
        
    -   `"owner": "user@example.com",`
        
    -   `"lastUpdateTime": "2020-12-16T16:43:37.915Z",`
        
    -   `"lastUpdateUser": "user@example.com",`
        
    -   `"resultSchema": []`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Queries/paths/~1api~1v2~1Queries~1{queryId}/patch)Update Queries

Update an existing LQL query registered in your Lacework instance by invoking the following endpoint:

> `PATCH https://YourLacework.lacework.net/api/v2/Queries/{queryId}`

Replace `{queryId}` with the `queryId` value returned for an LQL query in the response when the `GET /api/v2/Queries` endpoint is invoked.

##### path Parameters

<table><tbody><tr><td kind="field" title="queryId"><span></span><span>queryId</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Identifier of the query that executes while running the policy.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="queryText"><span></span><span>queryText</span></td><td><div><p><span></span><span>string</span></p><div><p>When sending a request, provide a human-readable text syntax for specifying selection, filtering, and manipulation of data.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"queryText": "string"`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"evaluatorId": "Cloudtrail",`
        
    -   `"queryId": "LW_Global_...",`
        
    -   `"queryText": "Query...",`
        
    -   `"owner": "user@example.com",`
        
    -   `"lastUpdateTime": "2020-12-16T16:43:37.915Z",`
        
    -   `"lastUpdateUser": "user@example.com",`
        
    -   `"resultSchema": []`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Queries/paths/~1api~1v2~1Queries~1{queryId}/delete)Delete Queries

Delete a Lacework Query Language (LQL) query registered in your Lacework instance by invoking the following endpoint:

> `DELETE https://YourLacework.lacework.net/api/v2/Queries/{queryId}`

Replace `{queryId}` with the `queryId` value returned for an LQL query in the response when invoking the following endpoint: `GET /api/v2/Queries`.

##### path Parameters

<table><tbody><tr><td kind="field" title="queryId"><span></span><span>queryId</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Identifier of the query that executes while running the policy.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ReportRules)Report Rules

## [](https://docs.lacework.net/api/v2/docs#tag/ReportRules/paths/~1api~1v2~1ReportRules/post)Create Report Rule

Create a report rule in your Lacework instance by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/ReportRules`

Get the unique identifiers for the alert channels (`intGuidList`) array by invoking the `GET /api/v2/ReportRules` endpoint.

In addition, the severity field is required if you create report rules for any of the following report types: `awsCloudtrailEvents`, `awsComplianceEvents`, `azureActivityLogEvents`, `azureComplianceEvents`, `gcpAuditTrailEvents`, `gcpComplianceEvents`, `openShiftComplianceEvents`, `platformEvents`, `agentEvents`.

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span><p>required</p></td><td><div><p><span></span><span>object</span></p><div><p>When sending a request, use this object to define the new report rule. When included in a response, this object contains details of a report rule. You can use these attributes when searching for existing report rules by invoking a GET request.</p></div></div></td></tr><tr><td kind="field" title="intgGuidList"><span></span><span>intgGuidList</span><p>required</p></td><td><div><p><span>Array of </span><span>strings</span><span> <span>non-empty </span><span>unique</span></span></p><div><p>The alert channels for the rule to access.</p></div></div></td></tr><tr><td kind="field" title="reportNotificationTypes"><span></span><p>required</p></td><td><div><p><span></span><span>object</span></p><div><p>The report types that you want the rule to apply to.</p></div></div></td></tr><tr><td kind="field" title="type"><span></span><span>type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": {`
    
    -   `"name": "string",`
        
    -   `"description": "string",`
        
    -   `"enabled": 1,`
        
    -   `"resourceGroups": [],`
        
    -   `"severity": [ ]`
        
    
    `},`
    
-   `"intgGuidList": [`
    
    -   `"string"`
        
    
    `],`
    
-   `"reportNotificationTypes": {`
    
    -   `"agentEvents": true,`
        
    -   `"awsCis14": true,`
        
    -   `"awsCisS3": true,`
        
    -   `"awsCloudtrailEvents": true,`
        
    -   `"awsComplianceEvents": true,`
        
    -   `"awsCis14IsoIec270022022": true,`
        
    -   `"awsCyberEssentials22": true,`
        
    -   `"awsCsaCcm405": true,`
        
    -   `"azureActivityLogEvents": true,`
        
    -   `"azureCis": true,`
        
    -   `"azureCis131": true,`
        
    -   `"azureComplianceEvents": true,`
        
    -   `"azurePci": true,`
        
    -   `"azurePciRev2": true,`
        
    -   `"azureSoc": true,`
        
    -   `"azureSocRev2": true,`
        
    -   `"azureIso27001": true,`
        
    -   `"azureHipaa": true,`
        
    -   `"azureNistCsf": true,`
        
    -   `"azureNist80053Rev5": true,`
        
    -   `"azureNist800171Rev2": true,`
        
    -   `"gcpAuditTrailEvents": true,`
        
    -   `"gcpCis": true,`
        
    -   `"gcpComplianceEvents": true,`
        
    -   `"gcpHipaa": true,`
        
    -   `"gcpHipaaRev2": true,`
        
    -   `"gcpIso27001": true,`
        
    -   `"gcpCis12": true,`
        
    -   `"gcpCis13": true,`
        
    -   `"gcpK8s": true,`
        
    -   `"gcpPci": true,`
        
    -   `"gcpPciRev2": true,`
        
    -   `"gcpSoc": true,`
        
    -   `"gcpSocRev2": true,`
        
    -   `"gcpNistCsf": true,`
        
    -   `"gcpNist80053Rev4": true,`
        
    -   `"gcpNist800171Rev2": true,`
        
    -   `"hipaa": true,`
        
    -   `"iso2700": true,`
        
    -   `"k8sAuditLogEvents": true,`
        
    -   `"nist800-53Rev4": true,`
        
    -   `"nist800-171Rev2": true,`
        
    -   `"openShiftCompliance": true,`
        
    -   `"openShiftComplianceEvents": true,`
        
    -   `"pci": true,`
        
    -   `"platformEvents": true,`
        
    -   `"soc": true,`
        
    -   `"awsSocRev2": true,`
        
    -   `"trendReport": true,`
        
    -   `"awsPciDss321": true,`
        
    -   `"awsNist80053Rev5": true,`
        
    -   `"awsSoc2": true,`
        
    -   `"awsNist800171Rev2": true,`
        
    -   `"awsNistCsf": true,`
        
    -   `"awsCmmc102": true,`
        
    -   `"awsHipaa": true,`
        
    -   `"awsIso270012013": true`
        
    
    `},`
    
-   `"type": "Report"`
    

`}`

### Response samples

-   201
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"mcGuid": "QA42F6C8_83...",`
        
    -   `"filters": {},`
        
    -   `"intgGuidList": [],`
        
    -   `"reportNotificationTypes": {},`
        
    -   `"type": "Report"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ReportRules/paths/~1api~1v2~1ReportRules/get)List All Report Rules

List all report rules in your Lacework instance, by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/ReportRules`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ReportRules/paths/~1api~1v2~1ReportRules~1search/post)Search Report Rules

Search all report rules in your Lacework instance by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/ReportRules/search`

To limit the returned result, optionally specify one or more filters in the request body. For more information about using filters, see the [Simple & Advanced Search section](https://docs.lacework.net/api/v2/docs/#tag/OVERVIEW).

Here are some example `body` payloads:

-   `{ "filters": [ { "expression": "eq", "field": "name", "value": " Jane" } ] }`
    
-   `{ "filters": [ { "field": "mcGuid", "expression": "rlike", "value": "123ABC" } ] }`
    
-   `{ "filters": [ { "field": "mcGuid", "expression": "between", "values": [ "ABC_123", "DEC_456" ] } ] }`
    
-   `{ "filters": [ { "field": "intgGuidList", "expression": "eq", "value": "ABC_123" } ] }`
    
-   `{ "filters": [ { "field": "intgGuidList", "expression": "in", "values": [ "ABC_123", "DEF_456" ] } ] }`
    
-   `{ "filters": [ { "field": "filters.name", "expression": "ilike", "value": "slack" } ] }`
    
-   `{ "filters": [ { "field": "filters.resourceGroups", "expression": "eq", "value": "ABC_123" } ] }`
    
-   `{ "filters": [ { "field": "filters.severity", "expression": "eq", "value": "5" } ] }`
    
-   `{ "filters": [ { "field": "filters.eventCategory", "expression": "eq", "value": "App" } ] }`
    
-   `{ "filters": [ { "field": "reportNotificationTypes.agentEvents", "expression": "eq", "value": "false" } ] }`
    

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ReportRules/paths/~1api~1v2~1ReportRules~1{mcGuid}/get)Report Rule Details

Get details about a report rule by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/ReportRules/{mcGuid}`

Replace `{mcGuid}` with the `mcGuid` value returned for a report rule in the response when invoking the following endpoint: `GET /api/v2/ReportRules`.

##### path Parameters

<table><tbody><tr><td kind="field" title="mcGuid"><span></span><span>mcGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"mcGuid": "QA42F6C8_83...",`
        
    -   `"filters": {},`
        
    -   `"intgGuidList": [],`
        
    -   `"reportNotificationTypes": {},`
        
    -   `"type": "Report"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ReportRules/paths/~1api~1v2~1ReportRules~1{mcGuid}/patch)Update Report Rules

Update a report rule by specifying parameters in the request body when invoking the following endpoint:

> `PATCH https://YourLacework.lacework.net/api/v2/ReportRules/{mcGuid}`

Replace `{mcGuid}` with the `mcGuid` value returned for a report rule in the response, when the `GET /api/v2/ReportRules` endpoint is invoked.

In addition, if the severity field doesn't exist for the report rule being updated, the severity field is required if you add any of the following report types: `awsCloudtrailEvents`, `awsComplianceEvents`, `azureActivityLogEvents`, `azureComplianceEvents`, `gcpAuditTrailEvents`, `gcpComplianceEvents`, `openShiftComplianceEvents`, `platformEvents`, `agentEvents`.

##### path Parameters

<table><tbody><tr><td kind="field" title="mcGuid"><span></span><span>mcGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>When sending a request, use this object to define the new report rule. When included in a response, this object contains details of a report rule. You can use these attributes when searching for existing report rules by invoking a GET request.</p></div></div></td></tr><tr><td kind="field" title="intgGuidList"><span></span><span>intgGuidList</span></td><td><div><p><span>Array of </span><span>strings</span><span> <span>non-empty </span><span>unique</span></span></p><div><p>The alert channels for the rule to access.</p></div></div></td></tr><tr><td kind="field" title="reportNotificationTypes"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The report types that you want the rule to apply to.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": {`
    
    -   `"name": "string",`
        
    -   `"description": "string",`
        
    -   `"enabled": 1,`
        
    -   `"resourceGroups": [],`
        
    -   `"severity": [ ]`
        
    
    `},`
    
-   `"intgGuidList": [`
    
    -   `"string"`
        
    
    `],`
    
-   `"reportNotificationTypes": {`
    
    -   `"agentEvents": true,`
        
    -   `"awsCis14": true,`
        
    -   `"awsCisS3": true,`
        
    -   `"awsCloudtrailEvents": true,`
        
    -   `"awsComplianceEvents": true,`
        
    -   `"awsCis14IsoIec270022022": true,`
        
    -   `"awsCyberEssentials22": true,`
        
    -   `"awsCsaCcm405": true,`
        
    -   `"azureActivityLogEvents": true,`
        
    -   `"azureCis": true,`
        
    -   `"azureCis131": true,`
        
    -   `"azureComplianceEvents": true,`
        
    -   `"azurePci": true,`
        
    -   `"azurePciRev2": true,`
        
    -   `"azureSoc": true,`
        
    -   `"azureSocRev2": true,`
        
    -   `"azureIso27001": true,`
        
    -   `"azureHipaa": true,`
        
    -   `"azureNistCsf": true,`
        
    -   `"azureNist80053Rev5": true,`
        
    -   `"azureNist800171Rev2": true,`
        
    -   `"gcpAuditTrailEvents": true,`
        
    -   `"gcpCis": true,`
        
    -   `"gcpComplianceEvents": true,`
        
    -   `"gcpHipaa": true,`
        
    -   `"gcpHipaaRev2": true,`
        
    -   `"gcpIso27001": true,`
        
    -   `"gcpCis12": true,`
        
    -   `"gcpCis13": true,`
        
    -   `"gcpK8s": true,`
        
    -   `"gcpPci": true,`
        
    -   `"gcpPciRev2": true,`
        
    -   `"gcpSoc": true,`
        
    -   `"gcpSocRev2": true,`
        
    -   `"gcpNistCsf": true,`
        
    -   `"gcpNist80053Rev4": true,`
        
    -   `"gcpNist800171Rev2": true,`
        
    -   `"hipaa": true,`
        
    -   `"iso2700": true,`
        
    -   `"k8sAuditLogEvents": true,`
        
    -   `"nist800-53Rev4": true,`
        
    -   `"nist800-171Rev2": true,`
        
    -   `"openShiftCompliance": true,`
        
    -   `"openShiftComplianceEvents": true,`
        
    -   `"pci": true,`
        
    -   `"platformEvents": true,`
        
    -   `"soc": true,`
        
    -   `"awsSocRev2": true,`
        
    -   `"trendReport": true,`
        
    -   `"awsPciDss321": true,`
        
    -   `"awsNist80053Rev5": true,`
        
    -   `"awsSoc2": true,`
        
    -   `"awsNist800171Rev2": true,`
        
    -   `"awsNistCsf": true,`
        
    -   `"awsCmmc102": true,`
        
    -   `"awsHipaa": true,`
        
    -   `"awsIso270012013": true`
        
    
    `}`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"mcGuid": "QA42F6C8_83...",`
        
    -   `"filters": {},`
        
    -   `"intgGuidList": [],`
        
    -   `"reportNotificationTypes": {},`
        
    -   `"type": "Report"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ReportRules/paths/~1api~1v2~1ReportRules~1{mcGuid}/delete)Delete Report Rules

Delete a report rule by invoking the following endpoint:

> `DELETE https://YourLacework.lacework.net/api/v2/ReportRules/{mcGuid}`

Replace `{mcGuid}` with the `mcGuid` value returned for a report rule in the response when invoking the following endpoint: `GET /api/v2/ReportRules`.

##### path Parameters

<table><tbody><tr><td kind="field" title="mcGuid"><span></span><span>mcGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Reports)Reports

Lacework combines details about non-compliant resources that are in violation into reports. You must configure at least one cloud integration with AWS, Azure, or GCP to receive these reports.

## [](https://docs.lacework.net/api/v2/docs#tag/Reports/paths/~1api~1v2~1Reports/get)Reports

Get a specific report by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/Reports?primaryQueryId={primaryQueryId}&secondaryQueryId={secondaryQueryId}&format={format}&reportType={reportType}&severity={severity}&status={status}`

Examples:

> `GET https://YourLacework.lacework.net/api/v2/Reports?primaryQueryId=343523252&format=json&reportType=HIPAA&severity=critical,high,medium&status=Compliant,NonCompliant`

##### query Parameters

<table><tbody><tr><td kind="field" title="primaryQueryId"><span></span><span>primaryQueryId</span></td><td><div><p><span></span><span>string</span></p><div><p>The primary ID that is used to fetch the report; for example, AWS Account ID or Azure Tenant ID.</p><p><strong>Note:</strong> For GCP, use the <code>secondaryQueryId</code> attribute to provide your GCP Project ID.</p></div></div></td></tr><tr><td kind="field" title="secondaryQueryId"><span></span><span>secondaryQueryId</span></td><td><div><p><span></span><span>string</span></p><div><p>The secondary ID that is used to fetch the report; for example, GCP Project ID or Azure Subscription ID.</p><p><strong>Note:</strong> For AWS, this parameter is not required.</p><p>Use the GCP Projects or Azure Subscriptions endpoints in the <a href="https://docs.lacework.net/api/v2/docs#tag/Configs">Configurations API</a> to get the IDs to use. Be sure to provide only the ID as this parameter value, excluding the project or subscription alias. That is, use "81A2D8F9-F8B6-3A5D-B3C7-99680EF0B89F", not "81A2D8F9-F8B6-3A5D-B3C7-99680EF0B89F (Pay-As-You-Go)".</p></div></div></td></tr><tr><td kind="field" title="format"><span></span><span>format</span></td><td><div><p><span></span><span>string</span></p><p><span>Default: </span><span>"pdf"</span></p><p><span>Enum:</span> <span>"json"</span> <span>"pdf"</span> <span>"csv"</span> <span>"html"</span></p><div><p>The report's format.</p></div></div></td></tr><tr><td kind="field" title="reportType"><span></span><span>reportType</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"AWS_CIS_14"</span> <span>"AZURE_CIS_1_5"</span> <span>"GCP_CIS13"</span></p><div><p>The name of the report type in API format, for example, AZURE_NIST_CSF_CIS_1_5. See <a href="https://docs.lacework.net/console/compliance-frameworks">Compliance Frameworks</a> for a list of available reports.</p><p><strong>Note:</strong> Use <code>reportName</code> to get the report by the report definition's name instead.</p></div></div></td></tr><tr><td kind="field" title="severity"><span></span><span>severity</span></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"critical"</span> <span>"high"</span> <span>"medium"</span> <span>"low"</span> <span>"info"</span></p><div><p>Severities to filter the report on, e.g. <code>severity=critical,high,medium</code>.</p></div></div></td></tr><tr><td kind="field" title="status"><span></span><span>status</span></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"Compliant"</span> <span>"NonCompliant"</span> <span>"Suppressed"</span> <span>"CouldNotAssess"</span> <span>"Manual"</span></p><div><p>Statuses to filter the report on, e.g. <code>status=Compliant,NonCompliant</code>.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ResourceGroups)Resource Groups

Resource groups provide a way to categorize Lacework-identifiable assets.

## [](https://docs.lacework.net/api/v2/docs#tag/ResourceGroups/paths/~1api~1v2~1ResourceGroups/post)Create Resource Group

Create a resource group by specifying parameters in the request body when invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/ResourceGroups`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="resourceName"><span></span><span>resourceName</span><p>required</p></td><td><div><p><span></span><span>string</span><span> <span>non-empty </span></span><span>(?!^ +$)^.+$</span></p><div><p>The resource group's name.</p></div></div></td></tr><tr><td kind="field" title="resourceType"><span></span><span>resourceType</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Default: </span><span>"AWS"</span></p><div><p>The resource type such as cloud accounts, containers, or machines.</p></div><p><label>AWS</label></p></div></td></tr><tr><td kind="field" title="enabled"><span></span><span>enabled</span></td><td><div><p><span></span><span>number</span></p><p><span>Enum:</span> <span>0</span> <span>1</span></p><div><p>When sending a request, use this attribute to enable or disable a resource group. When included in a response, returns <code>1</code> for enabled resource groups, or returns <code>0</code> for disabled resource groups.</p></div></div></td></tr><tr><td kind="field" title="props"><span></span><p>required</p></td><td><div><p><span></span><span>object</span></p><div><p>The new resource group's properties. The data varies based on the value of the <code>type</code> attribute.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"resourceName": "string",`
    
-   `"resourceType": "AWS",`
    
-   `"enabled": 1,`
    
-   `"props": {`
    
    -   `"description": "string",`
        
    -   `"accountIds": []`
        
    
    `}`
    

`}`

### Response samples

-   201
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"guid": "LW_XYZ...",`
        
    -   `"isDefault": 1,`
        
    -   `"resourceGuid": "LWABC...",`
        
    -   `"resourceName": "AWS Resource Group",`
        
    -   `"resourceType": "AWS",`
        
    -   `"enabled": 1,`
        
    -   `"props": {},`
        
    -   `"isDefaultInteger": 1,`
        
    -   `"propsJson": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ResourceGroups/paths/~1api~1v2~1ResourceGroups/get)List All Resource Groups

Get a list of all resource groups for the account by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/ResourceGroups`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ResourceGroups/paths/~1api~1v2~1ResourceGroups~1search/post)Search Resource Groups

Search resource groups by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/ResourceGroups/search`

To limit the returned result, optionally specify one or more filters in the request body. For more information about using filters, see the [Simple & Advanced Search section](https://docs.lacework.net/api/v2/docs/#tag/OVERVIEW).

In the request body, optionally specify the list of fields to return in the response by specifying the list in the `returns` array, for example, `"returns":[ "name", "type", "enabled" ]`.

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ResourceGroups/paths/~1api~1v2~1ResourceGroups~1{resourceGuid}/get)Resource Groups Details

Get details about a resource group by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/ResourceGroups/{resourceGuid}`

##### path Parameters

<table><tbody><tr><td kind="field" title="resourceGuid"><span></span><span>resourceGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"guid": "LW_XYZ...",`
        
    -   `"isDefault": 1,`
        
    -   `"resourceGuid": "LWABC...",`
        
    -   `"resourceName": "AWS Resource Group",`
        
    -   `"resourceType": "AWS",`
        
    -   `"enabled": 1,`
        
    -   `"props": {},`
        
    -   `"isDefaultInteger": 1,`
        
    -   `"propsJson": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ResourceGroups/paths/~1api~1v2~1ResourceGroups~1{resourceGuid}/patch)Update Resource Groups

Update a resource group by specifying parameters in the request body when invoking the following endpoint:

> `PATCH https://YourLacework.lacework.net/api/v2/ResourceGroups/{resourceGuid}`

In the request body, only specify the parameters that you want to update, for example, `{ "enabled" : 0 }`.

##### path Parameters

<table><tbody><tr><td kind="field" title="resourceGuid"><span></span><span>resourceGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

Only specify the parameter(s) that you want to update, for example, `{ "enabled" : 0 }`.

<table><tbody><tr><td kind="field" title="resourceName"><span></span><span>resourceName</span></td><td><div><p><span></span><span>string</span><span> <span>non-empty </span></span><span>(?!^ +$)^.+$</span></p><div><p>The resource group's name.</p></div></div></td></tr><tr><td kind="field" title="resourceType"><span></span><span>resourceType</span></td><td><div><p><span></span><span>string</span></p><p><span>Default: </span><span>"AWS"</span></p><div><p>The resource type such as cloud accounts, containers, or machines.</p></div><p><label>AWS</label></p></div></td></tr><tr><td kind="field" title="enabled"><span></span><span>enabled</span></td><td><div><p><span></span><span>number</span></p><p><span>Enum:</span> <span>0</span> <span>1</span></p><div><p>When sending a request, use this attribute to enable or disable a resource group. When included in a response, returns <code>1</code> for enabled resource groups, or returns <code>0</code> for disabled resource groups.</p></div></div></td></tr><tr><td kind="field" title="props"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The new resource group's properties. The data varies based on the value of the <code>type</code> attribute.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"resourceName": "string",`
    
-   `"resourceType": "AWS",`
    
-   `"enabled": 1,`
    
-   `"props": {`
    
    -   `"description": "string",`
        
    -   `"accountIds": []`
        
    
    `}`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"guid": "LW_XYZ...",`
        
    -   `"isDefault": 1,`
        
    -   `"resourceGuid": "LWABC...",`
        
    -   `"resourceName": "AWS Resource Group",`
        
    -   `"resourceType": "AWS",`
        
    -   `"enabled": 1,`
        
    -   `"props": {},`
        
    -   `"isDefaultInteger": 1,`
        
    -   `"propsJson": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/ResourceGroups/paths/~1api~1v2~1ResourceGroups~1{resourceGuid}/delete)Delete Resource Groups

Delete a resource group by invoking the following endpoint:

> `DELETE https://YourLacework.lacework.net/api/v2/ResourceGroups/{resourceGuid}`

##### path Parameters

<table><tbody><tr><td kind="field" title="resourceGuid"><span></span><span>resourceGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/TeamMembers)Team Members (Deprecated)

Team members can be granted access to multiple Lacework accounts and have different roles for each account. Team members can also be granted organization-level roles. For more information, see [Team Members](https://docs.lacework.com/console/team-members-nav).

**Note**: The TeamMembers API is deprecated and is unavailable if you have migrated to the new RBAC model in your Lacework Console. See [Access Control](https://docs.lacework.com/console/access-control-nav) for more information about the new RBAC model.

## [](https://docs.lacework.net/api/v2/docs#tag/TeamMembers/paths/~1api~1v2~1TeamMembers/post)Create Team Members Deprecated

Create a team member in your Lacework instance by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/TeamMembers`

Here is an example `body` payload:

> `{ "userName": "jane.smith@mycompany.com", "userEnabled": 1, "props": { "firstName": "Jane", "lastName": "Smith", "company": "myCompany", "accountAdmin": true } }`

**Note**: This API is deprecated and is unavailable if you have migrated to the new RBAC model in your Lacework Console. See [Access Control](https://docs.lacework.com/console/access-control-nav) for more information about the new RBAC model.

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="schemaOption"><span></span><span>schemaOption</span></td><td><div><p><span></span><span>string</span></p><div><p>Not required.</p></div><p><label>With_Org-Access</label></p></div></td></tr><tr><td kind="field" title="props"><span></span><p>required</p></td><td><div><p><span></span><span>object</span></p></div></td></tr><tr><td kind="field" title="orgAdmin"><span></span><span>orgAdmin</span></td><td><div><p><span></span><span>boolean</span></p><p><span>Default: </span><span>false</span></p><div><p>When sending a request, set to <code>True</code> to make the team member an organization admin. Otherwise, set to <code>False</code>. When included in a response, returns the role assigned to the team member. <strong>Note:</strong> If the team member is currently an organization admin, Lacework ignores the <code>adminRoleAccounts</code> and <code>userRoleAccounts</code> attributes.</p></div></div></td></tr><tr><td kind="field" title="orgUser"><span></span><span>orgUser</span></td><td><div><p><span></span><span>boolean</span></p><p><span>Default: </span><span>false</span></p><div><p>When sending a request, set to <code>True</code> to make the new member an organization user. Otherwise, set to <code>False</code> When included in a response, returns the role assigned to the new member. <strong>Note:</strong> If the team member is currently an organization user, Lacework will ignore the <code>userRoleAccounts</code> attribute.</p></div></div></td></tr><tr><td kind="field" title="adminRoleAccounts"><span></span><span>adminRoleAccounts</span><p>required</p></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>A list of account names for which this team member will be an admin.</p></div></div></td></tr><tr><td kind="field" title="userRoleAccounts"><span></span><span>userRoleAccounts</span><p>required</p></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>A list of account names for which this team member will be a user.</p></div></div></td></tr><tr><td kind="field" title="userEnabled"><span></span><span>userEnabled</span><p>required</p></td><td><div><p><span></span><span>integer</span></p><p><span>Enum:</span> <span>1</span> <span>0</span></p></div></td></tr><tr><td kind="field" title="userName"><span></span><span>userName</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>user email address</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"schemaOption": "With_Org-Access",`
    
-   `"props": {`
    
    -   `"firstName": "string",`
        
    -   `"lastName": "string",`
        
    -   `"company": "string",`
        
    -   `"accountAdmin": false`
        
    
    `},`
    
-   `"orgAdmin": false,`
    
-   `"orgUser": false,`
    
-   `"adminRoleAccounts": [`
    
    -   `"string"`
        
    
    `],`
    
-   `"userRoleAccounts": [`
    
    -   `"string"`
        
    
    `],`
    
-   `"userEnabled": 1,`
    
-   `"userName": "string"`
    

`}`

### Response samples

-   201
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"userName": "user1@example.com",`
        
    -   `"orgAccount": true,`
        
    -   `"url": "url",`
        
    -   `"orgAdmin": false,`
        
    -   `"orgUser": false,`
        
    -   `"accounts": []`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/TeamMembers/paths/~1api~1v2~1TeamMembers/get)List All Team Members Deprecated

Get a list of team members in your Lacework instance by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/TeamMembers`

**Note**: This API is deprecated and is unavailable if you have migrated to the new RBAC model in your Lacework Console. See [Access Control](https://docs.lacework.com/console/access-control-nav) for more information about the new RBAC model.

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/TeamMembers/paths/~1api~1v2~1TeamMembers~1search/post)Search Team Members Deprecated

Search all team members in your Lacework instance by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/TeamMembers/search`

To limit the returned result, optionally specify one or more filters in the request body. For more information about using filters, see the [Simple & Advanced Search section](https://docs.lacework.net/api/v2/docs/#tag/OVERVIEW).

You can filter on the following fields:

-   `custGuid`
    
-   `userGuid`
    
-   `userName`
    
-   `userEnabled`
    

Here is an example `body` payload:

> `{ "filters" : [ { "expression": "eq", "field": "userName", "value": "jane.smith@mycompany.com" } ] }`

**Note**: This API is deprecated and is unavailable if you have migrated to the new RBAC model in your Lacework Console. See [Access Control](https://docs.lacework.com/console/access-control-nav) for more information about the new RBAC model.

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/TeamMembers/paths/~1api~1v2~1TeamMembers~1{userGuid}/get)Team Member Details Deprecated

Get details about a team member by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/TeamMembers/{userGuid}`

Replace `{userGuid}` with the `userGuid` value returned for a team member in the response when invoking the following endpoint: `GET /api/v2/TeamMembers`

**Note**: This API is deprecated and is unavailable if you have migrated to the new RBAC model in your Lacework Console. See [Access Control](https://docs.lacework.com/console/access-control-nav) for more information about the new RBAC model.

##### path Parameters

<table><tbody><tr><td kind="field" title="userGuid"><span></span><span>userGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"userName": "user1@example.com",`
        
    -   `"orgAccount": true,`
        
    -   `"url": "url",`
        
    -   `"orgAdmin": false,`
        
    -   `"orgUser": false,`
        
    -   `"accounts": []`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/TeamMembers/paths/~1api~1v2~1TeamMembers~1{userGuid}/patch)Update Team Member Deprecated

Optionally update the `userName` and`userEnabled` settings and the `props` sub-settings of the passed in team member. Update these settings by invoking the following endpoint:

> `PATCH https://YourLacework.lacework.net/api/v2/TeamMembers/{userGuid}`

Replace `{userGuid}` with the `userGuid` value returned for a team member in the response, when invoking the following endpoint: `GET /api/v2/TeamMembers`.

Here is an example `body` payload:

> `{ "props": {"firstName":"Jane"} }`

**Note**: This API is deprecated and is unavailable if you have migrated to the new RBAC model in your Lacework Console. See [Access Control](https://docs.lacework.com/console/access-control-nav) for more information about the new RBAC model.

##### path Parameters

<table><tbody><tr><td kind="field" title="userGuid"><span></span><span>userGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="schemaOption"><span></span><span>schemaOption</span></td><td><div><p><span></span><span>string</span></p><div><p>Not required.</p></div><p><label>With_Org-Access</label></p></div></td></tr><tr><td kind="field" title="props"><span></span></td><td><div><p><span></span><span>object</span></p></div></td></tr><tr><td kind="field" title="orgAdmin"><span></span><span>orgAdmin</span></td><td><div><p><span></span><span>boolean</span></p><p><span>Default: </span><span>false</span></p><div><p>When sending a request, set to <code>True</code> to make the team member an organization admin. Otherwise, set to <code>False</code>. When included in a response, returns the role assigned to the team member. <strong>Note:</strong> If the team member is currently an organization admin, Lacework ignores the <code>adminRoleAccounts</code> and <code>userRoleAccounts</code> attributes.</p></div></div></td></tr><tr><td kind="field" title="orgUser"><span></span><span>orgUser</span></td><td><div><p><span></span><span>boolean</span></p><p><span>Default: </span><span>false</span></p><div><p>When sending a request, set to <code>True</code> to make the new member an organization user. Otherwise, set to <code>False</code> When included in a response, returns the role assigned to the new member. <strong>Note:</strong> If the team member is currently an organization user, Lacework will ignore the <code>userRoleAccounts</code> attribute.</p></div></div></td></tr><tr><td kind="field" title="adminRoleAccounts"><span></span><span>adminRoleAccounts</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>A list of account names for which this team member will be an admin.</p></div></div></td></tr><tr><td kind="field" title="userRoleAccounts"><span></span><span>userRoleAccounts</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>A list of account names for which this team member will be a user.</p></div></div></td></tr><tr><td kind="field" title="userEnabled"><span></span><span>userEnabled</span></td><td><div><p><span></span><span>integer</span></p><p><span>Enum:</span> <span>1</span> <span>0</span></p></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"schemaOption": "With_Org-Access",`
    
-   `"props": {`
    
    -   `"firstName": "string",`
        
    -   `"lastName": "string",`
        
    -   `"company": "string",`
        
    -   `"accountAdmin": false`
        
    
    `},`
    
-   `"orgAdmin": false,`
    
-   `"orgUser": false,`
    
-   `"adminRoleAccounts": [`
    
    -   `"string"`
        
    
    `],`
    
-   `"userRoleAccounts": [`
    
    -   `"string"`
        
    
    `],`
    
-   `"userEnabled": 1`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"userName": "user1@example.com",`
        
    -   `"orgAccount": true,`
        
    -   `"url": "url",`
        
    -   `"orgAdmin": false,`
        
    -   `"orgUser": false,`
        
    -   `"accounts": []`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/TeamMembers/paths/~1api~1v2~1TeamMembers~1{userGuid}/delete)Delete Team Member Deprecated

Delete a team member by invoking the following endpoint:

> `DELETE https://YourLacework.lacework.net/api/v2/TeamMembers/{userGuid}`

Replace `{userGuid}` with the `userGuid` value returned for a team member in the response when invoking the following endpoint: `GET /api/v2/TeamMembers`

**Note**: This API is deprecated and is unavailable if you have migrated to the new RBAC model in your Lacework Console. See [Access Control](https://docs.lacework.com/console/access-control-nav) for more information about the new RBAC model.

##### path Parameters

<table><tbody><tr><td kind="field" title="userGuid"><span></span><span>userGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/TeamUsers)Team Users

Role-based access control (RBAC) gives you control over user access to resources based on a defined role at an account level.

The Team Users API works with the new Lacework role-based access control (RBAC) model. After you enable RBAC in the Lacework Console, the Team Users API is available and the legacy Team Members API (deprecated) is disabled. For more information on the legacy API, see the [Team Members APIs](https://docs.lacework.com/api/v2/docs/#tag/TeamMembers).

The Team Users API works with users and groups at the account level only; organization-level users are not supported. For information on working with account level users in the Lacework Console, see [Access Control at Account Level](https://docs.lacework.com/onboarding/access-control-account-level).

The Lacework RBAC model defines two types of users: standard users and service users. Standard user accounts are typically associated with specific people in your organization, while service users are often shared among people and typically represent a service, client, or other type of programmatic Lacework integration.

See [Access Control Overview](https://docs.lacework.com/onboarding/access-control-overview) for details on users and groups in Lacework.

## [](https://docs.lacework.net/api/v2/docs#tag/TeamUsers/paths/~1api~1v2~1TeamUsers/post)Create Team Users

Create a standard or service user in a Lacework account using the following endpoint:

> `POST /api/v2/TeamUsers`

In the request body, specify the type of user to create, a standard user or service user, as well as properties of the user.

Here is an example `body` payload for a standard user:

> `{"type": "StandardUser", "name": "name_one", "company": "company_name", "email": "test_email", "userEnabled": 1}`

Here is an example `body` payload for a service user:

> `{"type": "ServiceUser", "name": "name_one", "description": "service_user_description", "userEnabled": 1}`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="type"><span></span><span>type</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>The user type. This type cannot be changed after the user is created.</p></div><p><label>StandardUser</label></p></div></td></tr><tr><td kind="field" title="name"><span></span><span>name</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>A name for the standard user.</p></div></div></td></tr><tr><td kind="field" title="userEnabled"><span></span><span>userEnabled</span></td><td><div><p><span></span><span>number</span></p><p><span>Default: </span><span>1</span></p><p><span>Enum:</span> <span>0</span> <span>1</span></p><div><p>When sending a request, use this attribute to enable or disable a team user's access. When included in a response, returns <code>1</code> for enabled team users, or returns <code>0</code> for disabled team users. NOTE: This will eventually change to being <code>true</code>/<code>false</code>.</p></div></div></td></tr><tr><td kind="field" title="company"><span></span><span>company</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>The name of the business or organization associated with the user.</p></div></div></td></tr><tr><td kind="field" title="email"><span></span><span>email</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>The user's email address.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"type": "StandardUser",`
    
-   `"name": "string",`
    
-   `"userEnabled": 0,`
    
-   `"company": "string",`
    
-   `"email": "string"`
    

`}`

### Response samples

-   201
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"name": "Support",`
        
    -   `"company": "LW",`
        
    -   `"email": "user@example.com",`
        
    -   `"userGuid": "LWXYZ...",`
        
    -   `"userEnabled": 1,`
        
    -   `"type": "StandardUser",`
        
    -   `"userGroups": [],`
        
    -   `"lastLoginTime": 1234567891011,`
        
    -   `"orgAccess": "NO_ORG_ACCESS"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/TeamUsers/paths/~1api~1v2~1TeamUsers/get)List All Team Users

Get a list of all users in a Lacework account, including both standard and service users, by invoking the following endpoint:

> `GET /api/v2/TeamUsers`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/TeamUsers/paths/~1api~1v2~1TeamUsers~1{id}/get)Team Users Details

Get details about a user in a Lacework Account by invoking the following endpoint:

> `GET /api/v2/TeamUsers/{userGuid}`

Replace `{userGuid}` with the `userGuid` value of the standard or service user whose details you want to retrieve. You can get the `userGuid` for a user in the response to the "List All Team Users" endpoint.

##### path Parameters

<table><tbody><tr><td kind="field" title="id"><span></span><span>id</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"name": "Support",`
        
    -   `"company": "LW",`
        
    -   `"email": "user@example.com",`
        
    -   `"userGuid": "LWXYZ...",`
        
    -   `"userEnabled": 1,`
        
    -   `"type": "StandardUser",`
        
    -   `"userGroups": [],`
        
    -   `"lastLoginTime": 1234567891011,`
        
    -   `"orgAccess": "NO_ORG_ACCESS"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/TeamUsers/paths/~1api~1v2~1TeamUsers~1{id}/patch)Update Team Users

Update an existing standard or service user by providing new values for the user properties to update using the following endpoint:

> `PATCH /api/v2/TeamUsers/{userGuid}`

Replace `{userGuid}` with the `userGuid` value of the user you want to update. You can get the `userGuid` for a user in the response to the "List All Team Users" endpoint.

Here is an example `body` payload for a standard user:

> `{"name": "new_name", "userEnabled": 0}`

Here is an example `body` payload for a service user:

> `{"name": "new_name", "userEnabled": 0, "description": "new_description"}`

##### path Parameters

<table><tbody><tr><td kind="field" title="id"><span></span><span>id</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="type"><span></span><span>type</span></td><td><div><p><span></span><span>string</span></p><div><p>The user type. This type cannot be changed after the user is created.</p></div><p><label>StandardUser</label></p></div></td></tr><tr><td kind="field" title="name"><span></span><span>name</span></td><td><div><p><span></span><span>string</span></p><div><p>A name for the standard user.</p></div></div></td></tr><tr><td kind="field" title="userEnabled"><span></span><span>userEnabled</span></td><td><div><p><span></span><span>number</span></p><p><span>Default: </span><span>1</span></p><p><span>Enum:</span> <span>0</span> <span>1</span></p><div><p>When sending a request, use this attribute to enable or disable a team user's access. When included in a response, returns <code>1</code> for enabled team users, or returns <code>0</code> for disabled team users. NOTE: This will eventually change to being <code>true</code>/<code>false</code>.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"type": "StandardUser",`
    
-   `"name": "string",`
    
-   `"userEnabled": 0`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"name": "Support",`
        
    -   `"company": "LW",`
        
    -   `"email": "user@example.com",`
        
    -   `"userGuid": "LWXYZ...",`
        
    -   `"userEnabled": 1,`
        
    -   `"type": "StandardUser",`
        
    -   `"userGroups": [],`
        
    -   `"lastLoginTime": 1234567891011,`
        
    -   `"orgAccess": "NO_ORG_ACCESS"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/TeamUsers/paths/~1api~1v2~1TeamUsers~1{id}/delete)Delete Team Users

Delete a service or standard user to remove access for the user to the Lacework Console and Lacework APIs. Delete a user account using the following endpoint:

> `DELETE /api/v2/TeamUsers/{userGuid}`

Replace `{userGuid}` with the `userGuid` value of the standard or service user whose details you want to retrieve. You can get the `userGuid` for a user in the response to the "List All Team Users" endpoint.

##### path Parameters

<table><tbody><tr><td kind="field" title="id"><span></span><span>id</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/TemplateFiles)Template Files

Template Files are equivalent to CloudFormation template files.

**AWS Config**

For the file parameter, specify AwsConfig to download an AWS Config CloudFormation template for configuring an AWS Config integration to analyze AWS configuration compliance.

**AWS Cloud Trail**

For the file parameter, specify AwsCloudTrail to download an AWS CloudTrail CloudFormation template for configuring an AWS CloudTrail integration to monitor cloud account security.

**AWS EKS Audit Logs**

For the file parameter, specify AwsEksAudit to download an AWS EKS Audit Log template for configuring resources to allow monitoring of Kubernetes runtime security using audit logs on EKS [(Step 1)](https://docs.lacework.com/eks-audit-log-integration-overview#what-happens-during-step-1).

For the file parameter, specify AwsEksAuditSubscriptionFilter to download an AWS EKS Audit Log template for configuring an EKS cluster log group to monitor EKS runtime security. Optionally pass in `intgGuid` as a query parameter. This allows the intgGuid to get the SNS ARN, create the firehose ARN, and insert that into the template before returning it. This means you don't have to find the firehoseARN and insert it manually. Obtain the integration's intgGuid by using the `GET https://YourLacework.lacework.net/api/v2/CloudAccounts` endpoint [(Step 2)](https://docs.lacework.com/eks-audit-log-integration-overview#what-happens-during-step-2).

After downloading the template, you must upload and run the template file in the AWS Console. For information about setting up AWS CloudTrail and AWS Config integrations, see [AWS Integration Using CloudFormation](https://docs.lacework.net/onboarding/aws-integration-with-cloudformation). For information on EKS Audit Log integration, see [EKS Audit Log Integration](https://docs.lacework.com/onboarding/eks-audit-log-integration-overview). You must also create the integration in the Lacework Console.

## [](https://docs.lacework.net/api/v2/docs#tag/TemplateFiles/paths/~1api~1v2~1TemplateFiles~1{templateFileName}/get)Download Template File

Download the CloudFormation template from the Lacework Console for a specific template file name by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/TemplateFiles/{templateFileName}`

Here is an example invocation:

> `GET https://YourLacework.lacework.net/api/v2/TemplateFiles/AwsConfig`

Here is another example invocation:

> `GET https://YourLacework.lacework.net/api/v2/TemplateFiles/AwsCloudTrail`

Optionally pass in `intgGuid` as a query parameter for the `AwsEksAuditSubscriptionFilter` template file name. Here is an example invocation:

> `GET https://YourLacework.lacework.net/api/v2/TemplateFiles/AwsEksAuditSubscriptionFilter?intgGuid=ROIJ898329....`

##### path Parameters

<table><tbody><tr><td kind="field" title="templateFileName"><span></span><span>templateFileName</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"AwsCloudTrail"</span> <span>"AwsConfig"</span></p><div><p>The template's filename to download.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/UserGroups)User Groups

A [user group](https://docs.lacework.com/console/access-control-nav#view-user-groups-page) associates Lacework service and standard users with specific permissions in Lacework. See [Team Users](https://docs.lacework.net/api/v2/docs#tag/TeamUsers) for information about service and standard users.

## [](https://docs.lacework.net/api/v2/docs#tag/UserGroups/paths/~1api~1v2~1UserGroups~1{userGroupGuid}~1addUsers/post)Add Users to User Groups

Add one or more users to an existing user group using the following endpoint:

> `POST /api/v2/UserGroups/{userGroupGuid}/addUsers`

Replace `{userGroupGuid}` with the `userGroupGuid` value of the user group you want to add users to. You can get the `userGroupGuid` for a user group from the User Groups section under Settings in the Lacework platform.

In the request body, specify the users to add to the group as an array of user IDs.

Here is an example body payload:

`{"userGuids": ["some_user_id"]}`

See [Add Standard Users to a User Group](https://docs.lacework.com/onboarding/access-control-account-level#add-standard-users-to-a-user-group) for more information.

##### path Parameters

<table><tbody><tr><td kind="field" title="userGroupGuid"><span></span><span>userGroupGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="userGuids"><span></span><span>userGuids</span><p>required</p></td><td><div><p><span>Array of </span><span>strings</span><span>[ items<span> <span>non-empty </span></span>]</span></p></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"userGuids": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"userGuids": [],`
        
    -   `"userGroupGuid": "group43p2fspfos..."`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/UserGroups/paths/~1api~1v2~1UserGroups~1{userGroupGuid}~1removeUsers/post)Remove Users from User Groups

Remove one or more users from a user group using the following endpoint:

> `POST /api/v2/UserGroups/{userGroupGuid}/removeUsers`.

Replace `{userGroupGuid}` with the `userGroupGuid` value of the user group you details to remove users from. You can get the `userGroupGuid` for a user group from the User Groups section under Settings in the Lacework platform.

In the request body, specify the users to remove from the group as an array of user IDs.

Here is an example body payload:

`{"userGuids": ["some_user_id"]}`

##### path Parameters

<table><tbody><tr><td kind="field" title="userGroupGuid"><span></span><span>userGroupGuid</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="userGuids"><span></span><span>userGuids</span><p>required</p></td><td><div><p><span>Array of </span><span>strings</span><span>[ items<span> <span>non-empty </span></span>]</span></p></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"userGuids": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/UserProfile)User Profiles

An organization can contain multiple accounts so you can also manage components such as alerts, resource groups, team members, and audit logs at a more granular level inside an organization. For more information, see [Organization Overview](https://docs.lacework.com/organization-overview).

## [](https://docs.lacework.net/api/v2/docs#tag/UserProfile/paths/~1api~1v2~1UserProfile/get)List Sub-accounts

List all sub-accounts that are managed by the `YourLacework` account by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/UserProfile`

For example, if you specify the `IT20.MyCompany` organization account in `YourLacework`, this lists all sub-accounts of the `IT20` account.

Here is an example invocation:

> `GET https://IT20.MyCompany.lacework.net/api/v2/UserProfile`

The response reports details about organization accounts and non-organization accounts in addition to authorization and privilege details.

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr><tr><td kind="field" title="Org-Access"><span></span><span>Org-Access</span></td><td><div><p><span></span><span>boolean</span></p><div><p>Use this attribute to specify if the access token has organization admin permissions. If the access token has only account permissions, use the <code>Account-Name</code> attribute to specify which account to access.</p></div></div></td></tr><tr><td kind="field" title="Account-Name"><span></span><span>Account-Name</span></td><td><div><p><span></span><span>string</span></p><div><p>Use this attribute to specify which sub-account to access.</p></div></div></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`[`

-   `{`
    
    -   `"username": "user@example.com",`
        
    -   `"orgAccount": true,`
        
    -   `"url": "url",`
        
    -   `"orgAdmin": true,`
        
    -   `"orgUser": false,`
        
    -   `"accounts": []`
        
    
    `}`
    

`]`

## [](https://docs.lacework.net/api/v2/docs#tag/Vulnerabilities)Vulnerabilities

Lacework provides the ability to assess, identify, and report vulnerabilities found in the operating system software packages in a Docker container image before the container image is deployed. Lacework also supports scanning of non-OS packages for programming languages (Java, Ruby, PHP, GO, NPM, .NET, Python).

## [](https://docs.lacework.net/api/v2/docs#tag/Vulnerabilities/paths/~1api~1v2~1Vulnerabilities~1Containers~1search/post)Search Container Vulnerabilities

Search the scan (assessment), including the risk score and scan status, the vulnerabilities found in the scan, and statistics for those vulnerabilities by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Vulnerabilities/Containers/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days. To use the current time as the end time, exclude the endTime field.

You can optionally filter returned vulnerabilities by severity, vulnerability ID, machine ID, and more. For more information, see [CONTAINER\_VULN\_DETAILS\_V View](https://docs.lacework.com/containervulndetailsv-view).

The `rlike` and `not_rlike` operators are useful for filtering results. For example, the following expression limits results to those that have `python` in their `featureKey` name field:

> `"filters": [ { "expression": "rlike", "field": "featureKey.name", "value": ".*python.*" } ]`

Here are additional example `body` payloads:

Here are some additional example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "vulnId", "expression": "eq", "value": "CVE-2018-7169" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "evalGuid", "expression": "eq", "value": "1234567a89012b34567890123cd56e78" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "evalCtx.image_info.digest", "expression": "eq", "value": "sha256:2e05f1f668367c1fc0f1c9c02ee87521ed66541e6ebf0a31905b8cdd78d22611" }, { "field": "severity", "expression": "eq", "value": "Medium" } ],`  
    `"returns": [ "imageId", "severity", "status", "vulnId", "evalCtx", "fixInfo", "featureKey" ] }`

To search for container vulnerabilities of only active containers, first use the "Search Containers" endpoint to get a list of active containers. Then call "Search Container Vulnerabilities" and pass the image IDs from the "Search Containers" results as a filter with the `in` filter type.

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 11668,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Vulnerabilities/paths/~1api~1v2~1Vulnerabilities~1Containers~1scan/post)Scan Container Vulnerabilities

Request that Lacework scans (evaluates) for vulnerabilities in the specified container image. Specify the container image by passing in a tag, repository, and registry in the body parameter. You must specify a container image and repository located in a registry domain that has already been integrated with Lacework.

For registries that are integrated using the Lacework generic `Docker V2 Registry` type, vulnerability scans can be started only by calling this API operation.

For registries that are integrated using any Lacework registry type except _"Docker V2 Registry"_, vulnerability scans start when the container registry is initially integrated, when specified by the default scan schedule, or when this operation is called.

For more information, see [https://docs.lacework.com/container-vulnerability-assessment-overview](https://docs.lacework.com/container-vulnerability-assessment-overview).

For more information about creating an API access key and token to run this operation and using this operation with organization resources, see [https://docs.lacework.com/generate-api-access-keys-and-tokens](https://docs.lacework.com/generate-api-access-keys-and-tokens).

Usage Example:

> `curl -X POST -H 'Content-Type: application/json' -d '{ "registry": "index.docker.io", "repository": "yourDockerOrg/yourRepository", "tag": "yourTag" }' "https://YourLacework.lacework.net/api/v2/Vulnerabilities/Containers/scan" -H "Authorization: Bearer YourAPIToken"`

In the JSON body, do not prefix the registry or the repository with the `http://` string.

This operation returns a unique requestId in the response that you can use to track the status of this scan/assessment.

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="registry"><span></span><span>registry</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>The container registry to be assessed.</p></div></div></td></tr><tr><td kind="field" title="repository"><span></span><span>repository</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>The repository within the container registry to be assessed.</p></div></div></td></tr><tr><td kind="field" title="tag"><span></span><span>tag</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>The identifier tag as <code>key:value</code> pairs.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"registry": "index.docker.io",`
    
-   `"repository": "yourDockerOrg/yourRepository",`
    
-   `"tag": "yourTag"`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"requestId": "abcdef124...",`
        
    -   `"status": "scanning"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Vulnerabilities/paths/~1api~1v2~1Vulnerabilities~1Containers~1scan~1{requestId}/get)Track Container Scan Status

Track the progress and return data about an on-demand vulnerability scan that was started by calling the `POST /api/v2/Vulnerabilities/Containers/scan` operation. You must pass in the unique request id returned in the response of the POST Vulnerabilities/Containers/scan operation. For example,

> `GET https://YourLacework.lacework.net/api/v2/Vulnerabilities/Containers/scan/abcdefgh-123...`

When completed, the scan operation returns an `evalGuid`, which you can use to get the results of the scan by passing it to the "Search Container Vulnerabilities" endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Vulnerabilities/Containers/search`

Pass the `evalGuid` in the request body, for example:

> `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "evalGuid", "expression": "eq", "value": "1234567a89012b34567890123cd56e78" } ] }`

##### path Parameters

<table><tbody><tr><td kind="field" title="requestId"><span></span><span>requestId</span><p>required</p></td><td></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"status": "completed",`
        
    -   `"evalGuid": "1234567a89012b34567890123cd56e78"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Vulnerabilities/paths/~1api~1v2~1Vulnerabilities~1Hosts~1search/post)Search Host Vulnerabilities

Search the scan (assessment), including the risk score and scan status, vulnerabilities found in the scan, and statistics about those vulnerabilities by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/Vulnerabilities/Hosts/search`

Lacework highly recommends specifying a time range. Without a specified time range, the request uses the default time range of 24 hours prior to the current time. The maximum time range per API request is 7 days.

Optionally filter the returned vulnerabilities by severity, vulnerability ID, machine ID, and more. For more information, see [HOST\_VULN\_DETAILS\_V View](https://docs.lacework.com/hostvulndetailsv-view).

The `rlike` and `not_rlike` operators are useful for filtering results. For example, the following expression limits results to those that have `python` in their `featureKey` name field:

> `"filters": [ { "expression": "rlike", "field": "featureKey.name", "value": ".*python.*" } ]`

Here are some additional example `body` payloads:

-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "vulnId", "expression": "eq", "value": "CVE-2018-7169" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "evalGuid", "expression": "eq", "value": "1234567a89012b34567890123cd56e78" } ] }`
-   `{ "timeFilter": { "startTime": "2021-08-28T20:30:00Z", "endTime": "2021-08-28T22:30:00Z"},` `"filters": [ { "field": "machineTags.AmiId", "expression": "eq", "value": "ami-0d9ef0d809e365a36" }, { "field": "severity", "expression": "eq", "value": "Medium" } ],`  
    `"returns": [ "mid", "props", "severity", "status", "vulnId", "evalCtx", "fixInfo", "featureKey", "machineTags" ] }`

Within request bodies, nested field names that contain one or more special characters—e.g., dot ("."), colon (":"), or slash ("/")—mus be enclosed in **escaped double quotes**. For example, the field name `aws:ec2launchtemplate:version` nested under the `machineTags` field would be rendered as follows:

`"machineTags.\"aws:ec2launchtemplate:version\""`

In a filter, the example would appear as follows:

`{ "field": "machineTags.\"aws:ec2launchtemplate:version\"", "expression": "eq", "value": "3" }`

In addition, forward slash characters within field names must be escaped with a backslash, as in the following example:

`"machineTags.\"kubernetes.io\/cluster\/prod1\""`

To search for host vulnerabilities of only online machines, first use the "Search Machines" endpoint to get a list of online machines. Then call "Search Host Vulnerabilities", passing the machine IDs from the "Search Machines" results as a filter with the `in` filter type.

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="timeFilter"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The date/time range during which actions occurred.</p></div></div></td></tr><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"timeFilter": {`
    
    -   `"startTime": "string",`
        
    -   `"endTime": "string"`
        
    
    `},`
    
-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"paging": {`
    
    -   `"rows": 5000,`
        
    -   `"totalRows": 209082,`
        
    -   `"urls": {}`
        
    
    `},`
    
-   `"data": [`
    
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Vulnerabilities/paths/~1api~1v2~1Vulnerabilities~1SoftwarePackages~1scan/post)Scan Software Packages

Request an on-demand vulnerability assessment of your software packages to determine if the packages contain any common vulnerabilities and exposures. The response for detected CVEs includes CVE details. Only packages managed by a package manager for supported operating systems are reported.

Use the body parameter to specify the list of packages to scan for. In the package list, separate each package entry with a comma. Here is the list of supported OS types with some osVer examples:

-   `{ "os": "alpine", "osVer": "v3.1" ... }`
-   `{ "os": "amzn", "osVer": "2" ... }`
-   `{ "os": "amzn", "osVer": "2018.03" ... }`
-   `{ "os": "centos", "osVer": "5" ... }`
-   `{ "os": "debian", "osVer": "unstable" ... }`
-   `{ "os": "debian", "osVer": "11" ... }`
-   `{ "os": "oracle", "osVer": "8" ... }`
-   `{ "os": "rhel", "osVer": "8" ... }`
-   `{ "os": "ubuntu", "osVer": "19.10" ... }`

For more information about creating an API access key and token to run this operation and using this operation with organization resources, see [https://docs.lacework.com/generate-api-access-keys-and-tokens](https://docs.lacework.com/generate-api-access-keys-and-tokens).

Usage Example:

> `curl -X POST -H 'Content-Type: application/json' -d '{ "osPkgInfoList": [ { "os":"Ubuntu", "osVer":"18.04", "pkg": "openssl","pkgVer": "1.1.1-1ubuntu2.1~18.04.5" } ] }' "https://YourLacework.lacework.net/api/v2/Vulnerabilities/SoftwarePackages/scan" -H "Authorization: Bearer YourAPIToken"`

Note: Calls to this operation are rate limited to 10 calls per hour, per access key. If this rate limit is exceeded, an exception is thrown. Also, note that this operation is limited to 1k of packages per payload. If you require a payload larger than 1k, you must make multiple requests. For more information about creating an API access key and token to run this operation and using this operation with organization resources, see [https://docs.lacework.com/generate-api-access-keys-and-tokens](https://docs.lacework.com/generate-api-access-keys-and-tokens).

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="osPkgInfoList"><span></span><p>required</p></td><td><div><p><span>Array of </span><span>objects</span><span> <span>non-empty </span></span><span>[ items ]</span></p><div><p>A list of supported OS types.</p></div></div></td></tr><tr><td colspan="2"><div><table><tbody><tr><td kind="field" title="os"><span></span><span>os</span></td><td></td></tr><tr><td kind="field" title="osVer"><span></span><span>osVer</span></td><td></td></tr><tr><td kind="field" title="pkg"><span></span><span>pkg</span></td><td></td></tr><tr><td kind="field" title="pkgVer"><span></span><span>pkgVer</span></td><td><div><p><span></span><span>string</span></p><div><p>The version of the package.</p></div></div></td></tr></tbody></table></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"osPkgInfoList": [`
    
    -   `{}`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/VulnerabilityExceptions)Vulnerability Exceptions

Lacework provides the ability to create exceptions for certain vulnerable resources and criteria. For example, a certain CVE for a certain package or all packages can be excepted until a set expiry time.

## [](https://docs.lacework.net/api/v2/docs#tag/VulnerabilityExceptions/paths/~1api~1v2~1VulnerabilityExceptions/post)Create Vulnerability Exceptions

Create a vulnerability exception by specifying parameters in the request body when invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/VulnerabilityExceptions`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="exceptionName"><span></span><span>exceptionName</span><p>required</p></td><td><div><p><span></span><span>string</span><span> <span>non-empty </span></span><span>(?!^ +$)^.+$</span></p><div><p>Name of the exception.</p></div></div></td></tr><tr><td kind="field" title="exceptionReason"><span></span><span>exceptionReason</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"False Positive"</span> <span>"Accepted Risk"</span> <span>"Compensating Controls"</span> <span>"Fix Pending"</span> <span>"Other"</span></p><div><p>Reason for creating an exception</p></div></div></td></tr><tr><td kind="field" title="resourceScope"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The set of resources this exception can apply to. The data varies based on the value of the <code>exceptionType</code> attribute.</p></div></div></td></tr><tr><td kind="field" title="vulnerabilityCriteria"><span></span><p>required</p></td><td><div><p><span></span><span>object</span></p><div><p>When sending a request, use this object to define the criteria of the vulnerability to be excluded. The criteria value changes depending on the type of criteria selected.</p></div></div></td></tr><tr><td kind="field" title="expiryTime"><span></span><span>expiryTime</span></td><td><div><p><span></span><span>string</span></p><div><p>The exception's expiration date and time.</p></div></div></td></tr><tr><td kind="field" title="state"><span></span><span>state</span></td><td><div><p><span></span><span>number</span></p><p><span>Value:</span> <span>1</span></p><div><p>State</p></div></div></td></tr><tr><td kind="field" title="props"><span></span><p>required</p></td><td><div><p><span></span><span>object</span></p><div><p>The vulnerability exception's properties.</p></div></div></td></tr><tr><td kind="field" title="exceptionType"><span></span><span>exceptionType</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Exception Type</p></div><p><label>Container</label></p></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"exceptionName": "string",`
    
-   `"exceptionReason": "False Positive",`
    
-   `"resourceScope": {`
    
    -   `"imageId": [],`
        
    -   `"imageTag": [],`
        
    -   `"registry": [],`
        
    -   `"repository": [],`
        
    -   `"namespace": []`
        
    
    `},`
    
-   `"vulnerabilityCriteria": {`
    
    -   `"cve": [],`
        
    -   `"package": [],`
        
    -   `"severity": [],`
        
    -   `"fixable": []`
        
    
    `},`
    
-   `"expiryTime": "string",`
    
-   `"state": 1,`
    
-   `"props": {`
    
    -   `"description": "string",`
        
    -   `"createdBy": "string",`
        
    -   `"updatedBy": "string"`
        
    
    `},`
    
-   `"exceptionType": "Container"`
    

`}`

### Response samples

-   201
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"createdTime": "2021-12-18T08:30:00Z",`
        
    -   `"exceptionGuid": "LWABC",`
        
    -   `"exceptionName": "Container Vulnerability Exception",`
        
    -   `"exceptionReason": "Accepted Risk",`
        
    -   `"exceptionType": "Container",`
        
    -   `"expiryTime": "2021-12-28T08:30:00Z",`
        
    -   `"props": {},`
        
    -   `"resourceScope": {},`
        
    -   `"state": 1,`
        
    -   `"updatedTime": "2021-12-18T08:30:00Z",`
        
    -   `"vulnerabilityCriteria": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/VulnerabilityExceptions/paths/~1api~1v2~1VulnerabilityExceptions/get)List All Vulnerability Exceptions

Get a list of all vulnerability exceptions for the account by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/VulnerabilityExceptions`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/VulnerabilityExceptions/paths/~1api~1v2~1VulnerabilityExceptions~1search/post)Search Vulnerability Exceptions

Search vulnerability exceptions by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/VulnerabilityExceptions/search`

To limit the returned result, optionally specify one or more filters in the request body. For more information about using filters, see the [Simple & Advanced Search section](https://docs.lacework.net/api/v2/docs/#tag/OVERVIEW).

In the request body, optionally specify the list of fields to return in the response by specifying the list in the `returns` array. Here are some example `body` payloads:

-   `{ "filters": [ { "field": "exceptionType", "expression": "eq", "value": "Host" } ] }`
-   `{ "filters": [ { "field": "exceptionType", "expression": "eq", "value": "Container" },`  
    `{ "field": "expiryTime", "expression": "gt", "value": "2021-01-01" } ],`  
    `"returns": [ "name", "exceptionType", "expiryTime" ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/VulnerabilityExceptions/paths/~1api~1v2~1VulnerabilityExceptions~1{exceptionGuid}/get)Vulnerability Exception Details

Get details about a vulnerability exception by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/VulnerabilityExceptions/{exceptionGuid}`

##### path Parameters

<table><tbody><tr><td kind="field" title="exceptionGuid"><span></span><span>exceptionGuid</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Vulnerability Exception ID</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"createdTime": "2021-12-18T08:30:00Z",`
        
    -   `"exceptionGuid": "LWABC",`
        
    -   `"exceptionName": "Container Vulnerability Exception",`
        
    -   `"exceptionReason": "Accepted Risk",`
        
    -   `"exceptionType": "Container",`
        
    -   `"expiryTime": "2021-12-28T08:30:00Z",`
        
    -   `"props": {},`
        
    -   `"resourceScope": {},`
        
    -   `"state": 1,`
        
    -   `"updatedTime": "2021-12-18T08:30:00Z",`
        
    -   `"vulnerabilityCriteria": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/VulnerabilityExceptions/paths/~1api~1v2~1VulnerabilityExceptions~1{exceptionGuid}/patch)Update Vulnerability Exceptions

Update a vulnerability exception by specifying parameters in the request body when invoking the following endpoint:

> `PATCH https://YourLacework.lacework.net/api/v2/VulnerabilityExceptions/{exceptionGuid}`

In the request body, only specify the parameters that you want to update, for example, `{ "exceptionReason" : "Other" }`.

##### path Parameters

<table><tbody><tr><td kind="field" title="exceptionGuid"><span></span><span>exceptionGuid</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Vulnerability Exception ID</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="exceptionName"><span></span><span>exceptionName</span></td><td><div><p><span></span><span>string</span><span> <span>non-empty </span></span><span>(?!^ +$)^.+$</span></p><div><p>Name of the exception.</p></div></div></td></tr><tr><td kind="field" title="exceptionReason"><span></span><span>exceptionReason</span></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"False Positive"</span> <span>"Accepted Risk"</span> <span>"Compensating Controls"</span> <span>"Fix Pending"</span> <span>"Other"</span></p><div><p>Reason for creating an exception</p></div></div></td></tr><tr><td kind="field" title="resourceScope"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The set of resources this exception can apply to. The data varies based on the value of the <code>exceptionType</code> attribute.</p></div></div></td></tr><tr><td kind="field" title="vulnerabilityCriteria"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>When sending a request, use this object to define the criteria of the vulnerability to be excluded. The criteria value changes depending on the type of criteria selected.</p></div></div></td></tr><tr><td kind="field" title="expiryTime"><span></span><span>expiryTime</span></td><td><div><p><span></span><span>string</span></p><div><p>The exception's expiration date and time.</p></div></div></td></tr><tr><td kind="field" title="state"><span></span><span>state</span></td><td><div><p><span></span><span>number</span></p><p><span>Value:</span> <span>1</span></p><div><p>State</p></div></div></td></tr><tr><td kind="field" title="props"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The vulnerability exception's properties.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"exceptionName": "string",`
    
-   `"exceptionReason": "False Positive",`
    
-   `"resourceScope": {`
    
    -   `"imageId": [],`
        
    -   `"imageTag": [],`
        
    -   `"registry": [],`
        
    -   `"repository": [],`
        
    -   `"namespace": []`
        
    
    `},`
    
-   `"vulnerabilityCriteria": {`
    
    -   `"cve": [],`
        
    -   `"package": [],`
        
    -   `"severity": [],`
        
    -   `"fixable": []`
        
    
    `},`
    
-   `"expiryTime": "string",`
    
-   `"state": 1,`
    
-   `"props": {`
    
    -   `"description": "string",`
        
    -   `"createdBy": "string",`
        
    -   `"updatedBy": "string"`
        
    
    `},`
    
-   `"exceptionType": "Container"`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"createdTime": "2021-12-18T08:30:00Z",`
        
    -   `"exceptionGuid": "LWABC",`
        
    -   `"exceptionName": "Container Vulnerability Exception",`
        
    -   `"exceptionReason": "Accepted Risk",`
        
    -   `"exceptionType": "Container",`
        
    -   `"expiryTime": "2021-12-28T08:30:00Z",`
        
    -   `"props": {},`
        
    -   `"resourceScope": {},`
        
    -   `"state": 1,`
        
    -   `"updatedTime": "2021-12-18T08:30:00Z",`
        
    -   `"vulnerabilityCriteria": {}`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/VulnerabilityExceptions/paths/~1api~1v2~1VulnerabilityExceptions~1{exceptionGuid}/delete)Delete Vulnerability Exceptions

Delete a vulnerability exception by invoking the following endpoint:

> `DELETE https://YourLacework.lacework.net/api/v2/VulnerabilityExceptions/{exceptionGuid}`

##### path Parameters

<table><tbody><tr><td kind="field" title="exceptionGuid"><span></span><span>exceptionGuid</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Vulnerability Exception ID</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/VulnerabilityPolicies)Vulnerability Policies

Lacework provides the ability to create container vulnerability policies to assess your container images at build and/or runtime based on your own unique requirements. For example, a policy can be created for any critical vulnerability with a fix available or a policy to target a specific CVE.

## [](https://docs.lacework.net/api/v2/docs#tag/VulnerabilityPolicies/paths/~1api~1v2~1VulnerabilityPolicies/post)Create Vulnerability Policies

Create a vulnerability policy by specifying parameters in the request body when invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/VulnerabilityPolicies`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="policyType"><span></span><span>policyType</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>The policy type such as <code>DockerFile</code>, <code>DockerConfig</code>, or <code>Image</code>.</p></div><p><label>DockerFile</label></p></div></td></tr><tr><td kind="field" title="policyName"><span></span><span>policyName</span><p>required</p></td><td><div><p><span></span><span>string</span><span> <span>non-empty </span></span><span>(?!^ +$)^.+$</span></p><div><p>Name of the policy.</p></div></div></td></tr><tr><td kind="field" title="policyEvalType"><span></span><span>policyEvalType</span></td><td><div><p><span></span><span>string</span></p><p><span>Default: </span><span>"local"</span></p><p><span>Value:</span> <span>"local"</span></p><div><p>The evaluation type to use for the policy. The default value is <code>local</code>.</p></div></div></td></tr><tr><td kind="field" title="severity"><span></span><span>severity</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"Critical"</span> <span>"High"</span> <span>"Medium"</span> <span>"Low"</span> <span>"Info"</span></p><div><p>The severity level of the policy; Info, Low, Medium, High, or Critical.</p></div></div></td></tr><tr><td kind="field" title="failOnViolation"><span></span><span>failOnViolation</span></td><td><div><p><span></span><span>number</span></p><p><span>Default: </span><span>0</span></p><p><span>Enum:</span> <span>0</span> <span>1</span></p><div><p>When sending a request, use this attribute to define what action is taken when a policy failure occurs. Set to <code>1</code> to permit container image deployment to continue even when the policy fails. Set to <code>0</code> to block container image deployment when the policy fails.</p></div></div></td></tr><tr><td kind="field" title="alertOnViolation"><span></span><span>alertOnViolation</span></td><td><div><p><span></span><span>number</span></p><p><span>Default: </span><span>0</span></p><p><span>Enum:</span> <span>0</span> <span>1</span></p><div><p>When sending a request, set to <code>1</code> if you want to send alerts to an alert profile when a violation is detected. Set to <code>0</code> if you want to mute alerts when a violation is detected.</p></div></div></td></tr><tr><td kind="field" title="state"><span></span><span>state</span><p>required</p></td><td><div><p><span></span><span>number</span></p><p><span>Enum:</span> <span>0</span> <span>1</span></p><div><p>When sending a request, set to <code>1</code> to enable the policy. Set to <code>0</code> to disable the policy.</p></div></div></td></tr><tr><td kind="field" title="filter"><span></span><p>required</p></td><td><div><p><span></span><span>object</span><span> (VulnerabilityPolicies_DockerFile)</span></p></div></td></tr><tr><td kind="field" title="props"><span></span><p>required</p></td><td><div><p><span></span><span>object</span></p><div><p>The vulnerability policy's properties.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"policyType": "DockerFile",`
    
-   `"policyName": "string",`
    
-   `"policyEvalType": "local",`
    
-   `"severity": "Critical",`
    
-   `"failOnViolation": 0,`
    
-   `"alertOnViolation": 0,`
    
-   `"state": 0,`
    
-   `"filter": {`
    
    -   `"rule": {},`
        
    -   `"exception": {}`
        
    
    `},`
    
-   `"props": {`
    
    -   `"description": "string",`
        
    -   `"createdBy": "string",`
        
    -   `"updatedBy": "string"`
        
    
    `}`
    

`}`

### Response samples

-   201
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"policyGuid": "LWABC",`
        
    -   `"policyName": "DockerFile Vulnerability Policy",`
        
    -   `"policyType": "DockerFile",`
        
    -   `"policyEvalType": "local",`
        
    -   `"severity": "Critical",`
        
    -   `"failOnViolation": 0,`
        
    -   `"alertOnViolation": 0,`
        
    -   `"filter": {},`
        
    -   `"state": 1,`
        
    -   `"isDefault": 0,`
        
    -   `"props": {},`
        
    -   `"createdTime": "2022-03-04T22:32:14.685Z",`
        
    -   `"updatedTime": "2022-03-04T22:32:14.685Z"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/VulnerabilityPolicies/paths/~1api~1v2~1VulnerabilityPolicies/get)List All Vulnerability Policies

Get a list of all vulnerability policies for the account by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/VulnerabilityPolicies`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/VulnerabilityPolicies/paths/~1api~1v2~1VulnerabilityPolicies~1search/post)Search Vulnerability Policies

Search vulnerability policies by invoking the following endpoint:

> `POST https://YourLacework.lacework.net/api/v2/VulnerabilityPolicies/search`

To limit the returned result, optionally specify one or more filters in the request body. For more information about using filters, see the [Simple & Advanced Search section](https://docs.lacework.net/api/v2/docs/#tag/OVERVIEW).

In the request body, optionally specify the list of fields to return in the response by specifying the list in the `returns` array. Here are some example `body` payloads:

-   `{ "filters": [ { "field": "policyType", "expression": "eq", "value": "DockerFile" } ] }`
-   `{ "filters": [ { "field": "PolicyType", "expression": "eq", "value": "CVE" },`  
    `{ "field": "createdTime", "expression": "gt", "value": "2021-01-01" } ],`  
    `"returns": [ "name", "policyType", "createdTime" ] }`

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="filters"><span></span></td><td><div><p><span>Array of </span><span>objects</span><span>[ items ]</span></p><div><p>One or more condition statements you can use to refine the data returned by the request. Only records that satisfy filtering conditions are returned. If there are multiple conditions, a record must satisfy all conditions for a match.</p></div></div></td></tr><tr><td kind="field" title="returns"><span></span><span>returns</span></td><td><div><p><span>Array of </span><span>strings</span></p><div><p>Use this attribute to specify which top-level fields of the response schema you want to receive.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"filters": [`
    
    -   `{}`
        
    
    `],`
    
-   `"returns": [`
    
    -   `"string"`
        
    
    `]`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": [`
    
    -   `{},`
        
    -   `{}`
        
    
    `]`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/VulnerabilityPolicies/paths/~1api~1v2~1VulnerabilityPolicies~1{policyGuid}/get)Vulnerability Policy Details

Get details about a vulnerability policy by invoking the following endpoint:

> `GET https://YourLacework.lacework.net/api/v2/VulnerabilityPolicies/{policyGuid}`

##### path Parameters

<table><tbody><tr><td kind="field" title="policyGuid"><span></span><span>policyGuid</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Vulnerability Policies ID</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"policyGuid": "LWABC",`
        
    -   `"policyName": "DockerFile Vulnerability Policy",`
        
    -   `"policyType": "DockerFile",`
        
    -   `"policyEvalType": "local",`
        
    -   `"severity": "Critical",`
        
    -   `"failOnViolation": 0,`
        
    -   `"alertOnViolation": 0,`
        
    -   `"filter": {},`
        
    -   `"state": 1,`
        
    -   `"isDefault": 0,`
        
    -   `"props": {},`
        
    -   `"createdTime": "2022-03-04T22:32:14.685Z",`
        
    -   `"updatedTime": "2022-03-04T22:32:14.685Z"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/VulnerabilityPolicies/paths/~1api~1v2~1VulnerabilityPolicies~1{policyGuid}/patch)Update Vulnerability Policies

Update a vulnerability policy by specifying parameters in the request body when invoking the following endpoint:

> `PATCH https://YourLacework.lacework.net/api/v2/VulnerabilityPolicies/{policyGuid}`

In the request body, only specify the parameters that you want to update, for example, `{ "severity" : "High" }`.

##### path Parameters

<table><tbody><tr><td kind="field" title="policyGuid"><span></span><span>policyGuid</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Vulnerability Policies ID</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

<table><tbody><tr><td kind="field" title="policyType"><span></span><span>policyType</span></td><td><div><p><span></span><span>string</span></p><div><p>The policy type such as <code>DockerFile</code>, <code>DockerConfig</code>, or <code>Image</code>.</p></div><p><label>DockerFile</label></p></div></td></tr><tr><td kind="field" title="policyName"><span></span><span>policyName</span></td><td><div><p><span></span><span>string</span><span> <span>non-empty </span></span><span>(?!^ +$)^.+$</span></p><div><p>Name of the policy.</p></div></div></td></tr><tr><td kind="field" title="policyEvalType"><span></span><span>policyEvalType</span></td><td><div><p><span></span><span>string</span></p><p><span>Default: </span><span>"local"</span></p><p><span>Value:</span> <span>"local"</span></p><div><p>The evaluation type to use for the policy. The default value is <code>local</code>.</p></div></div></td></tr><tr><td kind="field" title="severity"><span></span><span>severity</span></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"Critical"</span> <span>"High"</span> <span>"Medium"</span> <span>"Low"</span> <span>"Info"</span></p><div><p>The severity level of the policy; Info, Low, Medium, High, or Critical.</p></div></div></td></tr><tr><td kind="field" title="failOnViolation"><span></span><span>failOnViolation</span></td><td><div><p><span></span><span>number</span></p><p><span>Default: </span><span>0</span></p><p><span>Enum:</span> <span>0</span> <span>1</span></p><div><p>When sending a request, use this attribute to define what action is taken when a policy failure occurs. Set to <code>1</code> to permit container image deployment to continue even when the policy fails. Set to <code>0</code> to block container image deployment when the policy fails.</p></div></div></td></tr><tr><td kind="field" title="alertOnViolation"><span></span><span>alertOnViolation</span></td><td><div><p><span></span><span>number</span></p><p><span>Default: </span><span>0</span></p><p><span>Enum:</span> <span>0</span> <span>1</span></p><div><p>When sending a request, set to <code>1</code> if you want to send alerts to an alert profile when a violation is detected. Set to <code>0</code> if you want to mute alerts when a violation is detected.</p></div></div></td></tr><tr><td kind="field" title="state"><span></span><span>state</span></td><td><div><p><span></span><span>number</span></p><p><span>Enum:</span> <span>0</span> <span>1</span></p><div><p>When sending a request, set to <code>1</code> to enable the policy. Set to <code>0</code> to disable the policy.</p></div></div></td></tr><tr><td kind="field" title="filter"><span></span></td><td><div><p><span></span><span>object</span><span> (VulnerabilityPolicies_DockerFile)</span></p></div></td></tr><tr><td kind="field" title="props"><span></span></td><td><div><p><span></span><span>object</span></p><div><p>The vulnerability policy's properties.</p></div></div></td></tr></tbody></table>

### Responses

### Request samples

-   Payload

Content type

application/json

`{`

-   `"policyType": "DockerFile",`
    
-   `"policyName": "string",`
    
-   `"policyEvalType": "local",`
    
-   `"severity": "Critical",`
    
-   `"failOnViolation": 0,`
    
-   `"alertOnViolation": 0,`
    
-   `"state": 0,`
    
-   `"filter": {`
    
    -   `"rule": {},`
        
    -   `"exception": {}`
        
    
    `},`
    
-   `"props": {`
    
    -   `"description": "string",`
        
    -   `"createdBy": "string",`
        
    -   `"updatedBy": "string"`
        
    
    `}`
    

`}`

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

`{`

-   `"data": {`
    
    -   `"policyGuid": "LWABC",`
        
    -   `"policyName": "DockerFile Vulnerability Policy",`
        
    -   `"policyType": "DockerFile",`
        
    -   `"policyEvalType": "local",`
        
    -   `"severity": "Critical",`
        
    -   `"failOnViolation": 0,`
        
    -   `"alertOnViolation": 0,`
        
    -   `"filter": {},`
        
    -   `"state": 1,`
        
    -   `"isDefault": 0,`
        
    -   `"props": {},`
        
    -   `"createdTime": "2022-03-04T22:32:14.685Z",`
        
    -   `"updatedTime": "2022-03-04T22:32:14.685Z"`
        
    
    `}`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/VulnerabilityPolicies/paths/~1api~1v2~1VulnerabilityPolicies~1{policyGuid}/delete)Delete Vulnerability Policies

Delete a vulnerability policy by invoking the following endpoint:

> `DELETE https://YourLacework.lacework.net/api/v2/VulnerabilityPolicies/{policyGuid}`

##### path Parameters

<table><tbody><tr><td kind="field" title="policyGuid"><span></span><span>policyGuid</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Vulnerability Policies ID</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Access Token. For example, "Bearer {YourAPIToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   4XX
-   5XX

Content type

application/json

`{`

-   `"message": "Invalid ..."`
    

`}`

## [](https://docs.lacework.net/api/v2/docs#tag/Webhooks)Webhooks

Send notifications from your integration using a server token or signature.

## [](https://docs.lacework.net/api/v2/docs#tag/Webhooks/paths/~1api~1v2~1Webhooks~1ServerTokens~1{type}/post)Webhooks by Server Tokens

Send notifications from your integration using a server token.

You must specify the integration's server token that was generated by the Lacework Console when you created the integration that subscribes to notifications.

For more information, see [https://docs.lacework.com/integrate-a-docker-v2-registry](https://docs.lacework.com/integrate-a-docker-v2-registry).

For more information about creating an API access key and token to run this operation and using this operation with organization resources, see [https://docs.lacework.com/generate-api-access-keys-and-tokens](https://docs.lacework.com/generate-api-access-keys-and-tokens).

Usage Example:

> `curl -H 'Content-Type: {content-type}' -X POST -d '{notification-body}' "https://YourLacework.lacework.net/api/v2/Webhooks/ServerTokens/DockerV2" -H "Authorization: Bearer YourServerToken"`

Note: If a container registry integration is unsubscribed from notifications and then subscribed again, the same server token is used.

##### path Parameters

<table><tbody><tr><td kind="field" title="type"><span></span><span>type</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Enum:</span> <span>"AzureCR"</span> <span>"DockerV2"</span> <span>"JFrog"</span></p><div><p>The integration type such as <code>AzureCR</code>, <code>DockerV2</code>, <code>JFrog</code>.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="Authorization"><span></span><span>Authorization</span><p>required</p></td><td><div><p><span></span><span>string</span></p><div><p>Bearer Server Token. For example, "Bearer {YourServerToken}"</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

##### Request Body schema: application/json

Integration specific notification body

### Responses

### Request samples

-   Payload

Content type

application/json

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json

## [](https://docs.lacework.net/api/v2/docs#tag/Webhooks/paths/~1api~1v2~1Webhooks~1Signatures~1{type}/post)Webhooks by Signature

Send notifications from your integration using a signature.

You must specify the integration's server token that was generated by the Lacework Console when you created the integration that subscribes to notifications. For more information, see [https://docs.lacework.com/integrate-github-container-registry](https://docs.lacework.com/integrate-github-container-registry).

Usage Example:

> `curl -H 'Content-Type: {content-type}' -X POST "https://YourLacework.lacework.net/api/v2/Webhooks/Signatures/GithubCR" -H "x-hub-signature-256: sha256=sha256 payload hash with YourServerToken as secret"`

Note: For a container registry integration, use the same server token if you want to re-subscribe to notifications after unsubscribing.

##### path Parameters

<table><tbody><tr><td kind="field" title="type"><span></span><span>type</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Value:</span> <span>"GithubCR"</span></p><div><p>The integration type such as <code>GithubCR</code>.</p></div></div></td></tr></tbody></table>

##### header Parameters

<table><tbody><tr><td kind="field" title="x-hub-signature-256"><span></span><span>x-hub-signature-256</span><p>required</p></td><td><div><p><span></span><span>string</span></p><p><span>Example: </span><span>x-hub-signature-256: sha256=123...</span></p><div><p>When your secret token is set, Lacework uses it to create a hash signature with each payload. This hash signature is included with the headers of each request as <code>X-Hub-Signature-256</code>.</p></div></div></td></tr><tr><td kind="field" title="Content-Type"><span></span><span>Content-Type</span><p>required</p></td><td></td></tr></tbody></table>

### Responses

### Response samples

-   200
-   4XX
-   5XX

Content type

application/json