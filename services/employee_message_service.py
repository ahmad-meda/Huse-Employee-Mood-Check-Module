from Files.SQLAlchemyModels import LeadMessageHistory

class EmployeeMessageHistoryService:
    @staticmethod
    def get_message_history(session, contact_number):
        """
            Retrieve all message history for a contact (optionally filtered by session).
            """
        try:
            query = session.query(LeadMessageHistory).filter_by(contact_number=contact_number)
            history = query.order_by(LeadMessageHistory.timestamp.asc()).all()
            return [{"role": m.role, "content": m.content, "timestamp": m.timestamp.isoformat() if m.timestamp else None} for m in history]
        except Exception as e:
            print(f"Error retrieving message history: {e}")
            raise

    @staticmethod
    def save_message(session, contact_number, role, content):
        """
        Save a message to the lead message history.
        """
        try:
            msg = LeadMessageHistory(
                contact_number=contact_number,
                role=role,
                content=content
            )
            session.add(msg)
            session.commit()
            return msg.id
        except Exception as e:
            print(f"Error saving message: {e}")
            session.rollback()
            raise

    @staticmethod
    def clear_message_history(session, contact_number):
        """
        Delete all message history for a contact (optionally for a specific session).
        """
        try:
            query = session.query(LeadMessageHistory).filter_by(contact_number=contact_number)
            deleted = query.delete()
            session.commit()
            return deleted
        except Exception as e:
            print(f"Error clearing message history: {e}")
            session.rollback()
            raise