#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
An example to show receiving events from an Event Hub asynchronously.
"""

import asyncio
import json
import os
import time
from azure.eventhub.aio import EventHubConsumerClient

if 'CONNECTION_STR' in os.environ and 'EVENTHUB_NAME' in os.environ is None:
    raise EnvironmentError("Failed because CONNECTION_STR or EVENTHUB_NAME environemt variable is not set.")

if 'STARTING_POSITION' in os.environ is None:
    STARTING_POSITION = "-1"
else:
    STARTING_POSITION = os.environ['STARTING_POSITION']

CONNECTION_STR = os.environ["EVENT_HUB_CONN_STR"]
EVENTHUB_NAME = os.environ['EVENT_HUB_NAME']

print("Starting position: {}",STARTING_POSITION)
time.sleep(10)

async def on_event(partition_context, event):
    # Put your code here.
    # If the operation is i/o intensive, async will have better performance.
    #print("Received event from partition: {}.".format(partition_context.partition_id))
    print("Received the event from the partition with ID: \"{}\"".format(partition_context.partition_id))
    print(json.dumps(json.loads(event.body_as_str(encoding='UTF-8')),indent=4, sort_keys=True))
    await partition_context.update_checkpoint(event)


async def on_partition_initialize(partition_context):
    # Put your code here.
    print("Partition: {} has been initialized.".format(partition_context.partition_id))


async def on_partition_close(partition_context, reason):
    # Put your code here.
    print("Partition: {} has been closed, reason for closing: {}.".format(
        partition_context.partition_id,
        reason
    ))


async def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


async def main():
    client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group="$default",
        eventhub_name=EVENTHUB_NAME
    )
    async with client:
        await client.receive(
            on_event=on_event,
            on_error=on_error,
            on_partition_close=on_partition_close,
            on_partition_initialize=on_partition_initialize,
            starting_position=STARTING_POSITION,  # "-1" is from the beginning of the partition.
        )

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())