import utils.db_manager as db_manager
import services.wish_service as wish_service

db_manager.initialize()
wish_service.retrieve_history()
