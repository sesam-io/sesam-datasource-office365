# sesam-office365-csvfileshare-service
sesam office365 csv fileshare microservice

This is a simple microservice with the purpose of reading CSV-files that is shared on an Office365 / SharePoint Online site.
The microservice should be configured with the base url of the SharePoint-site, and can be called from a pipe using the following
syntax: "http://sesam-office365-csvfileshare-service:5000/nameofcsvfile.csv".

An example of system config:

```json
{
  "_id": "sesam-office365-csvfileshare-service",
  "type": "system:microservice",
  "connect_timeout": 60,
  "docker": {
    "environment": {
      "baseurl": "https://loremipsum.sharepoint.com",
      "username": "$ENV(username)",
      "password": "$SECRET(password)"
    },
    "image": "sesam/sesam-office365-csvfileshare-service:latest",
    "memory": 64,
    "port": 5000
  },
  "read_timeout": 7200,
  "verify_ssl": false
}
```

