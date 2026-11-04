from app.models.audit_log import AuditLog
from app.core.auth import CurrentUser


def create_audit_log(
    db,
    user: CurrentUser,
    action: str,
    entity: str,
    entity_id: str,
    old_values = None,
    new_values = None,
):
    audit =  AuditLog(
        actor_guid=user.guid,
        actor_username=user.username,
        actor_full_name=user.full_name,
        actor_email=user.email,
        action=action,
        entity=entity,
        entity_id=str(entity_id),
        old_values=old_values,
        new_values=new_values
    )

    db.add(audit)

    return audit
