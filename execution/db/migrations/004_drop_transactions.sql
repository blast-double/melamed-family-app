-- Last Edited: 2026-03-29
-- Migration: 004_drop_transactions
-- Drops the transactions table — Monarch is the source of truth for transaction data.
--
-- ROLLBACK: Re-run 002_tax_processing.sql to recreate the table.

BEGIN;

DROP TABLE IF EXISTS transactions;

COMMIT;
