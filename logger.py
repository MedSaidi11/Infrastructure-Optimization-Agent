from loguru import logger

logger.add(
    "app.log", 
    rotation="1 MB",        
    compression="zip",      
    colorize=True,          
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>"
)