import unittest

from tap_postgres.tap import TapPostgres
from tests.settings import DB_SCHEMA_NAME, DB_SQLALCHEMY_URL


class TestReplicationSlot(unittest.TestCase):
    def setUp(self):
        self.default_config = {"sqlalchemy_url": DB_SQLALCHEMY_URL}

    def test_default_slot_name(self):
        # Test backward compatibility when slot name is not provided.
        config = self.default_config
        tap = TapPostgres(config)
        self.assertEqual(
            tap.config.get("replication_slot_name", "tappostgres"), "tappostgres"
        )

    def test_custom_slot_name(self):
        # Test if the custom slot name is used.
        config = {**self.default_config, "replication_slot_name": "custom_slot"}
        tap = TapPostgres(config)
        self.assertEqual(tap.config["replication_slot_name"], "custom_slot")

    def test_multiple_slots(self):
        # Simulate using multiple configurations with different slot names.
        config_1 = {**self.default_config, "replication_slot_name": "slot_1"}
        config_2 = {**self.default_config, "replication_slot_name": "slot_2"}

        tap_1 = TapPostgres(config_1)
        tap_2 = TapPostgres(config_2)

        self.assertNotEqual(
            tap_1.config["replication_slot_name"],
            tap_2.config["replication_slot_name"],
        )
        self.assertEqual(tap_1.config["replication_slot_name"], "slot_1")
        self.assertEqual(tap_2.config["replication_slot_name"], "slot_2")

    def test_invalid_slot_name(self):
        # Test validation for invalid slot names (if any validation rules exist).
        invalid_config = {
            **self.default_config,
            "replication_slot_name": "invalid slot name!",
        }

        with self.assertRaises(ValueError) as context:
            TapPostgres(invalid_config)
        self.assertIn("must be alphanumeric", str(context.exception))
