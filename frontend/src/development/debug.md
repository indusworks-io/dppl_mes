### Browser Console Output:
console.log('window.location:', window.location)
console.log('window.location.hostname:', window.location.hostname)
console.log('window.location.port:', window.location.port)
console.log('window.location.protocol:', window.location.protocol)
console.log('window.site_name:', window.site_name)
VM361:1 window.location: Location {ancestorOrigins: DOMStringList, href: 'http://frontend.localhost:8080/frontend/', origin: 'http://frontend.localhost:8080', protocol: 'http:', host: 'frontend.localhost:8080', …}
VM361:2 window.location.hostname: frontend.localhost
VM361:3 window.location.port: 8080
VM361:4 window.location.protocol: http:
VM361:5 window.site_name: undefined
undefined


### Docker Terminal Output 
docker ps
CONTAINER ID   IMAGE                          COMMAND                  CREATED          STATUS                    PORTS                                         NAMES
306d05855180   navneetindusworks/dppl:3.1.3   "nginx-entrypoint.sh"    20 minutes ago   Up 20 minutes             0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp   dppl-frontend-1
dfac76a96f44   redis:6.2-alpine               "docker-entrypoint.s…"   20 minutes ago   Up 20 minutes             6379/tcp                                      dppl-redis-cache-1
a15489687a08   navneetindusworks/dppl:3.1.3   "node /home/frappe/f…"   20 minutes ago   Up 20 minutes                                                           dppl-websocket-1
7ac10d4694b6   navneetindusworks/dppl:3.1.3   "/home/frappe/frappe…"   20 minutes ago   Up 20 minutes                                                           dppl-backend-1
2851433a6c89   mariadb:10.6                   "docker-entrypoint.s…"   20 minutes ago   Up 20 minutes (healthy)   3306/tcp                                      dppl-db-1
b2df6c296cf3   navneetindusworks/dppl:3.1.3   "bench worker --queu…"   20 minutes ago   Up 20 minutes                                                           dppl-queue-long-1
4d6cf3b45936   redis:6.2-alpine               "docker-entrypoint.s…"   20 minutes ago   Up 20 minutes             6379/tcp                                      dppl-redis-queue-1
8b6791982f7b   navneetindusworks/dppl:3.1.3   "bench worker --queu…"   20 minutes ago   Up 20 minutes                                                           dppl-queue-short-1
633f47db2a2e   navneetindusworks/dppl:3.1.3   "bench schedule"         20 minutes ago   Up 20 minutes                                                           dppl-scheduler-1



docker inspect dppl-backend-1 | grep -A 20 "NetworkSettings"
        "NetworkSettings": {
            "Bridge": "",
            "SandboxID": "c06b00ac73f7eaba6a3579e5f22b51a841aa04c58ccf182a62934e49043eec3d",
            "SandboxKey": "/var/run/docker/netns/c06b00ac73f7",
            "Ports": {},
            "HairpinMode": false,
            "LinkLocalIPv6Address": "",
            "LinkLocalIPv6PrefixLen": 0,
            "SecondaryIPAddresses": null,
            "SecondaryIPv6Addresses": null,
            "EndpointID": "",
            "Gateway": "",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "IPAddress": "",
            "IPPrefixLen": 0,
            "IPv6Gateway": "",
            "MacAddress": "",
            "Networks": {
                "dppl_default": {
                    "IPAMConfig": null,
                    
                    
                    
docker inspect dppl-frontend-1 | grep -A 20 "NetworkSettings"
        "NetworkSettings": {
            "Bridge": "",
            "SandboxID": "3982653ec60e6773e1efa3f7caa25b8fc0462287e38dbd014e70eaede8874b7b",
            "SandboxKey": "/var/run/docker/netns/3982653ec60e",
            "Ports": {
                "8080/tcp": [
                    {
                        "HostIp": "0.0.0.0",
                        "HostPort": "8080"
                    },
                    {
                        "HostIp": "::",
                        "HostPort": "8080"
                    }
                ]
            },
            "HairpinMode": false,
            "LinkLocalIPv6Address": "",
            "LinkLocalIPv6PrefixLen": 0,
            "SecondaryIPAddresses": null,
            "SecondaryIPv6Addresses": null,


docker inspect dppl-websocket-1 | grep -A 20 "NetworkSettings"
        "NetworkSettings": {
            "Bridge": "",
            "SandboxID": "58b8365c9505f08a58279b6fdbfe01710ecb47a82532b56376dcd7f98afcbe56",
            "SandboxKey": "/var/run/docker/netns/58b8365c9505",
            "Ports": {},
            "HairpinMode": false,
            "LinkLocalIPv6Address": "",
            "LinkLocalIPv6PrefixLen": 0,
            "SecondaryIPAddresses": null,
            "SecondaryIPv6Addresses": null,
            "EndpointID": "",
            "Gateway": "",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "IPAddress": "",
            "IPPrefixLen": 0,
            "IPv6Gateway": "",
            "MacAddress": "",
            "Networks": {
                "dppl_default": {
                    "IPAMConfig": null,

For some reason realtime update functionality that should trigger job_metrics_update on:
- DashboardComponent.vue path: dppl_mes/frontend/src/components/DashboardComponent.vue
- FactoryFloorMap.vue path: dppl_mes/frontend/src/components/FactoryFloorMap.vue
Is not working... can you please check why?