import os
from supabase import create_client
import logging

logger = logging.getLogger(__name__)

class SupabaseConnector:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            logger.error("Variáveis SUPABASE_URL/SUPABASE_KEY não configuradas")
            raise ValueError("Credenciais Supabase ausentes")
            
        self.client = create_client(self.url, self.key)
        logger.info("Conexão com Supabase estabelecida")

    def upsert_property(self, item: dict):
        try:
            # Converter campos JSON quando necessário
            if 'descricao' in item and isinstance(item['descricao'], str):
                item['descricao'] = item['descricao']  # Já é string JSON
            
            response = self.client.table('imoveis').upsert(
                [item],
                on_conflict='id_dfi'
            ).execute()
            
            if response.data:
                logger.info(f"Upsert realizado: ID {item['id_dfi']}")
                return True
                
        except Exception as e:
            logger.error(f"Erro no upsert ID {item.get('id_dfi')}: {str(e)}")
            return False