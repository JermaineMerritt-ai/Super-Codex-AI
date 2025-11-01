def normalize_payload(source: str, x_event: str | None, payload: dict) -> dict:
	# Example mapping for Shopify order.created
	if source == "shopify" and (x_event == "orders/create" or payload.get("type") == "order.created"):
		return {
			"type": "order.created",
			"source": "ecommerce.shopify",
			"data": {
				"order_id": str(payload.get("id")),
				"participant_email": payload.get("email"),
				"total": payload.get("total_price"),
				"items": [{"sku": i.get("sku"), "qty": i.get("quantity")} for i in payload.get("line_items", [])],
			},
		}
	# Fallback passthrough
	return {"type": payload.get("type", "unknown"), "source": source, "data": payload}
