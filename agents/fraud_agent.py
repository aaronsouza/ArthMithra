def check_for_fraud(customer_data: dict):
    """Simulates a fraud check."""
    # Example: Check if PAN name matches Aadhar name
    if customer_data.get("pan_name") != customer_data.get("aadhar_name"):
        return {"is_fraud": True, "reason": "Name mismatch in documents."}

    # Add more simple checks here...
    return {"is_fraud": False, "reason": "No obvious red flags detected."}