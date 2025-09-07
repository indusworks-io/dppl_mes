My app is a frappe framework app that has a custom frontend app built on vue js...
The app gets compiled and
- frontend.html is placed in dppl_mes/dppl_mes/www
- assets are placed in dppl_mes/dppl_mes/public/frontend

The app is pushed to production using docker using dppl_mes/frontend/src/development/pwd.yml


This is the starting url for the frontend vue js app is:
https://production.soundseal.in/frontend/

On refresh the url changes to:
https://production.soundseal.in:8080/frontend

in network tab of the browser I see this:
Request URL
https://production.soundseal.in/frontend/
Request Method
GET
Status Code
301 Moved Permanently
Remote Address
103.225.225.155:443
Referrer Policy
strict-origin-when-cross-origin
Request URL
http://production.soundseal.in:8080/frontend
Request Method
GET
Status Code
307 Internal Redirect
Referrer Policy
strict-origin-when-cross-origin
Request URL
https://production.soundseal.in:8080/frontend
Referrer Policy
strict-origin-when-cross-origin


debug this issue, think hard... 