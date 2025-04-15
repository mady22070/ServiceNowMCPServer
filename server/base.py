# server/base.py
def validate_data(data: dict, required_fields: list) -> bool:
    for field in required_fields:
        if field not in data:
            return False
    return True

def update_comments(ritm_id: str, comment: str) -> None:
    # In production, update the record using sn_client.update_record.
    print(f"RITM {ritm_id} updated with comment: {comment}")
