from app.database.session_generator import session_background
from app.modules.encrypter import generate_key
from app.modules.model import Magento_Service

session_background('delete')
session = session_background( 'create')
generate_key()
service = Magento_Service( session)
session.add( service)
session.commit()
session.close()
