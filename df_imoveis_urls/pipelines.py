from itemadapter import ItemAdapter
from src.utils.supabase_loader import SupabaseConnector
import logging


logger = logging.getLogger(__name__)

class SupabasePipeline:
    def __init__(self):
        self.connector = SupabaseConnector()
        logger.info("Pipeline Supabase inicializada")

    def process_item(self, item, spider):
        # Converter campos numéricos
        numeric_fields = ['quartos', 'suites', 'garagens']
        for field in numeric_fields:
            if field in item:
                try:
                    item[field] = int(item[field])
                except (ValueError, TypeError):
                    item[field] = None
        
        # Processar características
        if 'características' in item and isinstance(item['características'], list):
            item['características'] = ', '.join(item['características'])
        
        # Enviar para Supabase
        if not self.connector.upsert_property(dict(item)):
            logger.warning(f"Falha ao processar item: {item['id_dfi']}")
        
        return item