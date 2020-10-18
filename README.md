[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Tioborto_raddar&metric=alert_status)](https://sonarcloud.io/dashboard?id=Tioborto_raddar)

## Summary

## Description  

This project uses [detect-secrets], from Yelp company, to analyze our project.

## Development

To get more information about development : [Developers.md](DEVELOPER.md)

## SPECS

http://localhost:3000/api


| ENDPOINT | TYPE | SPECS |
| --------- | --- | ----- |
| /webhook/github | POST | ... |
| /projects/{name}/_scan | POST | Analyze |
| /projects/{name}/refs/{refName} | GET | ... |


[detect-secrets]: https://github.com/Yelp/detect-secrets