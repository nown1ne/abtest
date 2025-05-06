from sqlalchemy.orm import Session
import models, database

def log_event(variant, event_type, plan=None, revenue=None):
    db = next(database.get_db())
    event = models.Event(
        variant=variant,
        event_type=event_type,
        plan=plan,
        revenue=revenue
    )
    db.add(event)
    db.commit()
    db.refresh(event)

def get_metrics():
    db = next(database.get_db())
    data = db.query(models.Event).all()
    
    metrics = {"A": {"clicks": 0, "conversions": 0, "revenue": 0.0},
               "B": {"clicks": 0, "conversions": 0, "revenue": 0.0}}

    for e in data:
        if e.variant not in metrics:
            continue
        if e.event_type == "click":
            metrics[e.variant]["clicks"] += 1
        if e.event_type == "conversion":
            metrics[e.variant]["conversions"] += 1
            metrics[e.variant]["revenue"] += e.revenue or 0

    return metrics
