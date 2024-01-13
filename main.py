from models import Sources, RelatedArticles
from util import Database
from google_news import GoogleRSS
import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger("gneesrss")
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(f"gneesrss.log", interval=1, backupCount=3, when='d')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == '__main__':
    logging.info('START')
    db = Database()
    sources = db.session.query(Sources).all()
    logger.info(f"Len sources = {len(sources)}")
    for source in sources:
        g = GoogleRSS()
        for d in g.get_data(f"site:{source.domain}"):
            m, created = RelatedArticles.get_or_create(
                db.session, 
                defaults={
                    **d
                },
                title=d['title'])
            logger.info(f"{m.id} is created = {created}")
            # if created:
            if source.university:
                m.university = [*m.university, source.university]
            if source.state:
                m.state = [*m.state, source.state]
            db.session.commit()