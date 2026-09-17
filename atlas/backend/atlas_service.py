from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import sqlite3
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable


class AtlasError(Exception):
    pass


class AuthenticationError(AtlasError):
    pass


class AuthorizationError(AtlasError):
    pass


class ConsentError(AtlasError):
    pass


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:20]}"


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _password_hash(password: str, salt: bytes) -> bytes:
    if len(password) < 10:
        raise ValueError("password must be at least 10 characters")
    return hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32)


@dataclass(frozen=True)
class Session:
    token: str
    user_id: str
    expires_at: int


class AtlasService:
    """Synthetic/private Atlas service used to test real authorization invariants.

    This is intentionally dependency-free and suitable for CI. It is not a claim of
    production hosting, regulatory compliance, or completed independent security review.
    """

    PURPOSES = {
        "storage",
        "ai_summarization",
        "ai_theme_extraction",
        "named_sharing",
        "public_display",
        "analytics",
        "research_use",
    }

    def __init__(self, db_path: str = ":memory:") -> None:
        self.db = sqlite3.connect(db_path)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys = ON")
        self._migrate()

    def close(self) -> None:
        self.db.close()

    def _migrate(self) -> None:
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                password_salt BLOB NOT NULL,
                password_hash BLOB NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sessions (
                token_hash TEXT PRIMARY KEY,
                user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                expires_at INTEGER NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS atlases (
                atlas_id TEXT PRIMARY KEY,
                author_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                atlas_type TEXT NOT NULL CHECK(atlas_type IN ('founder','learner','visitor')),
                display_name TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS entries (
                entry_id TEXT PRIMARY KEY,
                atlas_id TEXT NOT NULL REFERENCES atlases(atlas_id) ON DELETE CASCADE,
                author_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                body TEXT NOT NULL,
                memory_confidence TEXT NOT NULL,
                corroboration_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS consents (
                consent_id TEXT PRIMARY KEY,
                author_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                purpose TEXT NOT NULL,
                scope_json TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('active','revoked')),
                created_at TEXT NOT NULL,
                revoked_at TEXT
            );
            CREATE TABLE IF NOT EXISTS ai_summaries (
                summary_id TEXT PRIMARY KEY,
                author_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                entry_id TEXT NOT NULL REFERENCES entries(entry_id) ON DELETE CASCADE,
                summary_text TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('user_review_required','accepted','rejected')),
                created_at TEXT NOT NULL,
                reviewed_at TEXT
            );
            CREATE TABLE IF NOT EXISTS graph_edges (
                edge_id TEXT PRIMARY KEY,
                author_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                source_entry_id TEXT NOT NULL REFERENCES entries(entry_id) ON DELETE CASCADE,
                target_entry_id TEXT NOT NULL REFERENCES entries(entry_id) ON DELETE CASCADE,
                provenance TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('pending_review','accepted','rejected')),
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS exports (
                export_id TEXT PRIMARY KEY,
                author_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                atlas_id TEXT NOT NULL REFERENCES atlases(atlas_id) ON DELETE CASCADE,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS audit_events (
                audit_id TEXT PRIMARY KEY,
                actor_id TEXT,
                action TEXT NOT NULL,
                object_type TEXT NOT NULL,
                object_id TEXT,
                result TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS deletion_tombstones (
                tombstone_id TEXT PRIMARY KEY,
                former_user_id TEXT NOT NULL,
                deleted_at TEXT NOT NULL,
                counts_json TEXT NOT NULL
            );
            """
        )
        self.db.commit()

    def register_user(self, email: str, password: str) -> str:
        normalized = email.strip().lower()
        if "@" not in normalized:
            raise ValueError("valid email required")
        salt = secrets.token_bytes(16)
        digest = _password_hash(password, salt)
        user_id = _new_id("USR")
        self.db.execute(
            "INSERT INTO users(user_id,email,password_salt,password_hash,created_at) VALUES(?,?,?,?,?)",
            (user_id, normalized, salt, digest, _utc_now()),
        )
        self.db.commit()
        self._audit(user_id, "register", "user", user_id, "allowed")
        return user_id

    def login(self, email: str, password: str, ttl_seconds: int = 3600) -> Session:
        row = self.db.execute(
            "SELECT * FROM users WHERE email = ?", (email.strip().lower(),)
        ).fetchone()
        if not row:
            raise AuthenticationError("invalid credentials")
        try:
            candidate = _password_hash(password, row["password_salt"])
        except ValueError:
            raise AuthenticationError("invalid credentials") from None
        if not hmac.compare_digest(candidate, row["password_hash"]):
            self._audit(row["user_id"], "login", "session", None, "denied")
            raise AuthenticationError("invalid credentials")
        token = secrets.token_urlsafe(32)
        expires_at = int(time.time()) + ttl_seconds
        self.db.execute(
            "INSERT INTO sessions(token_hash,user_id,expires_at,created_at) VALUES(?,?,?,?)",
            (_hash_token(token), row["user_id"], expires_at, _utc_now()),
        )
        self.db.commit()
        self._audit(row["user_id"], "login", "session", None, "allowed")
        return Session(token=token, user_id=row["user_id"], expires_at=expires_at)

    def logout(self, token: str) -> None:
        token_hash = _hash_token(token)
        row = self.db.execute(
            "SELECT user_id FROM sessions WHERE token_hash = ?", (token_hash,)
        ).fetchone()
        self.db.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash,))
        self.db.commit()
        self._audit(row["user_id"] if row else None, "logout", "session", None, "allowed")

    def _require_user(self, token: str) -> str:
        row = self.db.execute(
            "SELECT user_id, expires_at FROM sessions WHERE token_hash = ?", (_hash_token(token),)
        ).fetchone()
        if not row or row["expires_at"] <= int(time.time()):
            if row:
                self.db.execute("DELETE FROM sessions WHERE token_hash = ?", (_hash_token(token),))
                self.db.commit()
            raise AuthenticationError("session invalid or expired")
        return row["user_id"]

    def _owned_row(self, table: str, id_column: str, object_id: str, user_id: str) -> sqlite3.Row:
        if table not in {"atlases", "entries", "ai_summaries", "graph_edges", "exports"}:
            raise ValueError("unsupported table")
        row = self.db.execute(
            f"SELECT * FROM {table} WHERE {id_column} = ? AND author_id = ?",
            (object_id, user_id),
        ).fetchone()
        if not row:
            self._audit(user_id, "access", table, object_id, "denied")
            raise AuthorizationError("object unavailable")
        return row

    def create_atlas(self, token: str, atlas_type: str, display_name: str | None = None) -> str:
        user_id = self._require_user(token)
        if atlas_type not in {"founder", "learner", "visitor"}:
            raise ValueError("unsupported atlas type")
        atlas_id = _new_id("ATL")
        now = _utc_now()
        self.db.execute(
            "INSERT INTO atlases(atlas_id,author_id,atlas_type,display_name,created_at,updated_at) VALUES(?,?,?,?,?,?)",
            (atlas_id, user_id, atlas_type, display_name, now, now),
        )
        self.db.commit()
        self._audit(user_id, "create", "atlas", atlas_id, "allowed")
        return atlas_id

    def add_entry(
        self,
        token: str,
        atlas_id: str,
        body: str,
        memory_confidence: str = "uncertain",
        corroboration_status: str = "not_checked",
    ) -> str:
        user_id = self._require_user(token)
        self._owned_row("atlases", "atlas_id", atlas_id, user_id)
        if not body.strip():
            raise ValueError("entry body required")
        entry_id = _new_id("ENT")
        now = _utc_now()
        self.db.execute(
            "INSERT INTO entries(entry_id,atlas_id,author_id,body,memory_confidence,corroboration_status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?)",
            (entry_id, atlas_id, user_id, body, memory_confidence, corroboration_status, now, now),
        )
        self.db.commit()
        self._audit(user_id, "create", "entry", entry_id, "allowed")
        return entry_id

    def get_entry(self, token: str, entry_id: str) -> dict[str, Any]:
        user_id = self._require_user(token)
        row = self._owned_row("entries", "entry_id", entry_id, user_id)
        return dict(row)

    def list_entries(self, token: str, atlas_id: str) -> list[dict[str, Any]]:
        user_id = self._require_user(token)
        self._owned_row("atlases", "atlas_id", atlas_id, user_id)
        rows = self.db.execute(
            "SELECT * FROM entries WHERE atlas_id = ? AND author_id = ? ORDER BY created_at",
            (atlas_id, user_id),
        ).fetchall()
        return [dict(row) for row in rows]

    def search_entries(self, token: str, query: str) -> list[dict[str, Any]]:
        user_id = self._require_user(token)
        rows = self.db.execute(
            "SELECT entry_id,atlas_id,memory_confidence,corroboration_status,created_at FROM entries WHERE author_id = ? AND body LIKE ? ORDER BY created_at",
            (user_id, f"%{query}%"),
        ).fetchall()
        return [dict(row) for row in rows]

    def grant_consent(self, token: str, purpose: str, scope_entry_ids: Iterable[str]) -> str:
        user_id = self._require_user(token)
        if purpose not in self.PURPOSES:
            raise ValueError("unsupported consent purpose")
        scope = sorted(set(scope_entry_ids))
        for entry_id in scope:
            self._owned_row("entries", "entry_id", entry_id, user_id)
        consent_id = _new_id("CON")
        self.db.execute(
            "INSERT INTO consents(consent_id,author_id,purpose,scope_json,status,created_at) VALUES(?,?,?,?,?,?)",
            (consent_id, user_id, purpose, json.dumps(scope), "active", _utc_now()),
        )
        self.db.commit()
        self._audit(user_id, "grant_consent", "consent", consent_id, "allowed")
        return consent_id

    def revoke_consent(self, token: str, consent_id: str) -> None:
        user_id = self._require_user(token)
        row = self.db.execute(
            "SELECT author_id FROM consents WHERE consent_id = ? AND author_id = ?",
            (consent_id, user_id),
        ).fetchone()
        if not row:
            raise AuthorizationError("object unavailable")
        self.db.execute(
            "UPDATE consents SET status='revoked', revoked_at=? WHERE consent_id=?",
            (_utc_now(), consent_id),
        )
        self.db.commit()
        self._audit(user_id, "revoke_consent", "consent", consent_id, "allowed")

    def _consent_covers(self, user_id: str, purpose: str, entry_id: str) -> bool:
        rows = self.db.execute(
            "SELECT scope_json FROM consents WHERE author_id=? AND purpose=? AND status='active'",
            (user_id, purpose),
        ).fetchall()
        return any(entry_id in json.loads(row["scope_json"]) for row in rows)

    def create_ai_summary(self, token: str, entry_id: str, summary_text: str) -> str:
        user_id = self._require_user(token)
        self._owned_row("entries", "entry_id", entry_id, user_id)
        if not self._consent_covers(user_id, "ai_summarization", entry_id):
            self._audit(user_id, "ai_summarize", "entry", entry_id, "denied_no_consent")
            raise ConsentError("active AI-summary consent does not cover this entry")
        summary_id = _new_id("AIS")
        self.db.execute(
            "INSERT INTO ai_summaries(summary_id,author_id,entry_id,summary_text,status,created_at) VALUES(?,?,?,?,?,?)",
            (summary_id, user_id, entry_id, summary_text, "user_review_required", _utc_now()),
        )
        self.db.commit()
        self._audit(user_id, "ai_summarize", "ai_summary", summary_id, "allowed")
        return summary_id

    def accept_ai_summary(self, token: str, summary_id: str) -> None:
        user_id = self._require_user(token)
        self._owned_row("ai_summaries", "summary_id", summary_id, user_id)
        self.db.execute(
            "UPDATE ai_summaries SET status='accepted', reviewed_at=? WHERE summary_id=? AND author_id=?",
            (_utc_now(), summary_id, user_id),
        )
        self.db.commit()
        self._audit(user_id, "accept", "ai_summary", summary_id, "allowed")

    def create_graph_edge(self, token: str, source_entry_id: str, target_entry_id: str) -> str:
        user_id = self._require_user(token)
        self._owned_row("entries", "entry_id", source_entry_id, user_id)
        self._owned_row("entries", "entry_id", target_entry_id, user_id)
        edge_id = _new_id("EDGE")
        self.db.execute(
            "INSERT INTO graph_edges(edge_id,author_id,source_entry_id,target_entry_id,provenance,status,created_at) VALUES(?,?,?,?,?,?,?)",
            (edge_id, user_id, source_entry_id, target_entry_id, "ai_suggested", "pending_review", _utc_now()),
        )
        self.db.commit()
        self._audit(user_id, "create", "graph_edge", edge_id, "allowed")
        return edge_id

    def export_atlas(self, token: str, atlas_id: str) -> dict[str, Any]:
        user_id = self._require_user(token)
        atlas = dict(self._owned_row("atlases", "atlas_id", atlas_id, user_id))
        entries = [dict(row) for row in self.db.execute(
            "SELECT * FROM entries WHERE atlas_id=? AND author_id=? ORDER BY created_at",
            (atlas_id, user_id),
        ).fetchall()]
        entry_ids = [entry["entry_id"] for entry in entries]
        summaries: list[dict[str, Any]] = []
        if entry_ids:
            placeholders = ",".join("?" for _ in entry_ids)
            summaries = [dict(row) for row in self.db.execute(
                f"SELECT * FROM ai_summaries WHERE author_id=? AND entry_id IN ({placeholders})",
                [user_id, *entry_ids],
            ).fetchall()]
        payload = {
            "export_version": 1,
            "author_id": user_id,
            "atlas": atlas,
            "entries": entries,
            "ai_summaries": summaries,
            "provenance_note": "AI summaries remain labeled as derived content.",
        }
        export_id = _new_id("EXP")
        self.db.execute(
            "INSERT INTO exports(export_id,author_id,atlas_id,payload_json,created_at) VALUES(?,?,?,?,?)",
            (export_id, user_id, atlas_id, json.dumps(payload, sort_keys=True), _utc_now()),
        )
        self.db.commit()
        self._audit(user_id, "export", "atlas", atlas_id, "allowed")
        return {"export_id": export_id, "payload": payload}

    def delete_entry(self, token: str, entry_id: str) -> None:
        user_id = self._require_user(token)
        row = self._owned_row("entries", "entry_id", entry_id, user_id)
        atlas_id = row["atlas_id"]
        # Delete stored export snapshots first so live system copies do not retain the narrative.
        self.db.execute("DELETE FROM exports WHERE author_id=? AND atlas_id=?", (user_id, atlas_id))
        # FK cascade removes AI summaries and graph edges that depend on the entry.
        self.db.execute("DELETE FROM entries WHERE entry_id=? AND author_id=?", (entry_id, user_id))
        # Remove the deleted entry from any active consent scope; empty scopes remain explicit records.
        consent_rows = self.db.execute(
            "SELECT consent_id,scope_json FROM consents WHERE author_id=?", (user_id,)
        ).fetchall()
        for consent in consent_rows:
            scope = [item for item in json.loads(consent["scope_json"]) if item != entry_id]
            self.db.execute(
                "UPDATE consents SET scope_json=? WHERE consent_id=?",
                (json.dumps(scope), consent["consent_id"]),
            )
        self.db.commit()
        self._audit(user_id, "delete", "entry", entry_id, "allowed")

    def delete_account(self, token: str) -> dict[str, int]:
        user_id = self._require_user(token)
        counts = {}
        for table in ("atlases", "entries", "consents", "ai_summaries", "graph_edges", "exports", "sessions"):
            column = "user_id" if table == "sessions" else "author_id"
            counts[table] = self.db.execute(
                f"SELECT COUNT(*) AS n FROM {table} WHERE {column}=?", (user_id,)
            ).fetchone()["n"]
        # Capture a minimal tombstone before deleting the account. No email/narrative is retained.
        self.db.execute(
            "INSERT INTO deletion_tombstones(tombstone_id,former_user_id,deleted_at,counts_json) VALUES(?,?,?,?)",
            (_new_id("DEL"), user_id, _utc_now(), json.dumps(counts, sort_keys=True)),
        )
        # User deletion cascades through all author-owned primary/derived/session tables.
        self.db.execute("DELETE FROM users WHERE user_id=?", (user_id,))
        self.db.commit()
        self._audit(None, "delete_account", "user", user_id, "completed")
        return counts

    def audit_events(self) -> list[dict[str, Any]]:
        return [dict(row) for row in self.db.execute(
            "SELECT * FROM audit_events ORDER BY created_at,audit_id"
        ).fetchall()]

    def raw_count(self, table: str, where: str = "", params: tuple[Any, ...] = ()) -> int:
        if table not in {
            "users", "sessions", "atlases", "entries", "consents", "ai_summaries",
            "graph_edges", "exports", "audit_events", "deletion_tombstones"
        }:
            raise ValueError("unsupported table")
        clause = f" WHERE {where}" if where else ""
        return int(self.db.execute(f"SELECT COUNT(*) AS n FROM {table}{clause}", params).fetchone()["n"])

    def _audit(self, actor_id: str | None, action: str, object_type: str, object_id: str | None, result: str) -> None:
        self.db.execute(
            "INSERT INTO audit_events(audit_id,actor_id,action,object_type,object_id,result,created_at) VALUES(?,?,?,?,?,?,?)",
            (_new_id("AUD"), actor_id, action, object_type, object_id, result, _utc_now()),
        )
        self.db.commit()
