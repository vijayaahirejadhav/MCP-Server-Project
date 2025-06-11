from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging
from config.config import DATABASE_URL

logger = logging.getLogger(__name__)

Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    post_id = Column(String, unique=True, nullable=False)
    content = Column(String, nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    posted = Column(Boolean, default=False)
    posted_at = Column(DateTime, nullable=True)
    tags = Column(String, nullable=True)

class Database:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def add_post(self, post_id: str, content: str, scheduled_time: datetime, tags: list = None) -> bool:
        """
        Add a new post to the database
        """
        try:
            session = self.Session()
            post = Post(
                post_id=post_id,
                content=content,
                scheduled_time=scheduled_time,
                tags=",".join(tags) if tags else None
            )
            session.add(post)
            session.commit()
            logger.info(f"Added post {post_id} to database")
            return True
        except Exception as e:
            logger.error(f"Failed to add post to database: {str(e)}")
            session.rollback()
            return False
        finally:
            session.close()

    def get_post(self, post_id: str) -> Post:
        """
        Get a post by ID
        """
        try:
            session = self.Session()
            post = session.query(Post).filter_by(post_id=post_id).first()
            return post
        except Exception as e:
            logger.error(f"Failed to get post from database: {str(e)}")
            return None
        finally:
            session.close()

    def get_pending_posts(self) -> list:
        """
        Get all pending posts
        """
        try:
            session = self.Session()
            posts = session.query(Post).filter_by(posted=False).all()
            return posts
        except Exception as e:
            logger.error(f"Failed to get pending posts: {str(e)}")
            return []
        finally:
            session.close()

    def mark_post_as_posted(self, post_id: str) -> bool:
        """
        Mark a post as posted
        """
        try:
            session = self.Session()
            post = session.query(Post).filter_by(post_id=post_id).first()
            if post:
                post.posted = True
                post.posted_at = datetime.utcnow()
                session.commit()
                logger.info(f"Marked post {post_id} as posted")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to mark post as posted: {str(e)}")
            session.rollback()
            return False
        finally:
            session.close()

    def delete_post(self, post_id: str) -> bool:
        """
        Delete a post
        """
        try:
            session = self.Session()
            post = session.query(Post).filter_by(post_id=post_id).first()
            if post:
                session.delete(post)
                session.commit()
                logger.info(f"Deleted post {post_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete post: {str(e)}")
            session.rollback()
            return False
        finally:
            session.close() 