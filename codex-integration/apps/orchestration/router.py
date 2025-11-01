from .workflows import order_created, participant_joined

WORKFLOWS = {
    "order.created": order_created.run,
    "participant.joined": participant_joined.run,
}

async def route_event(event):
    handler = WORKFLOWS.get(event["event_type"])
    if not handler:
        return {"status": "unhandled"}
    return await handler(event)
