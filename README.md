# evthubreciever
Simple eventhub reciever

## Ready to go 

You can use docker image to connect to the event hub and display all the events

Environment variables>

| Variable Name | Description |
|---|---|
| EVENT_HUB_CONN_STR | **Required** Connection string to your Azure Eventhub Namespace with key (Listener rights are necessary) |
| EVENT_HUB_NAME | **Required** Name of the eventhub |
| STARTING_POSITION | (Optional) If you will add large number here, there will be an error, but in error message you will get the actual events count. Starting position is the place, from where you would like to pickup the events.  |

For Windows:
```powershell
docker run -it `
     -e EVENT_HUB_CONN_STR='<Your listener access connection string>' ` 
     -e EVENT_HUB_NAME='<Hub Name>' ` 
     -e STARTING_POSITION=<Large number here>  ` 
     ecaha/evt-p
```

For Linux:
```bash
docker run -it \
     -e EVENT_HUB_CONN_STR='<Your listener access connection string>' \
     -e EVENT_HUB_NAME='<Hub Name>' \
     -e STARTING_POSITION=<Large number here>  \
     ecaha/evt-p
```
