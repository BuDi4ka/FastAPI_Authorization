import unittest
from unittest.mock import MagicMock
from datetime import date, timedelta

from src.database.models import Contacts, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    update_contact,
    delete_contact,
    get_upcoming_birthdays,
)


class TestContactsRepository(unittest.IsolatedAsyncioTestCase):
    async def test_get_contacts(self):
        db = MagicMock()
        current_user = User(id=1)
        db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = [
            Contacts(id=1, user_id=1, first_name="Test", last_name="User")
        ]

        result = await get_contacts(skip=0, limit=10, current_user=current_user, db=db)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].first_name, "Test")
        self.assertEqual(result[0].last_name, "User")

    async def test_get_contact_found(self):
        db = MagicMock()
        current_user = User(id=1)

        contact = Contacts(
            id=1, user_id=1, first_name="Test", last_name="User", email="test@example.com"
        )

        db.query.return_value.filter.return_value.filter.return_value.first.return_value = contact

        result = await get_contact(first_name="Test", current_user=current_user, db=db)

        self.assertIsNotNone(result)
        self.assertEqual(result.first_name, "Test")
        self.assertEqual(result.email, "test@example.com")

    async def test_get_contact_not_found(self):
        db = MagicMock()
        current_user = User(id=1)

        db.query.return_value.filter.return_value.filter.return_value.first.return_value = None

        result = await get_contact(first_name="NonExistent", current_user=current_user, db=db)

        self.assertIsNone(result)

    async def test_create_contact(self):
        db = MagicMock()
        current_user = User(id=1)
        body = ContactModel(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            mobile_number="1234567890",
            date_of_birth=date(1990, 1, 1),
            additional_notes="Sample notes",
        )

        new_contact = Contacts(
            id=1,
            user_id=current_user.id,
            first_name=body.first_name,
            last_name=body.last_name,
            email=body.email,
            mobile_number=body.mobile_number,
            date_of_birth=body.date_of_birth,
            additional_notes=body.additional_notes,
        )
        db.add = MagicMock()
        db.commit = MagicMock()
        db.refresh = MagicMock()

        db.refresh.return_value = new_contact

        result = await create_contact(body, current_user, db)
        self.assertIsNotNone(result)
        self.assertEqual(result.first_name, "Test")
        self.assertEqual(result.email, "test@example.com")

    async def test_update_contact(self):
        db = MagicMock()
        current_user = User(id=1)
        body = ContactModel(
            first_name="Updated",
            last_name="User",
            email="updated@example.com",
            mobile_number="0987654321",
            date_of_birth=date(1990, 2, 2),
            additional_notes="Updated notes",
        )

        contact_to_update = Contacts(
            id=1,
            user_id=current_user.id,
            first_name="Old",
            last_name="User",
            email="old@example.com",
            mobile_number="1234567890",
            date_of_birth=date(1990, 1, 1),
            additional_notes="Old notes",
        )

        db.query.return_value.filter.return_value.first.return_value = contact_to_update

        result = await update_contact(1, body, current_user, db)
        self.assertIsNotNone(result)
        self.assertEqual(result.first_name, "Updated")
        self.assertEqual(result.email, "updated@example.com")

    async def test_delete_contact(self):
        db = MagicMock()
        current_user = User(id=1)
        contact_to_delete = Contacts(
            id=1, user_id=current_user.id, first_name="Test", last_name="User"
        )
        db.query.return_value.filter.return_value.first.return_value = contact_to_delete

        result = await delete_contact(1, current_user, db)
        db.delete.assert_called_once_with(contact_to_delete)
        db.commit.assert_called_once()
        self.assertIsNotNone(result)
        self.assertEqual(result.first_name, "Test")

    def test_get_upcoming_birthdays(self):
        db = MagicMock()
        current_user = User(id=1)

        today = date.today()
        next_week = today + timedelta(days=7)
        contact_with_birthday = Contacts(
            id=1,
            user_id=current_user.id,
            first_name="Birthday",
            last_name="User",
            date_of_birth=today,
        )
        db.query.return_value.filter.return_value.all.return_value = [contact_with_birthday]

        result = get_upcoming_birthdays(current_user, db)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].first_name, "Birthday")


if __name__ == "__main__":
    unittest.main()