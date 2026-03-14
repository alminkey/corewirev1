def get_analytics_summary() -> dict:
    return {
        "page_metrics": {
            "homepage_views": 1240,
            "article_views": 3890,
            "citation_clicks": 214,
        },
        "queue_metrics": {
            "pending_jobs": 3,
            "failed_jobs": 0,
            "average_publish_minutes": 12,
        },
        "cost_metrics": {
            "monthly_budget_used_usd": 182.5,
            "average_cost_per_article_usd": 0.34,
        },
        "source_health": [
            {"source": "Reuters", "status": "healthy"},
            {"source": "AP", "status": "healthy"},
        ],
    }
