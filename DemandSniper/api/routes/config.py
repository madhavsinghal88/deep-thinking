from fastapi import APIRouter, HTTPException
from config.loader import load_search_config, load_scoring_config
from api.schemas import SearchConfig, ScoringConfig

router = APIRouter(prefix="/config", tags=["configuration"])


@router.get("/search", response_model=SearchConfig)
async def get_search_config():
    """Get current search configuration."""
    config = load_search_config()
    return SearchConfig(**config)


@router.get("/scoring", response_model=ScoringConfig)
async def get_scoring_config():
    """Get current scoring configuration."""
    config = load_scoring_config()
    return ScoringConfig(**config)


@router.put("/search")
async def update_search_config(config: SearchConfig):
    """Update search configuration."""
    import yaml
    from config.settings import settings
    
    config_path = settings.CONFIG_DIR / "search_config.yaml"
    
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config.dict(), f, default_flow_style=False)
        return {"message": "Search configuration updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update configuration: {str(e)}"
        )


@router.put("/scoring")
async def update_scoring_config(config: ScoringConfig):
    """Update scoring configuration."""
    import yaml
    from config.settings import settings
    
    config_path = settings.CONFIG_DIR / "scoring_config.yaml"
    
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config.dict(), f, default_flow_style=False)
        return {"message": "Scoring configuration updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update configuration: {str(e)}"
        )
