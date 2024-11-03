#!/bin/bash
result=$(curl -s -X POST https://api.uptimerobot.com/v2/getMonitors?api_key=<APIKEY>)
echo $result | jq -r '
.monitors[] |
(
    if .status == 2 then 0
    elif .status == 0 or .status == 1 then 1
    elif .status == 8 or .status == 9 then 2
    else 3
    end
) as $statusCode |
(
    if .status == 0 then "paused"
    elif .status == 1 then "not checked yet"
    elif .status == 2 then "up"
    elif .status == 8 then "seems down"
    elif .status == 9 then "down"
    else "unknown"
    end
) as $statusText |
"\($statusCode) \"\(.friendly_name)\" - UptimeRobot \(.friendly_name) \($statusText)"
'
