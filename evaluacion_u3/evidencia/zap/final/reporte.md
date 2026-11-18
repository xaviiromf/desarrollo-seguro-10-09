# ZAP final - CRUD Supermercado (laboratorio Docker)

ZAP by [Checkmarx](https://checkmarx.com/).


## Summary of Alerts

| Risk Level | Number of Alerts |
| --- | --- |
| High | 0 |
| Medium | 0 |
| Low | 0 |
| Informational | 3 |




## Insights

| Level | Reason | Site | Description | Statistic |
| --- | --- | --- | --- | --- |
| Low | Warning |  | ZAP warnings logged - see the zap.log file for details | 110    |
| Info | Informational | http://127.0.0.1:8000 | Percentage of responses with status code 2xx | 69 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of responses with status code 3xx | 30 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with content type text/css | 7 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with content type text/csv | 3 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with content type text/html | 82 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with content type text/javascript | 7 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with method GET | 60 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with method POST | 39 % |
| Info | Informational | http://127.0.0.1:8000 | Count of total endpoints | 28    |
| Info | Informational | http://127.0.0.1:8000 | Percentage of slow responses | 2 % |







## Alerts

| Name | Risk Level | Number of Instances |
| --- | --- | --- |
| Authentication Request Identified | Informational | 1 |
| Session Management Response Identified | Informational | 22 |
| User Controllable HTML Element Attribute (Potential XSS) | Informational | 2 |




## Alert Detail



### [ Authentication Request Identified ](https://www.zaproxy.org/docs/alerts/10111/)



##### Informational (High)

### Description

The given request has been identified as an authentication request. The 'Other Info' field contains a set of key=value lines which identify any relevant fields. If the request is in a context which has an Authentication Method set to "Auto-Detect" then this rule will change the authentication to match the request identified.

* URL: http://127.0.0.1:8000/login/
  * Node Name: `http://127.0.0.1:8000/login/ ()(csrfmiddlewaretoken,password,username)`
  * Method: `POST`
  * Parameter: `username`
  * Attack: ``
  * Evidence: `password`
  * Other Info: `userParam=username
userValue=qa_ana
passwordParam=password
referer=http://127.0.0.1:8000/login/`


Instances: 1

### Solution

This is an informational alert rather than a vulnerability and so there is nothing to fix.

### Reference


* [ https://www.zaproxy.org/docs/desktop/addons/authentication-helper/auth-req-id/ ](https://www.zaproxy.org/docs/desktop/addons/authentication-helper/auth-req-id/)



#### Source ID: 3

### [ Session Management Response Identified ](https://www.zaproxy.org/docs/alerts/10112/)



##### Informational (Medium)

### Description

The given response has been identified as containing a session management token. The 'Other Info' field contains a set of header tokens that can be used in the Header Based Session Management Method. If the request is in a context which has a Session Management Method set to "Auto-Detect" then this rule will change the session management to use the tokens identified.

* URL: http://127.0.0.1:8000/
  * Node Name: `http://127.0.0.1:8000/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/%3Fsort=newest&q=Lista
  * Node Name: `http://127.0.0.1:8000/ (q,sort)`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/items/13/edit/
  * Node Name: `http://127.0.0.1:8000/items/13/edit/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/lists/13/
  * Node Name: `http://127.0.0.1:8000/lists/13/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/lists/13/%3Fstatus=pending
  * Node Name: `http://127.0.0.1:8000/lists/13/ (status)`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/lists/13/delete/
  * Node Name: `http://127.0.0.1:8000/lists/13/delete/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/lists/13/edit/
  * Node Name: `http://127.0.0.1:8000/lists/13/edit/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/lists/14/
  * Node Name: `http://127.0.0.1:8000/lists/14/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/lists/new/
  * Node Name: `http://127.0.0.1:8000/lists/new/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/login/
  * Node Name: `http://127.0.0.1:8000/login/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/login/%3Fnext=/lists/13/
  * Node Name: `http://127.0.0.1:8000/login/ (next)`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/register/
  * Node Name: `http://127.0.0.1:8000/register/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/items/13/edit/
  * Node Name: `http://127.0.0.1:8000/items/13/edit/ ()(brand,category,csrfmiddlewaretoken,name,quantity,unit_price)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/lists/13/bulk-toggle/
  * Node Name: `http://127.0.0.1:8000/lists/13/bulk-toggle/ ()(action,csrfmiddlewaretoken)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/lists/13/clear-purchased/
  * Node Name: `http://127.0.0.1:8000/lists/13/clear-purchased/ ()(csrfmiddlewaretoken)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/lists/13/delete/
  * Node Name: `http://127.0.0.1:8000/lists/13/delete/ ()(csrfmiddlewaretoken)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/lists/13/duplicate/
  * Node Name: `http://127.0.0.1:8000/lists/13/duplicate/ ()(csrfmiddlewaretoken)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/lists/13/edit/
  * Node Name: `http://127.0.0.1:8000/lists/13/edit/ ()(budget_limit,csrfmiddlewaretoken,description,name,priority)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/lists/13/items/add/
  * Node Name: `http://127.0.0.1:8000/lists/13/items/add/ ()(brand,category,csrfmiddlewaretoken,name,quantity,unit_price)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/lists/new/
  * Node Name: `http://127.0.0.1:8000/lists/new/ ()(budget_limit,csrfmiddlewaretoken,description,name,priority)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/login/
  * Node Name: `http://127.0.0.1:8000/login/ ()(csrfmiddlewaretoken,password,username)`
  * Method: `POST`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken
cookie:messages
cookie:sessionid`
* URL: http://127.0.0.1:8000/logout/
  * Node Name: `http://127.0.0.1:8000/logout/ ()(csrfmiddlewaretoken)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`


Instances: 22

### Solution

This is an informational alert rather than a vulnerability and so there is nothing to fix.

### Reference


* [ https://www.zaproxy.org/docs/desktop/addons/authentication-helper/session-mgmt-id/ ](https://www.zaproxy.org/docs/desktop/addons/authentication-helper/session-mgmt-id/)



#### Source ID: 3

### [ User Controllable HTML Element Attribute (Potential XSS) ](https://www.zaproxy.org/docs/alerts/10031/)



##### Informational (Low)

### Description

This check looks at user-supplied input in query string parameters and POST data to identify where certain HTML attribute values might be controlled. This provides hot-spot detection for XSS (cross-site scripting) that will require further review by a security analyst to determine exploitability.

* URL: http://127.0.0.1:8000/%3Fsort=newest&q=Lista
  * Node Name: `http://127.0.0.1:8000/ (q,sort)`
  * Method: `GET`
  * Parameter: `q`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://127.0.0.1:8000/?sort=newest&q=Lista

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
q=Lista

The user-controlled value was:
lista`
* URL: http://127.0.0.1:8000/%3Fsort=newest&q=Lista
  * Node Name: `http://127.0.0.1:8000/ (q,sort)`
  * Method: `GET`
  * Parameter: `sort`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://127.0.0.1:8000/?sort=newest&q=Lista

appears to include user input in:
a(n) [option] tag [value] attribute

The user input found was:
sort=newest

The user-controlled value was:
newest`


Instances: 2

### Solution

Validate all input and sanitize output it before writing to any HTML attributes.

### Reference


* [ https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html ](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)


#### CWE Id: [ 20 ](https://cwe.mitre.org/data/definitions/20.html)


#### WASC Id: 20

#### Source ID: 3


