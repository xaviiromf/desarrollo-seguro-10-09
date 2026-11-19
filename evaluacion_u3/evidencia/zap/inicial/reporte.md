# ZAP inicial - CRUD Supermercado (laboratorio Docker)

ZAP by [Checkmarx](https://checkmarx.com/).


## Summary of Alerts

| Risk Level | Number of Alerts |
| --- | --- |
| High | 0 |
| Medium | 2 |
| Low | 1 |
| Informational | 3 |




## Insights

| Level | Reason | Site | Description | Statistic |
| --- | --- | --- | --- | --- |
| Low | Warning |  | ZAP warnings logged - see the zap.log file for details | 110    |
| Info | Informational | http://127.0.0.1:8000 | Percentage of responses with status code 2xx | 68 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of responses with status code 3xx | 31 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with content type text/css | 3 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with content type text/csv | 3 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with content type text/html | 85 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with content type text/javascript | 7 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with method GET | 59 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with method POST | 40 % |
| Info | Informational | http://127.0.0.1:8000 | Count of total endpoints | 27    |
| Info | Informational | http://127.0.0.1:8000 | Percentage of slow responses | 2 % |







## Alerts

| Name | Risk Level | Number of Instances |
| --- | --- | --- |
| Content Security Policy (CSP) Header Not Set | Medium | Systemic |
| Cross-Domain Misconfiguration | Medium | 2 |
| Cookie No HttpOnly Flag | Low | Systemic |
| Authentication Request Identified | Informational | 1 |
| Session Management Response Identified | Informational | 22 |
| User Controllable HTML Element Attribute (Potential XSS) | Informational | 2 |




## Alert Detail



### [ Content Security Policy (CSP) Header Not Set ](https://www.zaproxy.org/docs/alerts/10038/)



##### Medium (High)

### Description

Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks, including Cross Site Scripting (XSS) and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.

* URL: http://127.0.0.1:8000/
  * Node Name: `http://127.0.0.1:8000/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: http://127.0.0.1:8000/%3Fsort=newest&q=Lista
  * Node Name: `http://127.0.0.1:8000/ (q,sort)`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: http://127.0.0.1:8000/lists/3/
  * Node Name: `http://127.0.0.1:8000/lists/3/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: http://127.0.0.1:8000/lists/new/
  * Node Name: `http://127.0.0.1:8000/lists/new/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: http://127.0.0.1:8000/login/
  * Node Name: `http://127.0.0.1:8000/login/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``

Instances: Systemic


### Solution

Ensure that your web server, application server, load balancer, etc. is configured to set the Content-Security-Policy header.

### Reference


* [ https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP ](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP)
* [ https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html ](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
* [ https://www.w3.org/TR/CSP/ ](https://www.w3.org/TR/CSP/)
* [ https://w3c.github.io/webappsec-csp/ ](https://w3c.github.io/webappsec-csp/)
* [ https://web.dev/articles/csp ](https://web.dev/articles/csp)
* [ https://caniuse.com/#feat=contentsecuritypolicy ](https://caniuse.com/#feat=contentsecuritypolicy)
* [ https://content-security-policy.com/ ](https://content-security-policy.com/)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 15

#### Source ID: 3

### [ Cross-Domain Misconfiguration ](https://www.zaproxy.org/docs/alerts/10098/)



##### Medium (Medium)

### Description

Web browser data loading may be possible, due to a Cross Origin Resource Sharing (CORS) misconfiguration on the web server.

* URL: http://127.0.0.1:8000/static/css/dist/styles.css
  * Node Name: `http://127.0.0.1:8000/static/css/dist/styles.css`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Access-Control-Allow-Origin: *`
  * Other Info: `The CORS misconfiguration on the web server permits cross-domain read requests from arbitrary third party domains, using unauthenticated APIs on this domain. Web browser implementations do not permit arbitrary third parties to read the response from authenticated APIs, however. This reduces the risk somewhat. This misconfiguration could be used by an attacker to access data that is available in an unauthenticated manner, but which uses some other form of security, such as IP address white-listing.`
* URL: http://127.0.0.1:8000/static/shopping/js/calculator.js
  * Node Name: `http://127.0.0.1:8000/static/shopping/js/calculator.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Access-Control-Allow-Origin: *`
  * Other Info: `The CORS misconfiguration on the web server permits cross-domain read requests from arbitrary third party domains, using unauthenticated APIs on this domain. Web browser implementations do not permit arbitrary third parties to read the response from authenticated APIs, however. This reduces the risk somewhat. This misconfiguration could be used by an attacker to access data that is available in an unauthenticated manner, but which uses some other form of security, such as IP address white-listing.`


Instances: 2

### Solution

Ensure that sensitive data is not available in an unauthenticated manner (using IP address white-listing, for instance).
Configure the "Access-Control-Allow-Origin" HTTP header to a more restrictive set of domains, or remove all CORS headers entirely, to allow the web browser to enforce the Same Origin Policy (SOP) in a more restrictive manner.

### Reference


* [ https://vulncat.fortify.com/en/detail?category=HTML5&subcategory=Overly%20Permissive%20CORS%20Policy ](https://vulncat.fortify.com/en/detail?category=HTML5&subcategory=Overly%20Permissive%20CORS%20Policy)


#### CWE Id: [ 264 ](https://cwe.mitre.org/data/definitions/264.html)


#### WASC Id: 14

#### Source ID: 3

### [ Cookie No HttpOnly Flag ](https://www.zaproxy.org/docs/alerts/10010/)



##### Low (Medium)

### Description

A cookie has been set without the HttpOnly flag, which means that the cookie can be accessed by JavaScript. If a malicious script can be run on this page then the cookie will be accessible and can be transmitted to another site. If this is a session cookie then session hijacking may be possible.

* URL: http://127.0.0.1:8000/
  * Node Name: `http://127.0.0.1:8000/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `Set-Cookie: csrftoken`
  * Other Info: ``
* URL: http://127.0.0.1:8000/%3Fsort=newest&q=Lista
  * Node Name: `http://127.0.0.1:8000/ (q,sort)`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `Set-Cookie: csrftoken`
  * Other Info: ``
* URL: http://127.0.0.1:8000/lists/new/
  * Node Name: `http://127.0.0.1:8000/lists/new/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `Set-Cookie: csrftoken`
  * Other Info: ``
* URL: http://127.0.0.1:8000/login/
  * Node Name: `http://127.0.0.1:8000/login/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `Set-Cookie: csrftoken`
  * Other Info: ``
* URL: http://127.0.0.1:8000/login/
  * Node Name: `http://127.0.0.1:8000/login/ ()(csrfmiddlewaretoken,password,username)`
  * Method: `POST`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `Set-Cookie: csrftoken`
  * Other Info: ``

Instances: Systemic


### Solution

Ensure that the HttpOnly flag is set for all cookies.

### Reference


* [ https://owasp.org/www-community/HttpOnly ](https://owasp.org/www-community/HttpOnly)


#### CWE Id: [ 1004 ](https://cwe.mitre.org/data/definitions/1004.html)


#### WASC Id: 13

#### Source ID: 3

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
* URL: http://127.0.0.1:8000/items/3/edit/
  * Node Name: `http://127.0.0.1:8000/items/3/edit/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/lists/3/
  * Node Name: `http://127.0.0.1:8000/lists/3/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/lists/3/%3Fstatus=pending
  * Node Name: `http://127.0.0.1:8000/lists/3/ (status)`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/lists/3/delete/
  * Node Name: `http://127.0.0.1:8000/lists/3/delete/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/lists/3/edit/
  * Node Name: `http://127.0.0.1:8000/lists/3/edit/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/lists/4/
  * Node Name: `http://127.0.0.1:8000/lists/4/`
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
* URL: http://127.0.0.1:8000/login/%3Fnext=/lists/3/
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
* URL: http://127.0.0.1:8000/items/3/edit/
  * Node Name: `http://127.0.0.1:8000/items/3/edit/ ()(brand,category,csrfmiddlewaretoken,name,quantity,unit_price)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/lists/3/bulk-toggle/
  * Node Name: `http://127.0.0.1:8000/lists/3/bulk-toggle/ ()(action,csrfmiddlewaretoken)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/lists/3/clear-purchased/
  * Node Name: `http://127.0.0.1:8000/lists/3/clear-purchased/ ()(csrfmiddlewaretoken)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/lists/3/delete/
  * Node Name: `http://127.0.0.1:8000/lists/3/delete/ ()(csrfmiddlewaretoken)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/lists/3/duplicate/
  * Node Name: `http://127.0.0.1:8000/lists/3/duplicate/ ()(csrfmiddlewaretoken)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/lists/3/edit/
  * Node Name: `http://127.0.0.1:8000/lists/3/edit/ ()(budget_limit,csrfmiddlewaretoken,description,name,priority)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/lists/3/items/add/
  * Node Name: `http://127.0.0.1:8000/lists/3/items/add/ ()(brand,category,csrfmiddlewaretoken,name,quantity,unit_price)`
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


